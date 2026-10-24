from dataclasses import dataclass
from typing import List
from models import RaceAnalysis

@dataclass
class ExoticLeg:
    leg_number: int
    race_number: int
    selections: List[int]
    horse_names: List[str]
    is_banker: bool
    note: str

@dataclass
class ExoticTicket:
    bet_type: str
    meeting: str
    legs: List[ExoticLeg]
    total_combinations: int
    cost_100: float
    cost_50: float
    cost_25: float

class ExoticsEngine:
    """
    Builds optimized multi-race exotic wagers (Place Accumulator, Pick 6, Jackpot).
    Uses Harville approximation to estimate place probability and applies banker logic.
    """

    @classmethod
    def generate_place_accumulator_ticket(cls, meeting: str, leg_analyses: List[RaceAnalysis]) -> ExoticTicket:
        legs: List[ExoticLeg] = []
        total_combos = 1

        for i, analysis in enumerate(leg_analyses, start=1):
            preds = analysis.predictions
            top = preds[0]
            top_place_prob = cls.estimate_place_probability(top.win_probability, len(preds))

            # Banker threshold: >= 65% place probability or 5 stars
            if top_place_prob >= 0.65 or top.confidence_stars >= 5:
                picks = [top.horse.number]
                names = [top.horse.name]
                is_banker = True
                note = f"🔒 BANKER ({int(top_place_prob*100)}% Top-3 Probability)"
            else:
                # Coverage spread: Top pick + Best overlay or second favorite
                picks = [top.horse.number]
                names = [top.horse.name]
                if len(preds) > 1:
                    picks.append(preds[1].horse.number)
                    names.append(preds[1].horse.name)
                # Add third runner if field is wide open
                if len(preds) > 2 and preds[0].win_probability < 0.22:
                    picks.append(preds[2].horse.number)
                    names.append(preds[2].horse.name)
                is_banker = False
                note = "Spread Leg (Upset cover)"

            legs.append(ExoticLeg(
                leg_number=i,
                race_number=analysis.race.race_number,
                selections=picks,
                horse_names=names,
                is_banker=is_banker,
                note=note
            ))
            total_combos *= len(picks)

        return ExoticTicket(
            bet_type="Place Accumulator",
            meeting=meeting,
            legs=legs,
            total_combinations=total_combos,
            cost_100=float(total_combos),
            cost_50=round(total_combos * 0.50, 2),
            cost_25=round(total_combos * 0.25, 2)
        )

    @classmethod
    def estimate_place_probability(cls, win_prob: float, field_size: int) -> float:
        """Harville model approximation for top-3 finish probability."""
        p1 = win_prob
        rem = 1.0 - p1
        p2 = rem * (p1 / max(0.01, 1.0 - (1.0 / field_size))) * 0.75
        p3 = rem * (p1 / max(0.01, 1.0 - (2.0 / field_size))) * 0.55
        return min(0.95, p1 + p2 + p3)
