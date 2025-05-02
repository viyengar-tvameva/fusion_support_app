from prometheus_client import Counter

tickets_created = Counter("tickets_created", "Number of tickets created")
tickets_resolved = Counter("tickets_resolved", "Number of tickets resolved")
tickets_escalated = Counter("tickets_escalated", "Number of tickets escalated")

def increment_tickets_created():
    tickets_created.inc()

def increment_tickets_resolved():
    tickets_resolved.inc()

def increment_tickets_escalated():
    tickets_escalated.inc()
