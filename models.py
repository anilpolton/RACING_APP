from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Horse:
    number: int
    name: str
    draw: int
    merit_rating: int
    jockey: str
    trainer: str
    weight_kg: float
    form: str
    cd_winner: bool
    days_rest: int
    bookmaker_odds: float
    jockey_strike_rate: float = 0.15
    trainer_strike_rate: float = 0.15

@dataclass
class Race:
    race_id: str
    meeting: str
    race_number: int
    race_name: str
    post_time: str
    distance_meters: int
    surface: str
    going: str
    runners: List[Horse]

@dataclass
class PredictionResult:
    horse: Horse
    fundamental_score: float
    win_probability: float
    fair_odds_decimal: float
    bookmaker_odds: float
    expected_value: float
    is_value_bet: bool
    is_top_pick: bool
    confidence_stars: int

@dataclass
class RaceAnalysis:
    race: Race
    predictions: List[PredictionResult]
    top_pick: PredictionResult
    best_value_bet: Optional[PredictionResult]
    recommended_trifecta: List[int]
