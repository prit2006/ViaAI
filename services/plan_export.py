import os
from datetime import datetime


def build_plan_markdown(user_label, query, results):
    return f"""# ViaAI Travel Plan

## User
{user_label}

## Query
{query}

## Flight Information
{results['flight_results']}

## Hotel Information
{results['hotel_results']}

## Itinerary
{results['itinerary']}

## Final Plan
{results['final_response']}
"""


def save_plan(file_content, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"travel_plan_{timestamp}.md"
    save_dir = os.path.join(base_dir, "travel_plans")
    os.makedirs(save_dir, exist_ok=True)

    full_path = os.path.join(save_dir, filename)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(file_content)

    return filename, os.path.join("travel_plans", filename)
