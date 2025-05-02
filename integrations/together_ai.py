from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def suggest_resolution(issue_description):
    with tracer.start_as_current_span("suggest_resolution") as span:
        span.set_attribute("issue.description", issue_description)
        response = {"suggestion": "Restart the system."}
        span.set_attribute("ai.suggestion", response["suggestion"])
        return response
