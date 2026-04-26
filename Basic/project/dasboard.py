from nsepython import *
import pandas as pd
def get_nifty_dashboard():
    # Fetch Nifty Spot
    nifty_spot = nse_quote_ltp("NIFTY 50")
    
    # Fetch Option Chain
    payload = nse_optionchain_scrapper("NIFTY")
    
    # PCR Calculation
    total_pe_oi = payload['filtered']['PE']['totOI']
    total_ce_oi = payload['filtered']['CE']['totOI']
    pcr = round(total_pe_oi / total_ce_oi, 2)
    
    # Identify Reasonable Call Options (Premiums between 50 and 150)
    # This filter helps find the 'Sweet Spot' for scalpers
    ce_data = []
    for item in payload['filtered']['data']:
        strike = item['strikePrice']
        if 'CE' in item:
            ltp = item['CE']['lastPrice']
            if 50 <= ltp <= 180: # Filter for 'Reasonable' premiums
                ce_data.append({"Strike": strike, "LTP": ltp, "Type": "CE"})
    
    # Output
    print(f"\nNIFTY SPOT: {nifty_spot}")
    print(f"PCR: {pcr} ({'🟢 BULLISH' if pcr > 1 else '🔴 BEARISH' if pcr < 0.7 else '🟡 NEUTRAL'})\n")
    print("REASONABLE CALL OPTIONS FOR TODAY:")
    print(pd.DataFrame(ce_data))

get_nifty_dashboard()
from nsepython import nse_fiidii
print(nse_fiidii())