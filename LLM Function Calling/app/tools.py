# app/tools.py

def get_weather(city: str):
    """
    Business logic function.
    - No LLM logic
    - No validation logic
    - No side effects
    """

    # In real systems, this would call a weather API
    return {
        "city": city,
        "temperature": 26,
        "condition": "Sunny"
    }


def update_ticket_status(ticket_id: str, status: str):
    """
    Enterprise action function.
    This could update a database, CRM, or ticketing system.
    """

    # Simulated database update
    return {
        "ticket_id": ticket_id,
        "status": status,
        "message": "Ticket updated successfully"
    }