from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def create_service_now_ticket(issue_description):
    with tracer.start_as_current_span("create_service_now_ticket") as span:
        span.set_attribute("issue.description", issue_description)
        response = {"ticket_id": "SN12345", "status": "created"}
        span.set_attribute("service_now.ticket_id", response["ticket_id"])
        return response

def update_service_now_ticket(ticket_id, status):
    with tracer.start_as_current_span("update_service_now_ticket") as span:
        span.set_attribute("ticket.id", ticket_id)
        span.set_attribute("ticket.status", status)
        return {"ticket_id": ticket_id, "status": status}
