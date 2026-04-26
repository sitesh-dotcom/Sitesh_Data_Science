# market_analyzer.py
def analyze_nifty_pro_v4(pcr, vix, adv, decl, sectors, heavyweights):
    print("\n" + "="*50)
    print("      SITESH'S DECISIVE TRADING DASHBOARD      ")
    print("="*50)

    # 1. SECTOR STATUS TABLE (The missing part!)
    print(f"{'SECTOR STATUS':<20} | {'STATE':<10}")
    print("-" * 35)
    score = 0
    
# Financials (High Weightage)
    fin_state = "🟢 GREEN" if sectors.get("Financials") else "🔴 RED"
    print(f"{'Financials (35%)':<20} | {fin_state}")
    if sectors.get("Financials"): score += 3
    
    # IT and Energy
    for s_name in ["IT", "Energy"]:
        s_state = "🟢 GREEN" if sectors.get(s_name) else "🔴 RED"
        print(f"{s_name + ' (~11%)':<20} | {s_state}")
        if sectors.get(s_name): score += 1
    
    print("-" * 50)

    # 2. MARKET DATA
    risk_mode = "LOW" if vix < 15 else "MODERATE" if vix < 22 else "HIGH (PANIC)"
    ad_ratio = round(adv / decl, 2) if decl > 0 else adv
    hw_up = sum(1 for up in heavyweights.values() if up)

    print(f"VOLATILITY : {vix} ({risk_mode})")
    print(f"BREADTH    : {adv} Adv / {decl} Decl (Ratio: {ad_ratio})")
    print(f"DERIVATIVE : PCR at {pcr}")
    print(f"WEIGHTS    : {hw_up}/7 Heavyweights Green")
    print("-" * 50)

    # 3. DECISIVE SIGNALS
    if pcr > 1.15 and score >= 4 and ad_ratio > 1.5:
        signal = "🔥 STRONG BUY"
        exit_rule = "EXIT if Financials turn 🔴 RED"
    elif pcr < 0.85 and score <= 1 and ad_ratio < 0.6:
        signal = "🚨 STRONG SELL"
        exit_rule = "EXIT if Financials turn 🟢 GREEN"
    elif score >= 4 and ad_ratio < 0.8:
        signal = "⚠️ BULL TRAP: Heavyweights up, but market is weak"
        exit_rule = "Avoid Longs"
    else:
        signal = "⏳ NEUTRAL / SCALP ONLY"
        exit_rule = "Wait for Sector Alignment"

    print(f"SIGNAL     : {signal}")
    print(f"EXIT RULE  : {exit_rule}")
    print("="*50 + "\n")

# --- UPDATE THESE MANUALLY FROM NSE ---
sector_data = {
    "Financials": False,  # If Nifty Bank is Red, set to False
    "IT": True, 
    "Energy": True
}

heavyweight_data = {
    "HDFCBANK": False, "RELIANCE": True, 
    "ICICIBANK": False, "INFY": True, "BHARTIARTL": True,
    "SBIN": True, "LT": True
}

# Run the Analysis
analyze_nifty_pro_v4(
    pcr=0.95, vix=15.2, adv=20, decl=30, 
    sectors=sector_data, heavyweights=heavyweight_data
)

