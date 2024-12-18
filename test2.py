import json
import os

import github


with open(os.getenv("GITHUB_EVENT_PATH"), "r") as f:
    event_data = json.load(f)
pr_number = event_data.get("number") or int(event_data.get("inputs", {}).get("pr_number"))
closed = event_data.get("action") == "closed"
merged = event_data.get("pull_request", {}).get("merged", False)
print(f"pr_number: {pr_number}")
print(f"closed: {closed}")
print(f"pr_merged: {merged}")
preview = not merged and not closed
if not merged and closed:
    print("No action to take")
print(f"preview: {preview}")

g = github.Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
pr = repo.get_pull(pr_number)

processed_files_path = "processed_files.json"
processed_files_branch = "processed_files"


try:
    branch = repo.get_branch(processed_files_branch)
except:
    repo.create_git_ref(
        ref=f"refs/heads/{processed_files_branch}",
        sha=repo.get_branch("main").commit.sha,
    )
    message = f"Initialize {processed_files_branch} with {processed_files_path}"
    repo.create_file(
        path=processed_files_path,
        message=message,
        content="{}",
        branch=processed_files_branch,
    )
    print(message)
    branch = repo.get_branch(processed_files_branch)

file_content = repo.get_contents(processed_files_path, ref=branch.commit.sha)
processed_files = file_content.decoded_content.decode()
with open(processed_files_path, "w") as f:
    f.write(processed_files)
print(f"processed_files:\n {processed_files}")

if os.path.exists(processed_files_path):
    with open(processed_files_path, "r") as file:
        file_data_json = json.load(file)
    file_data_json = {"test": "test"}
    with open(processed_files_path, "w") as file:
        json.dump(file_data_json, file)

with open(processed_files_path, "r") as file:
    file_data = file.read()

processed_files_content_file = repo.get_contents(
    processed_files_path, ref=processed_files_branch
)
message = f"Update {processed_files_path}"
repo.update_file(
    path=processed_files_path,
    message=message,
    content=file_data,
    sha=processed_files_content_file.sha,
    branch=processed_files_branch,
)
print(message)

def get_files():
    files_to_process = []
    for file in pr.get_files():
        file_path = file.filename
        if file_path.endswith(".md"):
            pr_content = pr.head.repo.get_contents(
                file_path, ref=pr.head.ref
            ).decoded_content.decode()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(pr_content)
            files_to_process.append(file_path)

    return files_to_process

files_to_process = get_files()
print("files_to_process:",files_to_process)
for file2 in files_to_process:
    with open(file2, "r") as f:
        print(f.read())