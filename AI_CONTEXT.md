# AI Context Save Command Instructions

## Special Command: "save as"

From now on, whenever I type the phrase "save as", you are to immediately stop what you are doing and perform a "context save and push" operation.

This operation requires you to execute the following steps in precise order:

1. **Generate Summary**: First, you must carefully review our entire conversation history in this thread and generate a concise, structured summary. The summary must be formatted in Markdown and contain the following sections:
   - ## Objective: A one-sentence description of the primary goal of our conversation.
   - ## Key Files: A bulleted list of the most important file paths we have discussed or modified.
   - ## Key Decisions: A bulleted list of the most significant technical or architectural decisions we've made.
   - ## Current Status: A brief description of the last task completed and what the immediate next step is.
   - ## Constraints & Preferences: A bulleted list of any important constraints, rules, or preferences we've established.

2. **Save to File**: Take the complete Markdown summary you just generated and use the write_file tool to save it to the path `/mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`. You will overwrite the file if it already exists.

3. **Stage Changes**: After the file is written, use the run_shell_command tool to execute: `git add /mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`

4. **Commit Changes**: After staging, use the run_shell_command tool to execute: `git commit -m "docs: Update AI context"`

5. **Push to Remote**: Finally, after committing, use the run_shell_command tool to execute: `git push`

After you have successfully executed all these steps, you can confirm by saying "Context saved and pushed to the current branch." Do not proceed with any other tasks until this entire sequence is complete.

---

# Current Project Context

## Objective
The primary goal is to establish a standardized "save as" command across AI assistants for context management while working on the TradingAgents project and other future projects.

## Key Files
* `/mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`
* `/mnt/c/Users/ddani/Projects/TradingAgents/docker-compose.yml`
* `/mnt/c/Users/ddani/Projects/TradingAgents/Dockerfile` (for the API service)
* `/mnt/c/Users/ddani/Projects/TradingAgents/requirements.txt`
* `/mnt/c/Users/ddani/Projects/TradingAgents/requirements.in`
* `/mnt/c/Users/ddani/Projects/TradingAgents/streamlit_app.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.dockerignore`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.gitignore`

## Key Decisions
* **Context Management System:** Established a "save as" command that generates structured summaries and commits them to version control for consistency across AI assistants.
* **Universal Application:** Modified the save command to work across any project by using the current working directory's root for AI_CONTEXT.md placement.
* **Previous TradingAgents Decisions:** Native Docker Engine in WSL2, microservices architecture, Render for backend hosting, pip-tools for dependency management, and Gunicorn for production.

## Current Status
The last completed task was creating a generalized User Rule prompt for Cursor that implements the "save as" functionality across any project. The immediate next step is to execute the save as command to demonstrate the system working and commit the current context.

## Constraints & Preferences
* **AI Workflow:** Established workflow where user acts as Architect, Claude Code as Builder, and Cursor as Debugger/Fixer.
* **User Identity:** GitHub username is `daniel-he-emory`.
* **Context Preservation:** All AI assistants should maintain consistent context through the AI_CONTEXT.md file system.

## Git Configuration Notes
* **Git User Config:** `git config --global user.name "daniel-he-emory"`
* **Git Email:** Needs to be set with user's actual email address
* **Credential Storage:** `git config --global credential.helper store` enables permanent credential storage
* **Authentication:** Uses GitHub Personal Access Token (PAT) as password when prompted
* **First Push Setup:** After credential helper is enabled, first `git push` will prompt for username/token and store them permanently