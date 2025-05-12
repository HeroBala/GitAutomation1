# GitAutomation1

This file was updated by PR automation script.
# 🤖 GitAutomation1

GitAutomation1 is a Python-based automation tool that simplifies GitHub workflows. It enables you to create branches, make file changes, push commits, and open pull requests — all from the command line.

> ✨ This project was bootstrapped using a Python script that automated its own GitHub creation and pull request.

---

## 🚀 Features

- 📁 Auto-create feature branches
- 📝 Modify or create project files (e.g. `README.md`)
- 💾 Stage, commit, and push changes
- 🔁 Open pull requests with title, body, labels, milestone, and assignee
- 🔐 Works with GitHub token (Personal Access Token)
- 🌐 Opens PR URL in your browser after creation
- 🔄 Optionally deletes merged branches

---

## 📦 Project Structure

GitAutomation1/
├── auto-pr-creator.py # Main script that automates PR creation
├── main.py # Placeholder Python entry point
├── README.md # This file

---

## ⚙️ Requirements

- Python 3.8+
- Git installed and initialized
- A GitHub repository with write access
- GitHub Personal Access Token (with `repo` scope)
- (Optional) `rich` for pretty CLI output

Install required libraries:

```bash
pip install requests rich
export GITHUB_TOKEN=ghp_yourtokenhere
python auto-pr-creator.py
GitHub repo (owner/repo): HeroBala/GitAutomation1
Feature branch name: add-readme
File to edit: README.md
Commit message: 📘 Add README.md with usage

