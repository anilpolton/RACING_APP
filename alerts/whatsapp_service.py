from models import RaceAnalysis

class WhatsAppAlertService:
    """
    Text & email layout formatter for race predictions, Place Accumulators, and hunch checks.
    """

    def format_prediction_alert(self, analysis: RaceAnalysis) -> str:
        race = analysis.race
        top = analysis.top_pick
        val = analysis.best_value_bet

        stars = "⭐" * top.confidence_stars
        prob_pct = f"{top.win_probability * 100:.1f}%"
        total_runners = len(race.runners)

        lines = [
            "🏇 *ANTIGRAVITY RACE PREDICTION*",
            f"📍 *{race.meeting}* - Race {race.race_number} ({race.post_time})",
            f"🏆 {race.race_name}",
            f"📏 {race.distance_meters}m | Surface: {race.surface} ({race.going})",
            f"👥 *Field Size:* {total_runners} Declared Runners",
            "-----------------------------------------------",
            f"🥇 *TOP PICK:* #{top.horse.number} *{top.horse.name}*",
            f"   • Win Probability: *{prob_pct}* (Rank 1 of {total_runners})",
            f"   • Confidence: {stars}",
            f"   • Jockey/Trainer: {top.horse.jockey} / {top.horse.trainer}",
            f"   • Bookie Odds: {top.bookmaker_odds:.2f} (Fair: {top.fair_odds_decimal:.2f})",
        ]

        if val and val.horse.number != top.horse.number:
            val_prob_pct = f"{val.win_probability * 100:.1f}%"
            edge_pct = f"+{val.expected_value * 100:.1f}%"
            lines.extend([
                "",
                f"💎 *VALUE BET ALERT:* #{val.horse.number} *{val.horse.name}*",
                f"   • Bookie Odds: *{val.bookmaker_odds:.2f}* (Fair: {val.fair_odds_decimal:.2f})",
                f"   • Model Probability: {val_prob_pct}",
                f"   • Expected Value Edge: *{edge_pct}* (Overpriced!)"
            ])

        lines.append("")
        lines.append("📊 *Top Contenders:*")
        for i, p in enumerate(analysis.predictions[:3], start=1):
            h = p.horse
            lines.append(f"   {i}. #{h.number} {h.name} — {p.win_probability*100:.1f}% (Odds: {p.bookmaker_odds:.2f})")

        trifecta_str = ", ".join(f"#{num}" for num in analysis.recommended_trifecta)
        lines.extend([
            "",
            f"🎯 *RECOMMENDED TRIFECTA BOX:* [{trifecta_str}]",
            "-----------------------------------------------",
            "⚡ _Powered by Antigravity Predictive Analytics_"
        ])

        return "\n".join(lines)

    def format_pa_alert(self, ticket, all_race_analyses=None) -> str:
        lines = [
            "🎟️ *ANTIGRAVITY PLACE ACCUMULATOR (PA) & FULL RACE CARD*",
            f"📍 *{ticket.meeting}*",
            f"🏆 Total Legs in PA: {len(ticket.legs)} Races",
            "----------------------------------------------------------",
        ]

        if all_race_analyses:
            pa_race_numbers = {leg.race_number for leg in ticket.legs}
            lines.append("📋 *FULL DAY CARD OVERVIEW (ALL RACES):*")
            for analysis in all_race_analyses:
                r = analysis.race
                top = analysis.top_pick.horse
                prob = analysis.top_pick.win_probability * 100
                is_pa = r.race_number in pa_race_numbers

                pa_tag = "🎯 [PA LEG]" if is_pa else "   [Non-PA]"
                lines.append(
                    f"{pa_tag} Race {r.race_number} ({r.post_time}): {r.race_name[:32]} "
                    f"| Top: #{top.number} {top.name} ({prob:.0f}%)"
                )
            lines.append("----------------------------------------------------------")

        lines.append("🎫 *OPTIMIZED PLACE ACCUMULATOR PICKS (7 LEGS):*")
        for leg in ticket.legs:
            sel_str = ", ".join(f"#{num}" for num in leg.selections)
            names_str = " / ".join(leg.horse_names)
            lines.append(f"• Leg {leg.leg_number} (Race {leg.race_number}): [{sel_str}] {names_str}")
            if leg.is_banker:
                lines.append(f"    ↳ {leg.note}")
            else:
                lines.append(f"    ↳ _{leg.note}_")

        lines.extend([
            "----------------------------------------------------------",
            f"📊 *Total Combinations:* {ticket.total_combinations} lines",
            f"💰 *Ticket Cost:*",
            f"   • R{ticket.cost_100:.2f} for 100% Payout",
            f"   • R{ticket.cost_50:.2f} for 50% Payout",
            f"   • R{ticket.cost_25:.2f} for 25% Payout",
            "----------------------------------------------------------",
            "⚡ _Optimized by Antigravity Exotics Engine_"
        ])
        return "\n".join(lines)
