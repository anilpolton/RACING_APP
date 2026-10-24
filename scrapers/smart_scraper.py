import urllib.request
import re
import json
from datetime import date
from typing import List, Optional, Tuple
from models import Horse, Race

class SmartSARacingProvider:
    """
    Live SA Scraper:
    Scans Sporting Life and online racecards dynamically for declared runners, draws, and live odds.
    """

    BASE_URL = "https://www.sportinglife.com"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    SA_VENUES = [
        "greyville", "fairview", "turffontein", "durbanville",
        "kenilworth", "scottsville", "vaal"
    ]
    VENUE_DISPLAY_NAMES = {
        "greyville": "Hollywoodbets Greyville",
        "fairview": "TAB Fairview",
        "turffontein": "TAB Turffontein (Inside)",
        "durbanville": "Hollywoodbets Durbanville",
        "kenilworth": "Hollywoodbets Kenilworth",
        "scottsville": "Hollywoodbets Scottsville",
        "vaal": "TAB Vaal"
    }

    @classmethod
    def detect_todays_venues(cls) -> List[Tuple[str, str]]:
        today = date.today().isoformat()
        url = f"{cls.BASE_URL}/racing/racecards"
        try:
            req = urllib.request.Request(url, headers=cls.HEADERS)
            html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
            found = []
            for venue in cls.SA_VENUES:
                pattern = rf'/racing/racecards/{today}/{venue}/racecard/\d+/'
                if re.search(pattern, html):
                    found.append((venue, cls.VENUE_DISPLAY_NAMES.get(venue, venue.title())))
            return found
        except Exception as e:
            print(f"  ⚠️ Error detecting today's venues: {e}")
            return []

    @classmethod
    def get_all_race_links(cls, venue_slug: str) -> List[Tuple[str, str]]:
        today = date.today().isoformat()
        url = f"{cls.BASE_URL}/racing/racecards"
        try:
            req = urllib.request.Request(url, headers=cls.HEADERS)
            html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
            pattern = rf'/racing/racecards/{today}/{venue_slug}/racecard/(\d+)/([^"\'<>\s]+)'
            return list(dict.fromkeys(re.findall(pattern, html)))
        except Exception as e:
            print(f"  ⚠️ Error getting race links for {venue_slug}: {e}")
            return []

    @classmethod
    def fetch_race(cls, venue_slug: str, race_id: str, race_slug: str, race_number: int) -> Optional[Race]:
        today = date.today().isoformat()
        url = f"{cls.BASE_URL}/racing/racecards/{today}/{venue_slug}/racecard/{race_id}/{race_slug}"
        display_name = cls.VENUE_DISPLAY_NAMES.get(venue_slug, venue_slug.title())
        try:
            req = urllib.request.Request(url, headers=cls.HEADERS)
            html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
            scripts = re.findall(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if not scripts:
                return None
            data = json.loads(scripts[0])
            race_data = data["props"]["pageProps"]["race"]
            race_summary = race_data.get("race_summary", {})
            race_name = race_summary.get("name") or race_slug.replace("-", " ").title()
            off_time = race_summary.get("time") or "00:00"

            riders = race_data.get("rides", [])
            runners = []
            for r in riders:
                if r.get("ride_status") != "RUNNER":
                    continue
                cloth = r.get("cloth_number", 0)
                draw = r.get("draw_number", cloth)
                h_obj = r.get("horse", {})
                name = h_obj.get("name", f"Runner {cloth}")
                jockey = r.get("jockey", {}).get("name", "Unknown")
                trainer = r.get("trainer", {}).get("name", "Unknown")

                try:
                    parts = r.get("handicap", "9-0").split("-")
                    weight = (int(parts[0]) * 14 + int(parts[1])) * 0.453592
                except Exception:
                    weight = 57.0

                form_text = h_obj.get("formsummary", {}).get("display_text", "5-5-5")
                days_rest = h_obj.get("last_ran_days", 30)

                history = r.get("race_history_stats", [])
                cd_winner = any(int(h.get("value", 0)) > 0 for h in history if h.get("type") in ["Course", "Distance", "Course & Distance"])

                bookie_list = r.get("bookmakerOdds", [])
                if bookie_list:
                    best = max(bookie_list, key=lambda x: x.get("decimalOdds", 0))
                    decimal_odds = float(best.get("decimalOdds", 10.0))
                else:
                    curr = r.get("betting", {}).get("current_odds", "")
                    if "/" in curr:
                        num, den = curr.split("/")
                        decimal_odds = round((float(num) / float(den)) + 1.0, 2)
                    else:
                        decimal_odds = 10.0

                try:
                    mr = int(r.get("official_rating") or 82)
                except Exception:
                    mr = 82

                j_rate = 0.20 if any(n in jockey for n in ["Fourie", "v'd Merwe", "Murray", "De Melo", "Muller", "Habib"]) else 0.14
                t_rate = 0.21 if any(n in trainer for n in ["Snaith", "Kotzen", "Marshall", "Whitehead"]) else 0.13

                runners.append(Horse(
                    number=cloth, name=name, draw=draw, merit_rating=mr,
                    jockey=jockey, trainer=trainer, weight_kg=round(weight, 1),
                    form=form_text, cd_winner=cd_winner, days_rest=days_rest,
                    bookmaker_odds=decimal_odds,
                    jockey_strike_rate=j_rate, trainer_strike_rate=t_rate
                ))

            if not runners:
                return None

            return Race(
                race_id=f"{venue_slug.upper()}-LIVE-{today}-R{race_number}",
                meeting=display_name,
                race_number=race_number,
                race_name=race_name,
                post_time=off_time[:5] if len(off_time) > 5 else off_time,
                distance_meters=1400,
                surface="Polytrack" if "poly" in venue_slug.lower() else "Turf",
                going="Standard",
                runners=runners
            )
        except Exception:
            return None

    @classmethod
    def fetch_todays_full_card(cls) -> List[Race]:
        print("🔍 Auto-detecting today's SA race meetings...")
        venues = cls.detect_todays_venues()
        all_races = []
        for venue_slug, display_name in venues:
            print(f"  ✅ Found: {display_name}")
            links = cls.get_all_race_links(venue_slug)
            for num, (rid, rslug) in enumerate(links, start=1):
                race = cls.fetch_race(venue_slug, rid, rslug, num)
                if race:
                    all_races.append(race)
        return all_races
