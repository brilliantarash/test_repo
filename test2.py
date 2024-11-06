import os

closed = os.getenv("ACTION_TYPE") == "closed"
merged = os.getenv("MERGED") == "true"
try:
    pr = int(os.getenv("PR_NUMBER"))
except Exception as e:
    raise Exception(f"PR_NUMBER is not a number or not set: {e}")
print(f"Closed: {closed}")
print(f"Merged: {merged}")
print(f"PR: {pr}")

if merged:
    print("Running in production mode")
elif not closed:
    print("Running in preview mode")
else:
    print("closed but not merged")