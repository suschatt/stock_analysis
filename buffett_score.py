import numpy as np
from utils import format_metric

def score_buffett_company(bs_df, is_df, cf_df):
    """
    Calculates a Buffett-style investment score based on profitability, 
    capital efficiency, and margin of safety.
    """
    breakdown = {}

    # Owner Earnings = Net Income + Depreciation & Amortization - CapEx
    ni = is_df["Net Income"].iloc[-1] if "Net Income" in is_df.columns else None
    da = is_df["Depreciation"].iloc[-1] if "Depreciation" in is_df.columns else None
    capex = cf_df["Capital Expenditures"].iloc[-1] if "Capital Expenditures" in cf_df.columns else None
    owner_earnings = None
    if ni is not None and da is not None and capex is not None:
        owner_earnings = ni + da - abs(capex)

    roe = None
    if "Total Stockholder Equity" in bs_df.columns and bs_df["Total Stockholder Equity"].iloc[-1] != 0:
        roe = ni / bs_df["Total Stockholder Equity"].iloc[-1]

    roic = None
    if "Total Assets" in bs_df.columns and "Total Liabilities Net Minority Interest" in bs_df.columns:
        invested_capital = bs_df["Total Assets"].iloc[-1] - bs_df["Total Liabilities Net Minority Interest"].iloc[-1]
        roic = ni / invested_capital if invested_capital != 0 else None

    debt_to_equity = bs_df["Debt_to_Equity"].iloc[-1] if "Debt_to_Equity" in bs_df.columns else None
    eps_growth = None  # placeholder unless EPS history is available

    fcff = cf_df["Free Cash Flow"].iloc[-1] if "Free Cash Flow" in cf_df.columns else None
    gross_margin = (is_df["Gross Profit"].iloc[-1] / is_df["Total Revenue"].iloc[-1]) if "Gross Profit" in is_df.columns else None
    net_margin = (is_df["Net Income"].iloc[-1] / is_df["Total Revenue"].iloc[-1]) if "Net Income" in is_df.columns else None

    breakdown.update({
        "Owner Earnings": {"value": format_metric(owner_earnings, is_currency=True), "score": _score_positive(owner_earnings)},
        "ROE": {"value": format_metric(roe, is_percentage=True), "score": _score_range(roe, 0.15, 0.25)},
        "ROIC": {"value": format_metric(roic, is_percentage=True), "score": _score_range(roic, 0.15, 0.25)},
        "Debt-to-Equity": {"value": format_metric(debt_to_equity), "score": _score_inverse_range(debt_to_equity, 0, 2)},
        "EPS Growth": {"value": format_metric(eps_growth, is_percentage=True), "score": _score_range(eps_growth, 0.05, 0.15) if eps_growth else 3},
        "FCFF": {"value": format_metric(fcff, is_currency=True), "score": _score_positive(fcff)},
        "Gross Margin": {"value": format_metric(gross_margin, is_percentage=True), "score": _score_range(gross_margin, 0.4, 0.6)},
        "Net Margin": {"value": format_metric(net_margin, is_percentage=True), "score": _score_range(net_margin, 0.1, 0.3)}
    })

    overall_score = np.nanmean([v["score"] for v in breakdown.values()])
    return overall_score, breakdown


# === SCORING HELPERS ===
def _score_range(val, low, high):
    if val is None or np.isnan(val):
        return 3
    if val < low:
        return max(0, 10 * (val / low))
    if val > high:
        return 10
    return 5 + 5 * ((val - low) / (high - low))

def _score_inverse_range(val, low, high):
    if val is None or np.isnan(val):
        return 3
    if val < low:
        return 10
    if val > high:
        return max(0, 10 - (10 * (val - high) / high))
    return 10 - (5 * ((val - low) / (high - low)))

def _score_positive(val):
    if val is None or np.isnan(val):
        return 3
    return 10 if val > 0 else 0
import numpy as np

