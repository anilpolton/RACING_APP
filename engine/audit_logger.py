import os
import json
import datetime
from typing import List, Dict, Any, Optional

class DailyAuditLogger:
    """
    Persists all race predictions made during the day to a local daily JSON file.
    At midnight, the Reconciliation Engine reads this file, fetches actual official results,
    calculates P&L on minimum unit bets (e.g. R10 win, R6 trifecta box, R10 place accumulator),
    and formats the midnight audit report.
    """

    LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_logs")

    @classmethod
    def get_today_file(cls) -> str:
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        today_str = datetime.date.today().isoformat()
        return os.path.join(cls.LOG_DIR, f"predictions_{today_str}.json")

    @classmethod
    def log_prediction(cls, meeting: str, race_number: int, race_name: str,
                       top_pick_num: int, top_pick_name: str, bookie_odds: float,
                       trifecta_box: List[int], value_pick_num: Optional[int] = None,
                       value_pick_name: Optional[str] = None, value_odds: Optional[float] = None):
        filepath = cls.get_today_file()
        data = cls.load_today_predictions()

        entry = {
            "meeting": meeting,
            "race_number": race_number,
            "race_name": race_name,
            "logged_at": datetime.datetime.now().strftime("%H:%M:%S"),
            "top_pick": {
                "number": top_pick_num,
                "name": top_pick_name,
                "odds": bookie_odds,
                "min_bet": 10.0  # R10 standard minimum win stake
            },
            "trifecta_box": {
                "runners": trifecta_box,
                "min_bet": 6.0   # R1 per combination (6 combos = R6)
            },
            "value_bet": {
                "number": value_pick_num,
                "name": value_pick_name,
                "odds": value_odds,
                "min_bet": 10.0 if value_pick_num else 0.0
            } if value_pick_num else None
        }

        # Avoid duplicates for same race
        data = [r for r in data if not (r["meeting"] == meeting and r["race_number"] == race_number)]
        data.append(entry)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"📝 Logged prediction for {meeting} Race {race_number} to audit file.")

    @classmethod
    def log_pa_ticket(cls, meeting: str, pa_ticket_data: Dict[str, Any]):
        filepath = cls.get_today_file()
        data = cls.load_today_predictions()
        # Log PA ticket metadata
        pa_entry = {
            "type": "PLACE_ACCUMULATOR",
            "meeting": meeting,
            "logged_at": datetime.datetime.now().strftime("%H:%M:%S"),
            "legs": pa_ticket_data.get("legs", []),
            "total_combinations": pa_ticket_data.get("total_combinations", 1),
            "min_bet": pa_ticket_data.get("cost_25", 10.0) # Fractional/minimum bet
        }
        data = [r for r in data if r.get("type") != "PLACE_ACCUMULATOR"]
        data.append(pa_entry)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load_today_predictions(cls) -> List[Dict[str, Any]]:
        filepath = cls.get_today_file()
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []
