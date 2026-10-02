from app.bot import TradingBot
from app.config import BotConfig


def main():
    config = BotConfig(
        starting_balance=10000.0,
        max_risk_fraction=0.02,
        max_position_fraction=0.10,
        max_drawdown_fraction=0.25,
        demo_mode=True,
        live_mode=False,
        min_trade_value=50.0,
    )
    bot = TradingBot(config)
    bot.run(steps=25)


if __name__ == "__main__":
    main()