def score_buffett(bs_df, is_df, cf_df):
    """
    Calculate Buffett-style score based on core investment metrics.
    Returns:
        overall_score (float), breakdown (dict)
    """
    breakdown = {}

    # --- Owner Earnings ---
    try:
        op_cf = cf_df["Free Cash Flow"].iloc[-1]
        capex = cf_df.get("Capital Expenditure", [0]).iloc[-1] if "Capital Expenditure" in cf_df else 0
        owner_earnings = op_cf - capex
        breakdown["Owner Earnings"] = {"value": owner_earnings, "score": _score_positive(owner_earnings)}
    except Exception:
        breakdown["Owner Earnings"] = {"value": None, "score": 3}

    # --- ROE ---
    try:
        net_income = is_df["Net Income"].iloc[-1]
        equity = bs_df["Total Stockholder Equity"].iloc[-1]
        roe = net_income / equity if equity else None
        breakdown["ROE"] = {"value": roe, "score": _score_percentage(roe)}
    except Exception:
        breakdown["ROE"] = {"value": None, "score": 3}

    # --- ROIC ---
    try:
        invested_capital = bs_df["Total Assets"].iloc[-1] - bs_df["Total Current Liabilities"].iloc[-1]
        roic = net_income / invested_capital if invested_capital else None
        breakdown["ROIC"] = {"value": roic, "score": _score_percentage(roic)}
    except Exception:
        breakdown["ROIC"] = {"value": None, "score": 3}

    # --- Debt-to-Equity ---
    try:
        total_liab = bs_df["Total Liabilities"].iloc[-1]
        equity = bs_df["Total Stockholder Equity"].iloc[-1]
        dte = total_liab / equity if equity else None
        breakdown["Debt-to-Equity"] = {"value": dte, "score": _score_inverse(dte)}
    except Exception:
        breakdown["Debt-to-Equity"] = {"value": None, "score": 3}

    # --- EPS Growth ---
    try:
        eps_latest = is_df["Net Income"].iloc[-1] / is_df["Basic Average Shares"].iloc[-1]
        eps_old = is_df["Net Income"].iloc[-5] / is_df["Basic Average Shares"].iloc[-5]
        eps_growth = (eps_latest - eps_old) / abs(eps_old)
        breakdown["EPS Growth"] = {"value": eps_growth, "score": _score_growth(eps_growth)}
    except Exception:
        breakdown["EPS Growth"] = {"value": None, "score": 3}

    # --- FCFF ---
    try:
        fcff = cf_df["Free Cash Flow"].iloc[-1]
        breakdown["FCFF"] = {"value": fcff, "score": _score_positive(fcff)}
    except Exception:
        breakdown["FCFF"] = {"value": None, "score": 3}

    # --- Gross Margin ---
    try:
        gross_margin = is_df["Gross Profit"].iloc[-1] / is_df["Total Revenue"].iloc[-1]
        breakdown["Gross Margin"] = {"value": gross_margin, "score": _score_percentage(gross_margin)}
    except Exception:
        breakdown["Gross Margin"] = {"value": None, "score": 3}

    # --- Net Margin ---
    try:
        net_margin = is_df["Net Income"].iloc[-1] / is_df["Total Revenue"].iloc[-1]
        breakdown["Net Margin"] = {"value": net_margin, "score": _score_percentage(net_margin)}
    except Exception:
        breakdown["Net Margin"] = {"value": None, "score": 3}

    # Calculate overall
    overall_score = np.mean([m["score"] for m in breakdown.values() if m["score"] is not None])
    return overall_score, breakdown


# -------------------------
# Scoring helper functions
# -------------------------
def _score_positive(val):
    if val is None:
        return 3
    return 10 if val > 0 else 0

def _score_percentage(val):
    if val is None:
        return 3
    if val >= 0.20:
        return 10
    elif val >= 0.10:
        return 7
    elif val >= 0.05:
        return 5
    elif val >= 0:
        return 3
    else:
        return 0

def _score_inverse(val):
    if val is None:
        return 3
    if val <= 0.5:
        return 10
    elif val <= 1:
        return 7
    elif val <= 2:
        return 5
    else:
        return 3

def _score_growth(val):
    if val is None:
        return 3
    if val >= 0.15:
        return 10
    elif val >= 0.05:
        return 7
    elif val > 0:
        return 5
    else:
        return 0
