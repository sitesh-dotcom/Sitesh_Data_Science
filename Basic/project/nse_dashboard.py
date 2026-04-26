# ══════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════

REFRESH_INTERVAL_MINUTES = 3  # Change to 5 if you get blocked by NSE

NIFTY50_HEAVYWEIGHTS = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY",
    "HINDUNILVR", "ITC", "KOTAKBANK", "LT", "SBIN",
    "BAJFINANCE", "BHARTIARTL", "AXISBANK", "ASIANPAINT", "MARUTI"
]

SECTORS = [
    "NIFTY BANK",
    "NIFTY IT",
    "NIFTY AUTO",
    "NIFTY PHARMA",
    "NIFTY FMCG",
    "NIFTY METAL",
    "NIFTY REALTY",
    "NIFTY ENERGY",
    "NIFTY INFRA",
    "NIFTY MEDIA",
    "NIFTY PSU BANK",
    "NIFTY MIDCAP 50",
]

console = Console()


# ══════════════════════════════════════════════════════════════════
#  NSE SESSION — Required to bypass NSE's anti-scraping headers
# ══════════════════════════════════════════════════════════════════

def create_session():
    """Create a requests session that mimics a browser to access NSE APIs."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.nseindia.com/",
        "DNT": "1",
    })
    # Warm up: visit the homepage to get session cookies
    try:
        session.get("https://www.nseindia.com", timeout=12)
        time.sleep(1)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not warm up NSE session: {e}[/yellow]")
    return session


# Global session — recreated if it expires
_session = create_session()


def nse_fetch(url: str, retry: bool = True):
    """
    Fetch JSON from an NSE API endpoint.
    Automatically re-initializes the session if the request fails.
    """
    global _session
    try:
        resp = _session.get(url, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        if retry:
            # Session likely expired — recreate and retry once
            _session = create_session()
            return nse_fetch(url, retry=False)
        return None


# ══════════════════════════════════════════════════════════════════
#  DATA FETCHERS
# ══════════════════════════════════════════════════════════════════

# ── 1. NIFTY PCR ─────────────────────────────────────────────────

def get_nifty_pcr():
    """
    Fetch Nifty option chain and compute Put-Call Ratio.
    PCR > 1.2 → Bullish sentiment (more puts written)
    PCR < 0.8 → Bearish sentiment (more calls written)
    """
    data = nse_fetch("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY")
    if not data:
        return None

    records = data.get("records", {}).get("data", [])
    total_ce_oi, total_pe_oi = 0, 0
    total_ce_vol, total_pe_vol = 0, 0

    for strike in records:
        if "CE" in strike:
            total_ce_oi  += strike["CE"].get("openInterest", 0)
            total_ce_vol += strike["CE"].get("totalTradedVolume", 0)
        if "PE" in strike:
            total_pe_oi  += strike["PE"].get("openInterest", 0)
            total_pe_vol += strike["PE"].get("totalTradedVolume", 0)

    pcr_oi  = round(total_pe_oi  / total_ce_oi,  2) if total_ce_oi  else 0
    pcr_vol = round(total_pe_vol / total_ce_vol, 2) if total_ce_vol else 0

    underlying = data.get("records", {}).get("underlyingValue", 0)

    return {
        "symbol": "NIFTY",
        "underlying": underlying,
        "pcr_oi": pcr_oi,
        "pcr_vol": pcr_vol,
        "total_ce_oi": total_ce_oi,
        "total_pe_oi": total_pe_oi,
        "total_ce_vol": total_ce_vol,
        "total_pe_vol": total_pe_vol,
    }


# ── 2. BANK NIFTY PCR ────────────────────────────────────────────

def get_banknifty_pcr():
    """
    Fetch Bank Nifty option chain and compute Put-Call Ratio.
    """
    data = nse_fetch("https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY")
    if not data:
        return None

    records = data.get("records", {}).get("data", [])
    total_ce_oi, total_pe_oi = 0, 0
    total_ce_vol, total_pe_vol = 0, 0

    for strike in records:
        if "CE" in strike:
            total_ce_oi  += strike["CE"].get("openInterest", 0)
            total_ce_vol += strike["CE"].get("totalTradedVolume", 0)
        if "PE" in strike:
            total_pe_oi  += strike["PE"].get("openInterest", 0)
            total_pe_vol += strike["PE"].get("totalTradedVolume", 0)

    pcr_oi  = round(total_pe_oi  / total_ce_oi,  2) if total_ce_oi  else 0
    pcr_vol = round(total_pe_vol / total_ce_vol, 2) if total_ce_vol else 0

    underlying = data.get("records", {}).get("underlyingValue", 0)

    return {
        "symbol": "BANKNIFTY",
        "underlying": underlying,
        "pcr_oi": pcr_oi,
        "pcr_vol": pcr_vol,
        "total_ce_oi": total_ce_oi,
        "total_pe_oi": total_pe_oi,
        "total_ce_vol": total_ce_vol,
        "total_pe_vol": total_pe_vol,
    }


# ── 3. ADVANCE / DECLINE ─────────────────────────────────────────

def get_advance_decline():
    """
    Fetch advance/decline data for Nifty 50, Nifty 500, and overall NSE.
    """
    data = nse_fetch("https://www.nseindia.com/api/allIndices")
    if not data:
        return []

    target_indices = {"NIFTY 50", "NIFTY 500", "NIFTY BANK", "NIFTY MIDCAP 100"}
    results = []

    for idx in data.get("data", []):
        name = idx.get("index", "")
        if name in target_indices:
            advances  = idx.get("advances", 0)
            declines  = idx.get("declines", 0)
            unchanged = idx.get("unchanged", 0)
            total = (advances or 0) + (declines or 0) + (unchanged or 0)
            adv_pct = round(advances / total * 100, 1) if total else 0
            results.append({
                "index":     name,
                "advances":  advances,
                "declines":  declines,
                "unchanged": unchanged,
                "adv_pct":   adv_pct,
                "last":      idx.get("last", 0),
                "pChange":   idx.get("percentChange", 0),
            })

    # Sort by target order
    order = list(target_indices)
    results.sort(key=lambda x: order.index(x["index"]) if x["index"] in order else 99)
    return results


# ── 4. NIFTY 50 HEAVYWEIGHTS ─────────────────────────────────────

def get_nifty50_heavyweights():
    """
    Fetch live data for top Nifty 50 heavyweight stocks.
    """
    data = nse_fetch(
        "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
    )
    if not data:
        return []

    results = []
    for stock in data.get("data", []):
        sym = stock.get("symbol", "")
        if sym in NIFTY50_HEAVYWEIGHTS:
            results.append({
                "symbol":    sym,
                "ltp":       stock.get("lastPrice", 0),
                "pChange":   stock.get("pChange", 0),
                "open":      stock.get("open", 0),
                "high":      stock.get("dayHigh", 0),
                "low":       stock.get("dayLow", 0),
                "volume":    stock.get("totalTradedVolume", 0),
            })

    # Sort by our defined order
    results.sort(
        key=lambda x: NIFTY50_HEAVYWEIGHTS.index(x["symbol"])
        if x["symbol"] in NIFTY50_HEAVYWEIGHTS else 99
    )
    return results


# ── 5. OI SPURTS (TOP OI BUILDUP) ────────────────────────────────

def get_oi_spurts():
    """
    Fetch top stocks with the highest OI buildup (long/short buildup signals).
    """
    data = nse_fetch(
        "https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings"
    )
    if not data:
        return []

    results = []
    for item in data.get("data", [])[:12]:
        oi_chg = item.get("oiChange", 0) or 0
        pchg   = item.get("pChange", 0) or 0

        # Interpret buildup signal
        if oi_chg > 0 and pchg > 0:
            signal = "[green]LONG BUILDUP[/green]"
        elif oi_chg > 0 and pchg < 0:
            signal = "[red]SHORT BUILDUP[/red]"
        elif oi_chg < 0 and pchg > 0:
            signal = "[cyan]SHORT COVER[/cyan]"
        else:
            signal = "[yellow]LONG UNWND[/yellow]"

        results.append({
            "symbol":  item.get("symbol", ""),
            "oi":      item.get("openInterest", 0),
            "oi_chg":  oi_chg,
            "ltp":     item.get("lastPrice", 0),
            "pChange": pchg,
            "signal":  signal,
        })
    return results


# ── 6. SECTOR-WISE PERFORMANCE ───────────────────────────────────

def get_sector_data():
    """
    Fetch all indices and filter for sector indices.
    """
    data = nse_fetch("https://www.nseindia.com/api/allIndices")
    if not data:
        return []

    results = []
    for idx in data.get("data", []):
        name = idx.get("index", "")
        if name in SECTORS:
            results.append({
                "sector":   name.replace("NIFTY ", ""),
                "value":    idx.get("last", 0),
                "pChange":  idx.get("percentChange", 0),
                "high":     idx.get("high", 0),
                "low":      idx.get("low", 0),
                "advances": idx.get("advances", 0),
                "declines": idx.get("declines", 0),
            })

    # Sort by % change descending
    results.sort(key=lambda x: x["pChange"] or 0, reverse=True)
    return results


# ── 7. FII / DII DATA ────────────────────────────────────────────

def get_fii_dii_data():
    """
    Fetch FII and DII participant-wise trading activity from NSE.
    This shows net buy/sell activity by Foreign and Domestic institutions.
    
    Endpoint returns data for last few trading sessions.
    """
    data = nse_fetch(
        "https://www.nseindia.com/api/fiidiiTradeReact"
    )
    if not data:
        # Fallback: try the derivatives participant data
        data = nse_fetch(
            "https://www.nseindia.com/api/participant-wise-trading-data"
        )
    if not data:
        return []

    results = []

    # The API returns a list of date-wise entries
    entries = data if isinstance(data, list) else data.get("data", [])

    for entry in entries[:5]:  # Show last 5 trading days
        try:
            trade_date = entry.get("date", entry.get("tradeDate", "N/A"))

            # FII data
            fii_buy  = float(str(entry.get("fiiBuy",  entry.get("fii_buy",  0))).replace(",", "") or 0)
            fii_sell = float(str(entry.get("fiiSell", entry.get("fii_sell", 0))).replace(",", "") or 0)
            fii_net  = round(fii_buy - fii_sell, 2)

            # DII data
            dii_buy  = float(str(entry.get("diiBuy",  entry.get("dii_buy",  0))).replace(",", "") or 0)
            dii_sell = float(str(entry.get("diiSell", entry.get("dii_sell", 0))).replace(",", "") or 0)
            dii_net  = round(dii_buy - dii_sell, 2)

            results.append({
                "date":     trade_date,
                "fii_buy":  fii_buy,
                "fii_sell": fii_sell,
                "fii_net":  fii_net,
                "dii_buy":  dii_buy,
                "dii_sell": dii_sell,
                "dii_net":  dii_net,
            })
        except Exception:
            continue

    return results


# ── 8. NIFTY 50 INDEX SUMMARY ────────────────────────────────────

def get_index_summary():
    """
    Fetch a quick summary for Nifty 50 and Bank Nifty indices.
    """
    data = nse_fetch("https://www.nseindia.com/api/allIndices")
    if not data:
        return []

    watch = {"NIFTY 50", "NIFTY BANK", "NIFTY MIDCAP 100", "INDIA VIX"}
    results = []
    for idx in data.get("data", []):
        if idx.get("index") in watch:
            results.append({
                "index":   idx.get("index"),
                "last":    idx.get("last", 0),
                "change":  idx.get("change", 0),
                "pChange": idx.get("percentChange", 0),
                "high":    idx.get("high", 0),
                "low":     idx.get("low", 0),
            })
    results.sort(key=lambda x: list(watch).index(x["index"]) if x["index"] in watch else 99)
    return results


# ══════════════════════════════════════════════════════════════════
#  HELPER RENDERERS
# ══════════════════════════════════════════════════════════════════

def pcr_sentiment(pcr: float) -> str:
    """Return colored sentiment label based on PCR value."""
    if pcr >= 1.3:
        return "[bold green]VERY BULLISH[/bold green]"
    elif pcr >= 1.0:
        return "[green]BULLISH[/green]"
    elif pcr >= 0.8:
        return "[yellow]NEUTRAL[/yellow]"
    elif pcr >= 0.6:
        return "[red]BEARISH[/red]"
    else:
        return "[bold red]VERY BEARISH[/bold red]"


def color_pct(val) -> str:
    """Return a colored percentage string."""
    try:
        v = float(val)
        sign = "▲" if v > 0 else ("▼" if v < 0 else "=")
        color = "green" if v > 0 else ("red" if v < 0 else "yellow")
        return f"[{color}]{sign} {abs(v):.2f}%[/{color}]"
    except Exception:
        return str(val)


def color_val(val, positive_is_good=True) -> str:
    """Return a colored value (green/red)."""
    try:
        v = float(val)
        if v > 0:
            color = "green" if positive_is_good else "red"
        elif v < 0:
            color = "red" if positive_is_good else "green"
        else:
            color = "yellow"
        return f"[{color}]{v:,.2f}[/{color}]"
    except Exception:
        return str(val)


def fmt_cr(val) -> str:
    """Format a value in crores (divide by 10,000,000)."""
    try:
        v = float(val) / 1e7
        return f"₹{v:,.2f} Cr"
    except Exception:
        return str(val)


def fmt_num(val) -> str:
    """Format a large number with commas."""
    try:
        return f"{int(val):,}"
    except Exception:
        return str(val)


# ══════════════════════════════════════════════════════════════════
#  DASHBOARD RENDERER
# ══════════════════════════════════════════════════════════════════

def build_dashboard():
    """
    Fetch all data and render the full terminal dashboard.
    Returns a list of Rich renderables to print.
    """
    now = datetime.now().strftime("%d %b %Y  %H:%M:%S")
    renderables = []

    # ── HEADER ────────────────────────────────────────────────────
    header = Text(justify="center")
    header.append("  🇮🇳  NSE LIVE MARKET DASHBOARD  ", style="bold white on dark_blue")
    header.append(f"  ⏱  {now}  ", style="bold yellow on grey15")
    renderables.append(Panel(Align.center(header), box=box.DOUBLE_EDGE,
                              border_style="bright_blue", padding=(0, 2)))

    # ── STATUS ────────────────────────────────────────────────────
    now_time = datetime.now().time()
    market_open = datetime.strptime("09:15", "%H:%M").time()
    market_close = datetime.strptime("15:30", "%H:%M").time()
    if market_open <= now_time <= market_close:
        status_txt = "[bold green]● MARKET OPEN[/bold green]"
    else:
        status_txt = "[bold red]● MARKET CLOSED[/bold red] (Showing last available data)"
    renderables.append(Align.center(Text.from_markup(status_txt)))
    renderables.append(Rule(style="bright_blue"))

    # ══════════════════════════════════════════════════
    # SECTION 1: INDEX SUMMARY
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup("\n[bold bright_cyan]📊  INDEX SUMMARY[/bold bright_cyan]"))
    indices = get_index_summary()
    if indices:
        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold bright_white on grey23",
                  expand=False, pad_edge=True)
        t.add_column("Index",   style="bold cyan", min_width=20)
        t.add_column("LTP",     justify="right", min_width=12)
        t.add_column("Change",  justify="right", min_width=12)
        t.add_column("% Chg",   justify="right", min_width=10)
        t.add_column("High",    justify="right", min_width=12)
        t.add_column("Low",     justify="right", min_width=12)

        for idx in indices:
            chg = idx["pChange"] or 0
            t.add_row(
                idx["index"],
                f"{idx['last']:,.2f}",
                color_val(idx["change"]),
                color_pct(chg),
                f"{idx['high']:,.2f}",
                f"{idx['low']:,.2f}",
            )
        renderables.append(t)
    else:
        renderables.append(Text.from_markup("  [yellow]Could not fetch index data[/yellow]"))

    # ══════════════════════════════════════════════════
    # SECTION 2: PCR — NIFTY & BANK NIFTY SIDE BY SIDE
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup("\n[bold bright_cyan]📈  PUT-CALL RATIO (PCR)[/bold bright_cyan]"))

    nifty_pcr = get_nifty_pcr()
    bnf_pcr   = get_banknifty_pcr()

    pcr_panels = []

    for pcr_data, label in [(nifty_pcr, "NIFTY"), (bnf_pcr, "BANK NIFTY")]:
        if pcr_data:
            p = pcr_data["pcr_oi"]
            sentiment = pcr_sentiment(p)
            color = "green" if p >= 1 else "red"
            content = (
                f"[bold]PCR (OI)  :[/bold]  [{color}]{p}[/{color}]  →  {sentiment}\n"
                f"[bold]PCR (Vol) :[/bold]  {pcr_data['pcr_vol']}\n"
                f"[bold]Spot      :[/bold]  {pcr_data['underlying']:,.2f}\n\n"
                f"[bold]Total CE OI :[/bold]  {fmt_num(pcr_data['total_ce_oi'])}\n"
                f"[bold]Total PE OI :[/bold]  {fmt_num(pcr_data['total_pe_oi'])}\n"
                f"[bold]CE Vol      :[/bold]  {fmt_num(pcr_data['total_ce_vol'])}\n"
                f"[bold]PE Vol      :[/bold]  {fmt_num(pcr_data['total_pe_vol'])}"
            )
            pcr_panels.append(
                Panel(content, title=f"[bold white]{label}[/bold white]",
                      border_style="bright_blue", padding=(1, 2))
            )
        else:
            pcr_panels.append(
                Panel("[yellow]Data unavailable[/yellow]",
                      title=f"[bold white]{label}[/bold white]",
                      border_style="dim")
            )

    # PCR Legend
    legend = (
        "[green]PCR > 1.2[/green] Very Bullish  "
        "[green]1.0–1.2[/green] Bullish  "
        "[yellow]0.8–1.0[/yellow] Neutral  "
        "[red]0.6–0.8[/red] Bearish  "
        "[bold red]< 0.6[/bold red] Very Bearish"
    )
    renderables.append(Columns(pcr_panels, equal=True))
    renderables.append(Text.from_markup(f"  ℹ  {legend}"))

    # ══════════════════════════════════════════════════
    # SECTION 3: ADVANCE / DECLINE
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup(
        "\n[bold bright_cyan]📊  ADVANCE / DECLINE BREADTH[/bold bright_cyan]"
    ))
    ad_data = get_advance_decline()
    if ad_data:
        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold bright_white on grey23", expand=False)
        t.add_column("Index",      style="bold cyan", min_width=22)
        t.add_column("▲ Advances", justify="right", style="green")
        t.add_column("▼ Declines", justify="right", style="red")
        t.add_column("= Unchanged",justify="right", style="yellow")
        t.add_column("Adv%",       justify="right")
        t.add_column("Index Value",justify="right")
        t.add_column("% Chg",      justify="right")

        for row in ad_data:
            t.add_row(
                row["index"],
                str(row["advances"]),
                str(row["declines"]),
                str(row["unchanged"]),
                f"[green]{row['adv_pct']}%[/green]",
                f"{row['last']:,.2f}",
                color_pct(row["pChange"]),
            )
        renderables.append(t)
    else:
        renderables.append(Text.from_markup("  [yellow]Could not fetch advance/decline data[/yellow]"))

    # ══════════════════════════════════════════════════
    # SECTION 4: NIFTY 50 HEAVYWEIGHTS
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup(
        "\n[bold bright_cyan]🏋️  NIFTY 50 HEAVYWEIGHTS[/bold bright_cyan]"
    ))
    hw = get_nifty50_heavyweights()
    if hw:
        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold bright_white on grey23", expand=False)
        t.add_column("Symbol", style="bold cyan", min_width=14)
        t.add_column("LTP",    justify="right", min_width=10)
        t.add_column("Open",   justify="right", min_width=10)
        t.add_column("High",   justify="right", min_width=10)
        t.add_column("Low",    justify="right", min_width=10)
        t.add_column("% Chg",  justify="right", min_width=10)
        t.add_column("Volume", justify="right", min_width=14)

        for s in hw:
            t.add_row(
                s["symbol"],
                f"{s['ltp']:,.2f}",
                f"{s['open']:,.2f}",
                f"{s['high']:,.2f}",
                f"{s['low']:,.2f}",
                color_pct(s["pChange"]),
                fmt_num(s["volume"]),
            )
        renderables.append(t)
    else:
        renderables.append(Text.from_markup("  [yellow]Could not fetch heavyweights data[/yellow]"))

    # ══════════════════════════════════════════════════
    # SECTION 5: OI SPURTS
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup(
        "\n[bold bright_cyan]🔥  OI SPURTS — TOP 12 BUILDUP SIGNALS[/bold bright_cyan]"
    ))
    oi_data = get_oi_spurts()
    if oi_data:
        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold bright_white on grey23", expand=False)
        t.add_column("Symbol",     style="bold cyan", min_width=14)
        t.add_column("LTP",        justify="right", min_width=10)
        t.add_column("% Chg",      justify="right", min_width=10)
        t.add_column("Open Int.",  justify="right", min_width=14)
        t.add_column("OI Chg%",   justify="right", min_width=10)
        t.add_column("Signal",     min_width=16)

        for s in oi_data:
            t.add_row(
                s["symbol"],
                f"{s['ltp']:,.2f}",
                color_pct(s["pChange"]),
                fmt_num(s["oi"]),
                color_pct(s["oi_chg"]),
                s["signal"],
            )
        renderables.append(t)
        renderables.append(Text.from_markup(
            "  [dim]Signal Logic: Price↑ + OI↑ = Long Buildup | "
            "Price↓ + OI↑ = Short Buildup | "
            "Price↑ + OI↓ = Short Covering | "
            "Price↓ + OI↓ = Long Unwinding[/dim]"
        ))
    else:
        renderables.append(Text.from_markup("  [yellow]Could not fetch OI spurt data[/yellow]"))

    # ══════════════════════════════════════════════════
    # SECTION 6: SECTOR-WISE PERFORMANCE
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup(
        "\n[bold bright_cyan]🏭  SECTOR-WISE PERFORMANCE[/bold bright_cyan]"
    ))
    sector_data = get_sector_data()
    if sector_data:
        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold bright_white on grey23", expand=False)
        t.add_column("Sector",     style="bold cyan", min_width=16)
        t.add_column("Value",      justify="right", min_width=12)
        t.add_column("% Chg",      justify="right", min_width=10)
        t.add_column("High",       justify="right", min_width=12)
        t.add_column("Low",        justify="right", min_width=12)
        t.add_column("▲ Adv",      justify="right", style="green")
        t.add_column("▼ Dec",      justify="right", style="red")

        for s in sector_data:
            t.add_row(
                s["sector"],
                f"{s['value']:,.2f}",
                color_pct(s["pChange"]),
                f"{s['high']:,.2f}",
                f"{s['low']:,.2f}",
                str(s["advances"] or "-"),
                str(s["declines"] or "-"),
            )
        renderables.append(t)
    else:
        renderables.append(Text.from_markup("  [yellow]Could not fetch sector data[/yellow]"))

    # ══════════════════════════════════════════════════
    # SECTION 7: FII / DII ACTIVITY
    # ══════════════════════════════════════════════════
    renderables.append(Text.from_markup(
        "\n[bold bright_cyan]🏦  FII / DII TRADING ACTIVITY (Last 5 Sessions)[/bold bright_cyan]"
    ))
    fii_dii = get_fii_dii_data()
    if fii_dii:
        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold bright_white on grey23", expand=False)
        t.add_column("Date",      style="bold cyan", min_width=14)
        t.add_column("FII Buy",   justify="right", style="green",  min_width=16)
        t.add_column("FII Sell",  justify="right", style="red",    min_width=16)
        t.add_column("FII Net",   justify="right",                 min_width=16)
        t.add_column("DII Buy",   justify="right", style="green",  min_width=16)
        t.add_column("DII Sell",  justify="right", style="red",    min_width=16)
        t.add_column("DII Net",   justify="right",                 min_width=16)

        for row in fii_dii:
            t.add_row(
                str(row["date"]),
                fmt_cr(row["fii_buy"]),
                fmt_cr(row["fii_sell"]),
                color_val(row["fii_net"]),
                fmt_cr(row["dii_buy"]),
                fmt_cr(row["dii_sell"]),
                color_val(row["dii_net"]),
            )
        renderables.append(t)
        renderables.append(Text.from_markup(
            "  [dim]Values in ₹ Crores. "
            "[green]FII Net > 0[/green] = Foreign buying (Bullish). "
            "[red]FII Net < 0[/red] = Foreign selling (Bearish). "
            "DII often acts as counter-party to FII.[/dim]"
        ))
    else:
        renderables.append(
            Panel(
                "[yellow]FII/DII data is published by NSE after market hours.\n"
                "It may not be available during live market hours.\n\n"
                "Manual check: [link]https://www.nseindia.com/reports-indices-derivatives/"
                "equity-market-fii-dii-activity[/link][/yellow]",
                title="[bold]FII / DII[/bold]",
                border_style="yellow"
            )
        )

    # ── FOOTER ────────────────────────────────────────────────────
    renderables.append(Rule(style="bright_blue"))
    renderables.append(Text.from_markup(
        f"  [dim]Auto-refresh every {REFRESH_INTERVAL_MINUTES} min  |  "
        "Press [bold]Ctrl+C[/bold] to exit  |  "
        "Data source: NSE India public APIs  |  "
        "⚠ For educational purposes only. Not financial advice.[/dim]"
    ))

    return renderables


# ══════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════

def run_dashboard():
    """Clear the console and print the full dashboard."""
    console.clear()
    try:
        items = build_dashboard()
        for item in items:
            console.print(item)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        console.print(f"\n[bold red]Error rendering dashboard:[/bold red] {e}")
        console.print("[yellow]Will retry on next refresh...[/yellow]")


def main():
    console.print(Panel(
        "[bold cyan]🚀 Starting NSE Live Market Dashboard...[/bold cyan]\n"
        "[dim]Initializing NSE session and fetching data. Please wait...[/dim]",
        border_style="bright_blue"
    ))
    time.sleep(2)

    # First render
    run_dashboard()

    # Schedule auto-refresh
    schedule.every(REFRESH_INTERVAL_MINUTES).minutes.do(run_dashboard)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Dashboard stopped. Goodbye! 👋[/bold yellow]")


if __name__ == "__main__":
    main()



