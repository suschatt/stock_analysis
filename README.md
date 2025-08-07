# Stock Analysis Project 📈

This project is a comprehensive financial analysis tool that fetches stock data, computes various financial health scores, and leverages AI-powered analysis to provide investment insights and recommendations.

---

✨ Features
  * Data Fetching: Gathers quarterly financial data (Balance Sheet, Income Statement, Cash Flow) for any given stock ticker using the yfinance library.
  * Financial Scoring: Calculates multiple financial health scores to evaluate a company's performance, including:
  * A Full Financial Health Score for an overall view.
  * A Buffett-Style Score based on principles of value investing.
  * A Peter Lynch-Style Score focusing on growth at a reasonable price.
  * AI-Powered Analysis: Generates a detailed investment summary and a buy/hold/sell recommendation using OpenAI's GPT model.
  * User-Friendly Interface: Supports a simple command-line interface and can be extended into an interactive Streamlit dashboard with data visualizations.
  * Modular Design: The project is organized into separate modules for data fetching, scoring, AI integration, and visualization, making it easy to understand and extend.

## 🛠️ Requirements

- **Python 3.8+**
- The following Python packages (install with `pip install -r requirements.txt`):
    - `yfinance`
    - `pandas`
    - `openai`
    - `python-dotenv`
    - `matplotlib`
    - `streamlit` (optional, for the dashboard)

---

## 🚀 Setup & Usage

### 1. Clone the Repository

```bash
git clone <repository_url>
cd stock-analysis-project 
```

Configure Your OpenAI API Key  
Create a file named `.env` in the root directory of the project and add your OpenAI API key to it:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ Note: Keep your .env file secure and never commit it to a public repository.

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the Streamlit Dashboard
   ```bash
   streamlit run app.py
   ```





5. Run the Streamlit Dashboard (Optional)
If you prefer a visual interface, you can run the Streamlit dashboard:

Bash

streamlit run app.py
📁 Project Structure

```bash
stock-analysis-project/
├── main.py               # Main script to run financial analysis and GPT summary
├── data_fetcher.py       # Fetches financial data from Yahoo Finance
├── score.py              # Calculates financial health scores
├── buffett_score.py      # Buffett-style financial scoring logic
├── lynch.py              # Peter Lynch-style financial scoring logic
├── gpt_summary.py        # Interacts with OpenAI GPT for the analysis summary
├── visualize.py          # Contains plotting functions for financial trends
├── app.py                # Streamlit dashboard implementation
├── .env                  # Environment variables (OpenAI API key)
├── requirements.txt      # Python dependencies
└── README.md             # This README file
```

📝 Notes
The accuracy of scores and analysis is dependent on the quality and availability of financial data from yfinance.

You can customize the scoring logic and the GPT prompt in their respective modules to fit your specific investment criteria.

This project is for informational purposes only and does not constitute financial advice.

📄 License
This project is licensed under the MIT License.

Developed by Susmit Chatterjee 👨‍💻
