from app.skills.momentum_trading_skill import MomentumTradingSkill

skill = MomentumTradingSkill()

for symbol in ["AAPL", "TSLA", "NVDA"]:
    signal = skill.analyze(symbol)
    print(signal)