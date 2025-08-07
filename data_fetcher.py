import yfinance as yf
import pandas as pd

# === BALANCE SHEET ===
def get_balance_sheet_data(ticker_symbol, num_quarters=8):
    """
    Fetches and prepares quarterly balance sheet data for the given ticker.
    Calculates Debt to Equity, Current Ratio, and Cash to Assets if possible.
    """
    stock = yf.Ticker(ticker_symbol)
    df = stock.quarterly_balance_sheet.T
    df = _prepare_df(df, num_quarters)

    if df is not None:
        # Liabilities & Equity columns to look for
        liab_cols = ["Total Liab", "Total Liabilities Net Minority Interest", "Total Liabilities"]
        equity_cols = ["Total Stockholder Equity", "Total Equity Gross Minority Interest", "Ordinary Shares Number"]

        liab_col = next((col for col in liab_cols if col in df.columns), None)
        equity_col = next((col for col in equity_cols if col in df.columns), None)

        if liab_col and equity_col:
            df["Debt_to_Equity"] = df[liab_col] / df[equity_col]

        if "Total Current Assets" in df.columns and "Total Current Liabilities" in df.columns:
            df["Current_Ratio"] = df["Total Current Assets"] / df["Total Current Liabilities"]

        if "Cash" in df.columns and "Total Assets" in df.columns:
            df["Cash_to_Assets"] = df["Cash"] / df["Total Assets"]

        # Standardize important column names if missing
        if "Total Assets" not in df.columns:
            for col in ["Total Asset", "TotalAssets"]:
                if col in df.columns:
                    df.rename(columns={col: "Total Assets"}, inplace=True)

    return df


# === INCOME STATEMENT ===
def get_income_statement_data(ticker_symbol, num_quarters=8):
    """
    Fetches and prepares quarterly income statement data for the given ticker.
    Standardizes key column names for consistency.
    """
    stock = yf.Ticker(ticker_symbol)
    df = stock.quarterly_financials.T
    df = _prepare_df(df, num_quarters)

    if df is not None:
        # Standardize column names
        if "Total Revenue" not in df.columns:
            for col in ["TotalRevenue", "Revenues"]:
                if col in df.columns:
                    df.rename(columns={col: "Total Revenue"}, inplace=True)

        if "Gross Profit" not in df.columns:
            for col in ["GrossProfit"]:
                if col in df.columns:
                    df.rename(columns={col: "Gross Profit"}, inplace=True)

        if "Net Income" not in df.columns:
            for col in ["NetIncome", "Net Income Applicable To Common Shares"]:
                if col in df.columns:
                    df.rename(columns={col: "Net Income"}, inplace=True)

    return df


# === CASH FLOW ===
def get_cash_flow_data(ticker_symbol, num_quarters=8):
    """
    Fetches and prepares quarterly cash flow data for the given ticker.
    Calculates Free Cash Flow if missing.
    Standardizes column names.
    """
    stock = yf.Ticker(ticker_symbol)
    df = stock.quarterly_cashflow.T
    df = _prepare_df(df, num_quarters)

    if df is not None:
        # Add Free Cash Flow if missing and data available
        if "Free Cash Flow" not in df.columns:
            if "Total Cash From Operating Activities" in df.columns and "Capital Expenditures" in df.columns:
                df["Free Cash Flow"] = df["Total Cash From Operating Activities"] - abs(df["Capital Expenditures"])

        # Standardize capital expenditure column name
        if "Capital Expenditure" not in df.columns:
            for col in ["Capital Expenditures", "CapitalExpenditures"]:
                if col in df.columns:
                    df.rename(columns={col: "Capital Expenditure"}, inplace=True)

    return df


# === Shared Preparation Function ===
def _prepare_df(df, num_quarters):
    """
    Prepares raw dataframes by:
    - Converting index to datetime
    - Sorting descending by date and trimming to required quarters
    - Sorting ascending for logical presentation
    - Resetting index and renaming 'index' to 'Date'
    """
    if df.empty:
        return None
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=False).head(num_quarters)
    df = df.sort_index()
    df = df.reset_index().rename(columns={"index": "Date"})
    return df
