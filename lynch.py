def safe_num(val):
    """Convert None or NaN to 0, otherwise return the number."""
    try:
        if val is None:
            return 0
        if isinstance(val, (int, float)):
            return val
        return float(val)
    except:
        return 0

def score_lynch_company(bs_df, is_df, cf_df, price=None):
    """
    Calculates a Peter Lynch-style score based on PEG ratio, EPS growth,
    debt-to-equity, dividend yield + growth, and net cash position.
    Missing values are handled gracefully.
    """
    breakdown = {}
    score = 0
    metrics_count = 0

    # EPS Growth %
    eps_growth_value = None
    if is_df is not None and "Net Income" in is_df.columns:
        try:
            first_eps = safe_num(is_df["Net Income"].iloc[0])
            last_eps = safe_num(is_df["Net Income"].iloc[-1])
            if first_eps != 0:
                eps_growth_value = ((last_eps - first_eps) / abs(first_eps)) * 100
        except:
            eps_growth_value = None

    eps_growth_score = 3
    if eps_growth_value is not None:
        if eps_growth_value >= 20:
            eps_growth_score = 10
        elif eps_growth_value >= 10:
            eps_growth_score = 7
        elif eps_growth_value >= 5:
            eps_growth_score = 5
        elif eps_growth_value > 0:
            eps_growth_score = 4
        else:
            eps_growth_score = 1

    breakdown["EPS Growth %"] = {"value": eps_growth_value, "score": eps_growth_score}
    score += eps_growth_score
    metrics_count += 1

    # PEG Ratio
    peg_ratio_value = None
    peg_ratio_score = 3
    if price is not None and is_df is not None and "Net Income" in is_df.columns and "Total Revenue" in is_df.columns:
        try:
            latest_eps = safe_num(is_df["Net Income"].iloc[-1]) / safe_num(is_df["Total Revenue"].iloc[-1])  # Approx EPS
            if latest_eps > 0 and eps_growth_value and eps_growth_value > 0:
                pe_ratio = price / latest_eps
                peg_ratio_value = pe_ratio / eps_growth_value
                if peg_ratio_value < 1:
                    peg_ratio_score = 10
                elif peg_ratio_value < 2:
                    peg_ratio_score = 7
                else:
                    peg_ratio_score = 3
        except:
            pass
    breakdown["PEG Ratio"] = {"value": peg_ratio_value, "score": peg_ratio_score}
    score += peg_ratio_score
    metrics_count += 1

    # Debt-to-Equity
    debt_to_equity_value = None
    if bs_df is not None and "Debt_to_Equity" in bs_df.columns:
        debt_to_equity_value = safe_num(bs_df["Debt_to_Equity"].iloc[-1])
    debt_to_equity_score = 3
    if debt_to_equity_value is not None:
        if debt_to_equity_value < 0.5:
            debt_to_equity_score = 10
        elif debt_to_equity_value < 1:
            debt_to_equity_score = 7
        elif debt_to_equity_value < 2:
            debt_to_equity_score = 5
        else:
            debt_to_equity_score = 1
    breakdown["Debt-to-Equity"] = {"value": debt_to_equity_value, "score": debt_to_equity_score}
    score += debt_to_equity_score
    metrics_count += 1

    # Dividend Yield + Growth (placeholder; requires dividend data)
    div_yield_growth_value = None
    div_yield_growth_score = 3
    breakdown["Dividend Yield + Growth"] = {"value": div_yield_growth_value, "score": div_yield_growth_score}
    score += div_yield_growth_score
    metrics_count += 1

    # Net Cash Position
    net_cash_value = None
    if bs_df is not None and "Cash" in bs_df.columns and "Total Liab" in bs_df.columns:
        cash = safe_num(bs_df["Cash"].iloc[-1])
        liab = safe_num(bs_df["Total Liab"].iloc[-1])
        net_cash_value = cash - liab
    net_cash_score = 3
    if net_cash_value is not None:
        if net_cash_value > 0:
            net_cash_score = 10
        elif net_cash_value > -1e9:
            net_cash_score = 5
        else:
            net_cash_score = 1
    breakdown["Net Cash Position"] = {"value": net_cash_value, "score": net_cash_score}
    score += net_cash_score
    metrics_count += 1

    overall_score = score / metrics_count if metrics_count else 0
    return overall_score, breakdown
