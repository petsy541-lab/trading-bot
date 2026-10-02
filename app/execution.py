from __future__ import annotations

from app.models import MarketSnapshot, StrategyDecision


class EventAwareStrategy:
    def evaluate(self, snapshot: MarketSnapshot) -> StrategyDecision:
        feature_score = snapshot.trend + snapshot.sentiment + snapshot.event_bias
        score = max(-1.0, min(1.0, feature_score / 1.5))

        if score > 0.35:
            action = "BUY"
            reason = "Positive macro and trend signal across market and event pressures."
        elif score < -0.35:
            action = "SELL"
            reason = "Negative momentum and event stress are dominating the market."
        else:
            action = "HOLD"
            reason = "Insufficient conviction for directional risk; holding capital."

        return StrategyDecision(
            action=action,
            confidence=abs(score),
            signal_score=score,
            reason=reason,
        )


class MultiStrategySelector:
    def __init__(self):
        self.trend = EventAwareStrategy()

    def choose(self, snapshot: MarketSnapshot) -> StrategyDecision:
        return self.trend.evaluate(snapshot)
