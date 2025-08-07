def compute_yoy_change(df, column):
    """
    Compute year-over-year percentage change for a given column,
    assuming quarterly data with 4 periods in a year.
    """
    if df[column].dtype != "object":
        df[f"{column}_YoY_%"] = df[column].pct_change(periods=4, fill_method=None) * 100
    return df

def add_all_yoy(df):
    """
    Compute YoY percentage changes for all numeric columns except 'Date'.
    """
    for col in df.columns:
        if col != "Date" and df[col].dtype != "object":
            df = compute_yoy_change(df, col)
    return df

def add_income_statement_ratios(df):
    """
    Add financial ratios to the income statement DataFrame.
    Gross Margin = Gross Profit / Total Revenue
    Net Margin = Net Income / Total Revenue
    """
    if "Total Revenue" in df.columns and "Gross Profit" in df.columns:
        df["Gross_Margin"] = df["Gross Profit"] / df["Total Revenue"]

    if "Total Revenue" in df.columns and "Net Income" in df.columns:
        df["Net_Margin"] = df["Net Income"] / df["Total Revenue"]

    return df

def add_cash_flow_ratios(df):
    """
    Add Free Cash Flow column to cash flow DataFrame.
    Free Cash Flow = Operating Cash Flow - Capital Expenditures
    """
    if "Total Cash From Operating Activities" in df.columns and "Capital Expenditures" in df.columns:
        df["Free_Cash_Flow"] = df["Total Cash From Operating Activities"] - df["Capital Expenditures"]

    return df
