import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from scrapers.sa_racing import SARacingDataProvider
from engine.predictor import QuantitativePredictor
from alerts.email_service import EmailAlertService
from alerts.whatsapp_service import WhatsAppAlertService

def send_live_prediction(race_index: int = 0):
    races = SARacingDataProvider.get_live_greyville_card()
    if race_index >= len(races):
        return
    race = races[race_index]
    predictor = QuantitativePredictor()
    analysis = predictor.analyze_race(race)

    formatter = WhatsAppAlertService()
    msg = formatter.format_prediction_alert(analysis)

    email_service = EmailAlertService()
    print(f"Sending live prediction for Race {race.race_number} to anilpolton@live.co.za...")
    email_service.send_email(
        subject=f"🏇 LIVE RACE PREDICTION: {race.meeting} Race {race.race_number} ({race.post_time})",
        body_text=msg
    )

if __name__ == "__main__":
    send_live_prediction(0)
