def score_full_company(bs_df, is_df, cf_df):
    """
    Scores the company financial health by calculating:
    - Balance Sheet metrics and score
    - Income Statement metrics and score
    - Cash Flow metrics and score
    Returns overall score and a detailed breakdown dictionary.
    """

    # === Balance Sheet Metrics ===
    balance_sheet_metrics = {}

    # Example metrics (replace with your actual calculations):
    # Liquidity: current ratio = current assets / current liabilities
    if bs_df is not None and "Current_Ratio" in bs_df.columns:
        liquidity_val = bs_df["Current_Ratio"].iloc[-1]
        liquidity_score = score_liquidity(liquidity_val)  # define your scoring functions
    else:
        liquidity_val, liquidity_score = None, 3  # default low score

    balance_sheet_metrics["Liquidity"] = {"value": liquidity_val, "score": liquidity_score}

    # Leverage: Debt to Equity ratio (inverse is better)
    if bs_df is not None and "Debt_to_Equity" in bs_df.columns:
        leverage_val = bs_df["Debt_to_Equity"].iloc[-1]
        leverage_score = score_leverage(leverage_val)
    else:
        leverage_val, leverage_score = None, 3

    balance_sheet_metrics["Leverage"] = {"value": leverage_val, "score": leverage_score}

    # Asset Quality (example placeholder)
    asset_quality_val, asset_quality_score = None, 3
    balance_sheet_metrics["Asset Quality"] = {"value": asset_quality_val, "score": asset_quality_score}

    # Cash Safety (Cash to Assets)
    if bs_df is not None and "Cash_to_Assets" in bs_df.columns:
        cash_safety_val = bs_df["Cash_to_Assets"].iloc[-1]
        cash_safety_score = score_cash_safety(cash_safety_val)
    else:
        cash_safety_val, cash_safety_score = None, 3

    balance_sheet_metrics["Cash Safety"] = {"value": cash_safety_val, "score": cash_safety_score}

    # Retained Earnings Growth (example)
    retained_earnings_growth_val, retained_earnings_growth_score = None, 3
    balance_sheet_metrics["Retained Earnings Growth"] = {"value": retained_earnings_growth_val, "score": retained_earnings_growth_score}

    # Equity Strength (example)
    equity_strength_val, equity_strength_score = None, 3
    balance_sheet_metrics["Equity Strength"] = {"value": equity_strength_val, "score": equity_strength_score}

    balance_sheet_score = average_scores(balance_sheet_metrics)

    # === Income Statement Metrics ===
    income_statement_metrics = {}

    # Revenue Growth
    rev_growth_val, rev_growth_score = None, 3
    if is_df is not None and "Total Revenue" in is_df.columns:
        rev_growth_val = pct_change(is_df["Total Revenue"])
        rev_growth_score = score_revenue_growth(rev_growth_val)
    income_statement_metrics["Revenue Growth"] = {"value": rev_growth_val, "score": rev_growth_score}

    # Gross Margin
    gross_margin_val, gross_margin_score = None, 3
    if is_df is not None and "Gross Profit" in is_df.columns and "Total Revenue" in is_df.columns:
        gross_margin_val = is_df["Gross Profit"].iloc[-1] / is_df["Total Revenue"].iloc[-1]
        gross_margin_score = score_gross_margin(gross_margin_val)
    income_statement_metrics["Gross Margin"] = {"value": gross_margin_val, "score": gross_margin_score}

    # Net Margin
    net_margin_val, net_margin_score = None, 3
    if is_df is not None and "Net Income" in is_df.columns and "Total Revenue" in is_df.columns:
        net_margin_val = is_df["Net Income"].iloc[-1] / is_df["Total Revenue"].iloc[-1]
        net_margin_score = score_net_margin(net_margin_val)
    income_statement_metrics["Net Margin"] = {"value": net_margin_val, "score": net_margin_score}

    # Net Income Growth
    net_income_growth_val, net_income_growth_score = None, 3
    if is_df is not None and "Net Income" in is_df.columns:
        net_income_growth_val = pct_change(is_df["Net Income"])
        net_income_growth_score = score_net_income_growth(net_income_growth_val)
    income_statement_metrics["Net Income Growth"] = {"value": net_income_growth_val, "score": net_income_growth_score}

    # Earnings Quality (example placeholder)
    earnings_quality_val, earnings_quality_score = None, 3
    income_statement_metrics["Earnings Quality"] = {"value": earnings_quality_val, "score": earnings_quality_score}

    income_statement_score = average_scores(income_statement_metrics)

    # === Cash Flow Metrics ===
    cash_flow_metrics = {}

    # FCF Positivity
    fcf_positivity_val, fcf_positivity_score = None, 3
    if cf_df is not None and "Free Cash Flow" in cf_df.columns:
        fcf_positivity_val = cf_df["Free Cash Flow"].iloc[-1]
        fcf_positivity_score = score_positive_fcf(fcf_positivity_val)
    cash_flow_metrics["FCF Positivity"] = {"value": fcf_positivity_val, "score": fcf_positivity_score}

    # FCF Growth (example)
    fcf_growth_val, fcf_growth_score = None, 3
    cash_flow_metrics["FCF Growth"] = {"value": fcf_growth_val, "score": fcf_growth_score}

    # FCF to Revenue
    fcf_to_revenue_val, fcf_to_revenue_score = None, 3
    cash_flow_metrics["FCF to Revenue"] = {"value": fcf_to_revenue_val, "score": fcf_to_revenue_score}

    # Operating Cash Flow Positivity (example)
    op_cf_positivity_val, op_cf_positivity_score = None, 3
    cash_flow_metrics["OpCF Positivity"] = {"value": op_cf_positivity_val, "score": op_cf_positivity_score}

    # CapEx Discipline (example)
    capex_discipline_val, capex_discipline_score = None, 3
    cash_flow_metrics["CapEx Discipline"] = {"value": capex_discipline_val, "score": capex_discipline_score}

    cash_flow_score = average_scores(cash_flow_metrics)

    # === Overall Score ===
    overall_score = (balance_sheet_score + income_statement_score + cash_flow_score) / 3

    breakdown = {
        "Balance Sheet Score": balance_sheet_score,
        "Income Statement Score": income_statement_score,
        "Cash Flow Score": cash_flow_score,
        "Balance Sheet Breakdown": balance_sheet_metrics,
        "Income Statement Breakdown": income_statement_metrics,
        "Cash Flow Breakdown": cash_flow_metrics,
    }

    return overall_score, breakdown


