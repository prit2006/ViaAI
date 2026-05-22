from langchain_core.messages import HumanMessage


AGENT_META = {
    "flight_agent": {
        "title": "Flight Agent",
        "subtitle": "Searching flight options",
        "content_key": "flight_results",
        "empty_message": "No flight data returned.",
    },
    "hotel_agent": {
        "title": "Hotel Agent",
        "subtitle": "Finding hotel context",
        "content_key": "hotel_results",
        "empty_message": "No hotel data returned.",
    },
    "itinerary_agent": {
        "title": "Itinerary Agent",
        "subtitle": "Building the itinerary",
        "content_key": "itinerary",
        "empty_message": "No itinerary generated.",
    },
    "final_agent": {
        "title": "Final Agent",
        "subtitle": "Preparing the final travel plan",
        "content_key": "final_response",
        "empty_message": "No final response returned.",
    },
}


def empty_collected_results():
    return {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0,
    }


def _content_from_update(node_name, state_update):
    meta = AGENT_META.get(node_name, {})
    content_key = meta.get("content_key")

    if content_key == "final_response":
        messages = state_update.get("messages", [])
        if not messages:
            return ""

        try:
            return messages[-1].content
        except Exception:
            return str(messages[-1])

    if content_key:
        return state_update.get(content_key, "")

    return ""


def stream_travel_plan(user_query, thread_id):
    from main import app

    config = {
        "configurable": {
            "thread_id": thread_id,
        },
    }

    graph_input = {
        "messages": [
            HumanMessage(content=user_query),
        ],
        "user_query": user_query,
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "llm_calls": 0,
    }

    for chunk in app.stream(graph_input, config=config, stream_mode="updates"):
        for node_name, state_update in chunk.items():
            meta = AGENT_META.get(
                node_name,
                {
                    "title": node_name,
                    "subtitle": "Processing",
                    "content_key": None,
                    "empty_message": "No output returned.",
                },
            )
            llm_calls = state_update.get("llm_calls")
            content = _content_from_update(node_name, state_update)

            yield {
                "node_name": node_name,
                "title": meta["title"],
                "subtitle": meta["subtitle"],
                "content_key": meta["content_key"],
                "content": content,
                "llm_calls": llm_calls,
                "empty_message": meta["empty_message"],
            }


def collect_update(collected, update):
    content_key = update.get("content_key")
    if content_key and update.get("content"):
        collected[content_key] = update["content"]

    if update.get("llm_calls") is not None:
        collected["llm_calls"] = update["llm_calls"]

    return collected
