from dataclasses import dataclass


@dataclass
class BotConfig:
    starting_balance: float = 10000.0
    max_risk_fraction: float = 0.02
    max_position_fraction: float = 0.10
    max_drawdown_fraction: float = 0.25
    demo_mode: bool = True
    live_mode: bool = False
    min_trade_value: float = 50.0
    symbols: list[str] = None

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "USOIL", "NGAS"]
