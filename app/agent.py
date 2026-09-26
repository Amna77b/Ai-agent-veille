import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.tools import fetch_articles, fetch_articles_multi, send_email_report

load_dotenv()


def build_agent():
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

    tools = [fetch_articles, fetch_articles_multi, send_email_report]

    agent = create_react_agent(llm, tools)
    return agent