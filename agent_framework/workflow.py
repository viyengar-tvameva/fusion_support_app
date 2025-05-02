from opentelemetry import trace
from metrics.ticket_metrics import increment_tickets_created, increment_tickets_resolved, increment_tickets_escalated

tracer = trace.get_tracer(__name__)

def create_ticket(agent_id, issue_description):
    with tracer.start_as_current_span("create_ticket") as span:
        span.set_attribute("agent.id", agent_id)
        span.set_attribute("issue.description", issue_description)
        increment_tickets_created()
        return {"ticket_id": "12345", "status": "created"}

def resolve_ticket(ticket_id):
    with tracer.start_as_current_span("resolve_ticket") as span:
        span.set_attribute("ticket.id", ticket_id)
        increment_tickets_resolved()
        return {"ticket_id": ticket_id, "status": "resolved"}

def escalate_ticket(ticket_id):
    with tracer.start_as_current_span("escalate_ticket") as span:
        span.set_attribute("ticket.id", ticket_id)
        increment_tickets_escalated()
        return {"ticket_id": ticket_id, "status": "escalated"}
