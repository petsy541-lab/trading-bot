from app.risk import SurvivalWallet


def test_wallet_stops_trading_when_empty():
    wallet = SurvivalWallet(balance=0.0)
    assert wallet.can_trade() is False
    assert wallet.dead is True


def test_wallet_does_not_allow_risk_above_caps():
    wallet = SurvivalWallet(balance=1000.0, max_risk_fraction=0.02, max_position_fraction=0.10)
    assert wallet.max_risk_amount() == 20.0
    assert wallet.max_trade_amount() == 100.0
    assert wallet.risk_is_allowed(50.0) is True
    assert wallet.risk_is_allowed(150.0) is False
