import time
import datetime
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from scrapers.smart_scraper import SmartSARacingProvider
from engine.predictor import QuantitativePredictor
from engine.exotics import ExoticsEngine
from engine.audit_logger import DailyAuditLogger
from engine.midnight_audit import MidnightReconciliationEngine
from alerts.whatsapp_service import WhatsAppAlertService
from alerts.email_service import EmailAlertService
from config import config

class DailyRacingAgent:
    def __init__(self):
        self.predictor = QuantitativePredictor()
        self.alert_service = WhatsAppAlertService()
        self.email_service = EmailAlertService()
        self.pa_dispatched_meetings = set()
        self.race_dispatched_ids = set()
        self.midnight_dispatched_dates = set()

    def run_cycle(self):
        now = datetime.datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        print(f"\n[{now.strftime('%H:%M:%S')}] 🔄 Checking SA racing status for {today_str}...")

        # 0. Check Midnight Audit Trigger (Runs at 00:00 every night)
        # Checks if midnight has hit and previous day's audit hasn't dispatched
        if now.hour == 0 and today_str not in self.midnight_dispatched_dates:
            print("🌙 Midnight detected! Executing daily reconciliation and P&L audit...")
            yesterday_str = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            MidnightReconciliationEngine.run_midnight_report(yesterday_str)
            self.midnight_dispatched_dates.add(today_str)

        races = SmartSARacingProvider.fetch_todays_full_card()
        if not races:
            print("ℹ️ No active SA meetings or races found currently.")
            return

        meeting_name = races[0].meeting
        print(f"📍 Active Meeting: {meeting_name} ({len(races)} races found)")

        # 1. Place Accumulator Check (1 Hour Before Leg 1)
        if len(races) >= 7 and meeting_name not in self.pa_dispatched_meetings:
            pa_start_index = 1 if len(races) == 8 else 2
            if len(races) > pa_start_index + 6:
                pa_races = races[pa_start_index : pa_start_index + 7]
                first_pa_race = pa_races[0]
                post_dt = self._parse_post_time(first_pa_race.post_time, now)
                if post_dt:
                    diff_minutes = (post_dt - now).total_seconds() / 60.0
                    if 0 <= diff_minutes <= 65:
                        print(f"✅ Verified PA pool is open 1 hour before start! Generating PA ticket...")
                        all_analyses = [self.predictor.analyze_race(r) for r in races]
                        pa_analyses = all_analyses[pa_start_index : pa_start_index + 7]
                        pa_ticket = ExoticsEngine.generate_place_accumulator_ticket(meeting_name, pa_analyses)
                        pa_msg = self.alert_service.format_pa_alert(pa_ticket, all_race_analyses=all_analyses)

                        if config.ENABLE_EMAIL_ALERTS:
                            self.email_service.send_email(
                                subject=f"🎟️ Verified Place Accumulator (PA) & Full Card - {meeting_name}",
                                body_text=pa_msg
                            )
                        self.pa_dispatched_meetings.add(meeting_name)

        # 2. Race Predictions (15 Minutes Before Each Race) + Audit Logging
        for race in races:
            if race.race_id in self.race_dispatched_ids:
                continue
            post_dt = self._parse_post_time(race.post_time, now)
            if post_dt:
                diff_minutes = (post_dt - now).total_seconds() / 60.0
                if 0 <= diff_minutes <= 20:
                    print(f"🏇 Race {race.race_number} ({race.race_name}) starts in {diff_minutes:.1f} mins. Dispatching live prediction...")
                    analysis = self.predictor.analyze_race(race)
                    alert_msg = self.alert_service.format_prediction_alert(analysis)

                    # Persist prediction for midnight audit reconciliation
                    top = analysis.top_pick
                    val = analysis.best_value_bet
                    DailyAuditLogger.log_prediction(
                        meeting=meeting_name,
                        race_number=race.race_number,
                        race_name=race.race_name,
                        top_pick_num=top.horse.number,
                        top_pick_name=top.horse.name,
                        bookie_odds=top.bookmaker_odds,
                        trifecta_box=analysis.recommended_trifecta,
                        value_pick_num=val.horse.number if val else None,
                        value_pick_name=val.horse.name if val else None,
                        value_odds=val.bookmaker_odds if val else None
                    )

                    if config.ENABLE_EMAIL_ALERTS:
                        self.email_service.send_email(
                            subject=f"🏇 Live Prediction: {meeting_name} Race {race.race_number} ({race.post_time})",
                            body_text=alert_msg
                        )
                    self.race_dispatched_ids.add(race.race_id)

    def _parse_post_time(self, time_str: str, current_dt: datetime.datetime):
        try:
            clean_time = time_str.strip()[:5]
            parts = clean_time.split(":")
            return current_dt.replace(hour=int(parts[0]), minute=int(parts[1]), second=0, microsecond=0)
        except Exception:
            return None

    def start_loop(self, poll_interval_seconds=300):
        print("🚀 Starting Daily Racing Autonomous Agent Loop...")
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                print(f"⚠️ Error during cycle execution: {e}")
            time.sleep(poll_interval_seconds)

if __name__ == "__main__":
    agent = DailyRacingAgent()
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        agent.run_cycle()
    elif len(sys.argv) > 1 and sys.argv[1] == "--midnight-audit":
        MidnightReconciliationEngine.run_midnight_report()
    else:
        agent.start_loop(poll_interval_seconds=300)
