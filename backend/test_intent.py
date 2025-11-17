# python backend/test_intent.py
import os
from dotenv import load_dotenv
load_dotenv()

from backend.LLM.router import resolve_intent

def show(q: str):
    intent = resolve_intent(q)
    print("RAW INPUT:", q)
    print("PARSED ACTION:", intent.action)
    print("PARSED PARAMS:", intent.params.model_dump())

if __name__ == "__main__":
    # try a few messages
    show("get top 5 anomalies in the past week")
<<<<<<< HEAD
    show("rerun with 15 features")
    show("why is IP 10.0.0.7 anomalous? verbose explanation")
=======
    show("get top 5 anomalies for last week")
    show("get top 5 anomalies for today")
    show("get top 5 anomalies from this tuesday to thursday")
    show("get top 10 anomalies for last month")
    show("rerun with 15 features")
    show("why is IP 10.0.0.7 anomalous? explanation")
    show("show me some anomalies")
    show("give me a summary for last month")
>>>>>>> frontend
