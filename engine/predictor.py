import math
from typing import List, Optional
from models import Horse, Race, PredictionResult, RaceAnalysis
from config import config

class QuantitativePredictor:
    """
    3-Tier Quantitative Horse Racing Engine:
    - Tier 1: Fundamentals scoring (MR, Form recency, C&D, Jockey/Trainer strike rate, Draw bias)
    - Tier 2: Multinomial Logit (Softmax) conversion to win probabilities summing to 100%
    - Tier 3: Market Expected Value (EV) overlay identifying overpriced overlays
    """

    def analyze_race(self, race: Race) -> RaceAnalysis:
        raw_scores = [self._score_fundamentals(h, race) for h in race.runners]
        probabilities = self._softmax(raw_scores)

        results: List[PredictionResult] = []
        for horse, prob in zip(race.runners, probabilities):
            fair_odds = round(1.0 / prob, 2) if prob > 0 else 999.0
            ev = round((prob * horse.bookmaker_odds) - 1.0, 4)
            is_val = (ev >= config.MIN_VALUE_EDGE)

            if prob >= 0.30:
                stars = 5
            elif prob >= 0.22:
                stars = 4
            elif prob >= 0.16:
                stars = 3
            elif prob >= 0.10:
                stars = 2
            else:
                stars = 1

            results.append(PredictionResult(
                horse=horse,
                fundamental_score=round(raw_scores[len(results)], 3),
                win_probability=round(prob, 4),
                fair_odds_decimal=fair_odds,
                bookmaker_odds=horse.bookmaker_odds,
                expected_value=ev,
                is_value_bet=is_val,
                is_top_pick=False,
                confidence_stars=stars
            ))

        results.sort(key=lambda x: x.win_probability, reverse=True)
        results[0].is_top_pick = True

        value_bets = [r for r in results if r.is_value_bet]
        best_value = max(value_bets, key=lambda x: x.expected_value) if value_bets else None

        trifecta = [results[0].horse.number, results[1].horse.number, results[2].horse.number]

        return RaceAnalysis(
            race=race,
            predictions=results,
            top_pick=results[0],
            best_value_bet=best_value,
            recommended_trifecta=trifecta
        )

    def _score_fundamentals(self, horse: Horse, race: Race) -> float:
        # 1. Merit Rating score (normalized 60 to 110)
        mr_norm = max(0.0, min(1.0, (horse.merit_rating - 60.0) / 50.0))

        # 2. Form Recency score (e.g. 1-2-1-3)
        form_score = self._parse_form(horse.form)

        # 3. C&D bonus
        cd_score = 1.0 if horse.cd_winner else 0.4

        # 4. Jockey & Trainer strike rate
        jt_score = min(1.0, (horse.jockey_strike_rate * 2.5 + horse.trainer_strike_rate * 2.5) / 2.0)

        # 5. Draw Bias
        field_size = len(race.runners)
        draw_score = 1.0 - (float(horse.draw - 1) / max(1.0, float(field_size - 1))) * 0.3

        # 6. Weight & Layoff rest factor
        rest_score = 1.0 if 14 <= horse.days_rest <= 45 else (0.8 if horse.days_rest <= 90 else 0.6)

        total = (
            config.WEIGHT_MERIT_RATING * mr_norm +
            config.WEIGHT_FORM * form_score +
            config.WEIGHT_COURSE_DISTANCE * cd_score +
            config.WEIGHT_JOCKEY_TRAINER * jt_score +
            config.WEIGHT_DRAW_BIAS * draw_score +
            config.WEIGHT_WEIGHT_REST * rest_score
        )
        return total * 3.5

    def _parse_form(self, form_str: str) -> float:
        cleaned = [c for c in form_str if c.isdigit()]
        if not cleaned:
            return 0.5
        weights = [1.0, 0.7, 0.5, 0.3]
        total_weight = 0.0
        weighted_sum = 0.0
        for i, pos_char in enumerate(reversed(cleaned[-4:])):
            w = weights[i] if i < len(weights) else 0.2
            pos = int(pos_char)
            score = 1.0 if pos == 1 else (0.8 if pos == 2 else (0.6 if pos == 3 else (0.4 if pos == 4 else 0.15)))
            weighted_sum += score * w
            total_weight += w
        return weighted_sum / total_weight if total_weight > 0 else 0.5

    def _softmax(self, scores: List[float]) -> List[float]:
        exp_scores = [math.exp(s) for s in scores]
        sum_exp = sum(exp_scores)
        return [s / sum_exp for s in exp_scores]
