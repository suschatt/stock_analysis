import streamlit as st
from data_fetcher import get_balance_sheet_data, get_income_statement_data, get_cash_flow_data
from score import score_full_company
from buffett_score import score_buffett_company
from lynch import score_lynch_company
from gpt_summary import get_financial_summary
import pandas as pd
import matplotlib.pyplot as plt

def simple_recommendation(score):
    if score >= 7.5:
        return "BUY"
    elif score >= 5.0:
        return "HOLD"
    else:
        return "SELL"

def plot_scores(title, scores_dict):
    labels = list(scores_dict.keys())
    scores = [scores_dict[k] for k in labels]
    fig, ax = plt.subplots()
    bars = ax.bar(labels, scores, color=['#1f77b4','#ff7f0e','#2ca02c'])
    ax.set_ylim(0, 10)
    ax.set_ylabel('Score (0-10)')
    ax.set_title(title)
    
    # Add score labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            f'{height:.2f}',
            ha='center',
            va='bottom'
        )
    
    st.pyplot(fig)

def format_to_billions_with_dollar(df, cols):
    def to_billions(x):
        if pd.isna(x):
            return ""
        return f"${x / 1e9:.2f}B"
    for col in cols:
        if col in df.columns:
            df[col] = df[col].apply(to_billions)
    return df

def main():
    st.title("Financial Health Dashboard")

    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)").upper()

    if ticker:
        # Fetch data
        bs_df = get_balance_sheet_data(ticker)
        is_df = get_income_statement_data(ticker)
        cf_df = get_cash_flow_data(ticker)

        st.subheader("Balance Sheet Data")
        if bs_df is not None and not bs_df.empty:
            # Columns to format - adjust as per your actual columns
            cols_to_format = [
                "Total Assets", "Total Liab", "Total Stockholder Equity", "Cash", "Long Term Debt",
                "Debt_to_Equity", "Current_Ratio", "Cash_to_Assets"
            ]
            formatted_bs_df = format_to_billions_with_dollar(bs_df.copy(), cols_to_format)
            st.table(formatted_bs_df)
        else:
            st.write("No relevant Balance Sheet data available.")

        st.subheader("Income Statement Data")
        if is_df is not None and not is_df.empty:
            st.dataframe(is_df)
        else:
            st.write("No relevant Income Statement data available.")

        st.subheader("Cash Flow Data")
        if cf_df is not None and not cf_df.empty:
            st.dataframe(cf_df)
        else:
            st.write("No relevant Cash Flow data available.")

        # Scores
        overall_fh_score, fh_breakdown = score_full_company(bs_df, is_df, cf_df)
        overall_buffett_score, buffett_breakdown = score_buffett_company(bs_df, is_df, cf_df)
        overall_lynch_score, lynch_breakdown = score_lynch_company(bs_df, is_df, cf_df)

        st.subheader("Scores Summary")
        scores_dict = {
            "Financial Health": overall_fh_score,
            "Buffett": overall_buffett_score,
            "Lynch": overall_lynch_score,
        }
        plot_scores("Company Financial Scores", scores_dict)

        # Local simple recommendation
        rec = simple_recommendation(overall_fh_score)
        st.markdown(f"### Simple Recommendation: **{rec}**")

        # New GPT prompt (independent analysis + technical analysis)
        gpt_prompt = f"""
        You are an expert financial analyst. Conduct an independent due diligence analysis on the company {ticker}.
        Consider fundamental financial health and also perform a technical analysis of the stock's recent market trends.
        Provide a detailed investment analysis covering strengths, weaknesses, risks, and opportunities.
        Conclude with a clear recommendation: BUY, HOLD, or SELL as of today.
        """

        with st.spinner("Getting GPT financial analysis..."):
            gpt_analysis = get_financial_summary(gpt_prompt)

        # Debug output to verify GPT response
        if not gpt_analysis:
            st.error("GPT returned an empty response.")
        else:
            st.write("GPT raw output:")
            st.write(gpt_analysis)

        st.subheader("GPT Analysis Summary")
        st.text_area("GPT Investment Analysis", gpt_analysis, height=400)

if __name__ == "__main__":
    main()
