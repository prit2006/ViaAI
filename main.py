import os
from typing import TypedDict, Annotated
import operator

import psycopg

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# =========================
# LLM
# =========================
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# =========================
# STATE
# =========================
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

# =========================
# FLIGHT AGENT
# =========================
def flight_agent(state: TravelState):

    query = state["user_query"]

    try:
        flight_data = search_flights(query)

    except Exception as e:
        flight_data = f"Flight search error: {str(e)}"

    return {
        "flight_results": str(flight_data),
        "messages": [
            AIMessage(content="Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# HOTEL AGENT
# =========================
def hotel_agent(state: TravelState):

    query = f"Best hotels for {state['user_query']}"

    try:
        hotel_results = tavily_search(query)

    except Exception as e:
        hotel_results = f"Hotel search error: {str(e)}"

    return {
        "hotel_results": str(hotel_results),
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# ITINERARY AGENT
# =========================
def itinerary_agent(state: TravelState):

    prompt = f"""
Create a detailed travel itinerary.

USER QUERY:
{state['user_query']}

FLIGHT RESULTS:
{state['flight_results']}

HOTEL RESULTS:
{state['hotel_results']}

Include:
1. Best flight suggestion
2. Best hotel suggestion
3. Day-wise itinerary
4. Estimated budget
5. Travel tips
"""

    response = llm.invoke([
        SystemMessage(
            content="You are an expert AI travel planner."
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# FINAL RESPONSE AGENT
# =========================
def final_agent(state: TravelState):

    final_prompt = f"""
Generate a clean final travel response.

Flights:
{state['flight_results']}

Hotels:
{state['hotel_results']}

Itinerary:
{state['itinerary']}

Format properly with headings and bullet points.
"""

    response = llm.invoke([
        SystemMessage(
            content="You are a professional travel assistant."
        ),
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# BUILD GRAPH
# =========================
graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)

# =========================
# POSTGRES CHECKPOINTER FIX
# =========================

# IMPORTANT:
# autocommit=True fixes:
# CREATE INDEX CONCURRENTLY cannot run inside transaction block

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True
)

checkpointer = PostgresSaver(_conn)

# Setup database tables
checkpointer.setup()

# Compile graph
app = graph.compile(
    checkpointer=checkpointer
)

# =========================
# MAIN
# =========================
if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "Prit"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\n========================")
    print("FINAL RESPONSE")
    print("========================\n")

    for msg in result["messages"]:
        print(msg.content)
        print("\n------------------------\n")


