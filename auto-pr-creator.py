import os
import subprocess
import requests
import sys
import webbrowser

try:
    from rich import print
except ImportError:
    def print(x): __builtins__.print(x)

def prompt(prompt_text, default=""):
    return input(f"{prompt_text} [default: {default}]: ").strip() or default

def github_api(url, method="GET", data=None):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.request(method, f"https://api.github.com{url}", headers=headers, json=data)
    if not response.ok:
        print(f"[red]❌ GitHub API error: {response.status_code}[/red] - {response.text}")
        sys.exit(1)
    return response.json()

# === Step 0: GitHub Token Setup ===
print("[bold cyan]🚀 GitHub PR Creator with Branch Push[/bold cyan]")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("\n[bold yellow]⚠️ GitHub token not found.[/bold yellow]")
    token_url = "https://github.com/settings/tokens/new?scopes=repo&description=PR+Creator+Script"
    try:
        webbrowser.open(token_url)
        print(f"[blue]🌐 If your browser didn't open, visit:[/blue] {token_url}")
    except:
        print(f"[blue]🌐 Open this manually: {token_url}")
    print("\n[bold]✅ Create the token with the 'repo' scope[/bold]")
    GITHUB_TOKEN = input("Paste your GitHub token here: ").strip()

# === Step 1: Git Auth ===
user = github_api("/user")
username = user["login"]
print(f"🔐 Logged in as: [green]{username}[/green]")

# === Step 2: Repo Info ===
REPO = prompt("GitHub repo (owner/repo)", "HeroBala/GitAutomation1")
repo_info = github_api(f"/repos/{REPO}")
default_branch = repo_info["default_branch"]

# === Step 3: Create Feature Branch and Make a Change ===
FEATURE_BRANCH = prompt("Feature branch name", "add-readme")
FILE_NAME = prompt("File to create/edit", "README.md")
COMMIT_MESSAGE = prompt("Git commit message", f"📘 Add {FILE_NAME}")

print(f"\n🌿 Creating and switching to branch: {FEATURE_BRANCH}")
subprocess.run(["git", "checkout", "-b", FEATURE_BRANCH], check=True)

print(f"📝 Writing to file: {FILE_NAME}")
with open(FILE_NAME, "a") as f:
    f.write("\nThis file was updated by PR automation script.\n")

subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
subprocess.run(["git", "push", "--set-upstream", "origin", FEATURE_BRANCH], check=True)

# === Step 4: Pull Request Details ===
BASE_BRANCH = prompt("Base branch", default_branch)
PR_TITLE = prompt("Pull Request Title", COMMIT_MESSAGE)
PR_BODY = prompt("Pull Request Description", "This change was made automatically by script.")
LABELS = prompt("Labels (comma-separated)", "automation,update").split(",")
MILESTONE_TITLE = prompt("Milestone title", "v1.0 - First Automation").strip().split("\n")[0]

# === Step 5: Create PR ===
print("\n📤 Creating pull request...")
pr_payload = {
    "title": PR_TITLE,
    "head": FEATURE_BRANCH,
    "base": BASE_BRANCH,
    "body": PR_BODY
}
pr = github_api(f"/repos/{REPO}/pulls", "POST", pr_payload)
pr_number = pr["number"]
pr_url = pr["html_url"]
print(f"[green]✅ Pull Request #{pr_number} created: {pr_url}[/green]")

# === Step 6: Add Labels (safe creation) ===
print(f"\n🏷️  Adding labels: {', '.join(LABELS)}")
existing_labels = github_api(f"/repos/{REPO}/labels")
existing_label_names = [label["name"] for label in existing_labels]
for label in LABELS:
    label = label.strip()
    if label not in existing_label_names:
        github_api(f"/repos/{REPO}/labels", "POST", {"name": label})
github_api(f"/repos/{REPO}/issues/{pr_number}/labels", "POST", {"labels": LABELS})

# === Step 7: Milestone (safe lookup and create) ===
print(f"\n📌 Checking milestone: {MILESTONE_TITLE}")
milestones = github_api(f"/repos/{REPO}/milestones")
milestone_id = next((m["number"] for m in milestones if m["title"] == MILESTONE_TITLE), None)

if milestone_id is None:
    milestone = github_api(f"/repos/{REPO}/milestones", "POST", {
        "title": MILESTONE_TITLE,
        "description": f"Milestone for: {MILESTONE_TITLE}",
        "state": "open"
    })
    milestone_id = milestone["number"]
    print(f"🆕 Created milestone: {MILESTONE_TITLE}")

github_api(f"/repos/{REPO}/issues/{pr_number}", "PATCH", {"milestone": milestone_id})

# === Step 8: Assign PR ===
print(f"\n👤 Assigning PR to: {username}")
github_api(f"/repos/{REPO}/issues/{pr_number}/assignees", "POST", {"assignees": [username]})

# === Done ===
print(f"\n[bold magenta]🎉 Done! Pull request created:[/bold magenta] [cyan]{pr_url}[/cyan]")