# Helper functions (implement your scoring logic here)
def pct_change(series):
    if series is None or len(series) < 2:
        return None
    try:
        return ((series.iloc[-1] - series.iloc[-2]) / abs(series.iloc[-2])) * 100
    except Exception:
        return None

def average_scores(metrics_dict):
    scores = [v["score"] for v in metrics_dict.values() if v["score"] is not None]
    if not scores:
        return 3.0  # default low score if no data
    return sum(scores) / len(scores)

def score_liquidity(val):
    if val is None:
        return 3.0
    if val >= 2:
        return 10
    if val >= 1.5:
        return 7
    return 3

def score_leverage(val):
    if val is None:
        return 3.0
    if val < 0.5:
        return 10
    if val < 1:
        return 7
    if val < 2:
        return 5
    return 3

def score_cash_safety(val):
    if val is None:
        return 3.0
    if val > 0.1:
        return 10
    if val > 0.05:
        return 7
    return 3

def score_revenue_growth(val):
    if val is None:
        return 3.0
    if val > 10:
        return 10
    if val > 5:
        return 7
    return 3

def score_gross_margin(val):
    if val is None:
        return 3.0
    if val > 0.4:
        return 10
    if val > 0.2:
        return 7
    return 3

def score_net_margin(val):
    if val is None:
        return 3.0
    if val > 0.2:
        return 10
    if val > 0.1:
        return 7
    return 3

def score_net_income_growth(val):
    if val is None:
        return 3.0
    if val > 10:
        return 10
    if val > 5:
        return 7
    return 3

def score_positive_fcf(val):
    if val is None:
        return 3.0
    if val > 0:
        return 10
    return 3
