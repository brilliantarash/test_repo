import os

action_type = os.getenv("ACTION_TYPE")
event_name = os.getenv("EVENT_NAME")
print(f"Action type: {action_type}")
print(f"Event name: {event_name}")
print(f"Merged: {os.getenv("MERGED")}")
if action_type == "closed" and os.getenv("MERGED") == "true":
    print("Running in production mode")
elif (
    event_name == "pull_request_target"
    and action_type in ["opened", "synchronize", "reopened"]
) or event_name == "workflow_dispatch":
    print("Running in preview mode")
else:
    print("No action to take")
print(f"PR: {os.getenv('PR_NUMBER')}")