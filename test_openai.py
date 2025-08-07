import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\PWQ\OneDrive - QlikTech Inc\Susmit Chatterjee's Personal Folder\Personal\stock_analysis\.env", override=True)
print("API Key from env:", os.getenv("OPENAI_API_KEY"))
