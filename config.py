import os
from dataclasses import dataclass

@dataclass
class Config:
    SA_TRACKS = [
        "Hollywoodbets Durbanville",
        "Hollywoodbets Greyville",
        "Turffontein",
        "Hollywoodbets Kenilworth",
        "Hollywoodbets Scottsville",
        "Fairview"
    ]

    WEIGHT_MERIT_RATING: float = 0.35
    WEIGHT_FORM: float = 0.20
    WEIGHT_COURSE_DISTANCE: float = 0.15
    WEIGHT_JOCKEY_TRAINER: float = 0.15
    WEIGHT_DRAW_BIAS: float = 0.10
    WEIGHT_WEIGHT_REST: float = 0.05

    MIN_VALUE_EDGE: float = 0.10
    LONGSHOT_MIN_ODDS: float = 8.0

    # Email Alert Settings (Primary Channel)
    ENABLE_EMAIL_ALERTS: bool = True
    TARGET_EMAIL: str = os.getenv("TARGET_EMAIL", "anilpolton@live.co.za")
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "re_T7Pmbdo3_C7D9JSz49kZpB1CNo6HN2KHq")
    EMAIL_FROM: str = "Antigravity Racing <onboarding@resend.dev>"

    # WhatsApp Settings (Disabled)
    ENABLE_WHATSAPP_ALERTS: bool = False
    WHATSAPP_MODE: str = "none"
    TARGET_PHONE_NUMBER: str = ""

config = Config()
