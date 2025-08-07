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
    ax.bar(labels, scores, color=['#1f77b4','#ff7f0e','#2ca02c'])
    ax.set_ylim(0, 10)
    ax.set_ylabel('Score (0-10)')
    ax.set_title(title)
    st.pyplot(fig)

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
            st.dataframe(bs_df)
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

        # Show detailed breakdowns
        st.subheader("Financial Health Breakdown")
        st.json(fh_breakdown)

        st.subheader("Buffett Score Breakdown")
        st.json(buffett_breakdown)

        st.subheader("Lynch Score Breakdown")
        st.json(lynch_breakdown)

        # Local simple recommendation
        rec = simple_recommendation(overall_fh_score)
        st.markdown(f"### Simple Recommendation: **{rec}**")

        # GPT prompt with explicit buy/hold/sell request
        gpt_prompt = f"""
        Analyze the company {ticker} based on the provided financial scores and breakdowns.
        Provide a detailed investment analysis covering strengths, weaknesses, risks, and opportunities.
        Conclude with a clear recommendation: should an investor BUY, HOLD, or SELL the stock as of today, considering all financial aspects?

        Financial Health Score: {overall_fh_score:.2f}/10
        Buffett Score: {overall_buffett_score:.2f}/10
        Lynch Score: {overall_lynch_score:.2f}/10

        Balance Sheet Breakdown:
        {fh_breakdown}

        Buffett Breakdown:
        {buffett_breakdown}

        Lynch Breakdown:
        {lynch_breakdown}
        """

        with st.spinner("Getting GPT financial analysis..."):
            gpt_analysis = get_financial_summary(
                gpt_prompt,
                overall_fh_score,
                fh_breakdown,
                overall_buffett_score,
                buffett_breakdown,
                overall_lynch_score,
                lynch_breakdown,
            )

        st.subheader("GPT Analysis Summary")
        st.text_area("GPT Investment Analysis", gpt_analysis, height=300)

if __name__ == "__main__":
    main()
