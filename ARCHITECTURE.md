# 🏗️ Petit Panthère Architecture

**System design for a privacy-first AI agent platform**

---

## Design Principles

1. **Modularity:** Components can be swapped without breaking the system
2. **Extensibility:** Adding new tools should be simple
3. **Security:** Least-privilege access by default
4. **Transparency:** Every action should be auditable
5. **Simplicity:** Avoid over-engineering — build what's needed

---

## System Components

### 1. Interface Layer

**Purpose:** User interaction surface

**Current:**
- Slack (primary control surface)
- Commands: `/task add`, `/task list`, `/remind`, `/check-in`

**Future:**
- Web dashboard (task management, system status)
- CLI (local control, debugging)
- Email (summary reports, notifications)
- SMS/messaging (urgent alerts)

**Design decision:** Interface is decoupled from backend. Any interface can send commands to the agent core.

---

### 2. Agent Backend (Orchestrator)

**Purpose:** Central nervous system — routes requests, enforces security, manages state

**Tech:** FastAPI (Python)

**Key responsibilities:**
- Parse incoming commands
- Route to appropriate tool executor
- Enforce security policies
- Maintain conversation context
- Log all actions

**API Structure:**
```python
POST /agent/command
{
  "user_id": "denise",
  "channel": "slack",
  "message": "Add task: film workout video",
  "context": { ... }
}

Response:
{
  "success": true,
  "response": "Task added: Film workout video (Priority: p1, Due: today)",
  "actions": [
    {"type": "sheet_write", "status": "success"}
  ]
}
```

**State management:**
- Session context (last 10 messages)
- Active tasks
- User preferences
- Tool credentials (encrypted)

---

### 3. Intelligence Layer (LLM)

**Purpose:** Understand intent, plan actions, generate responses

**Primary:** Claude (Anthropic API)
- Models: Claude Opus (reasoning), Claude Sonnet (speed)
- Why Claude: Best for agent-style reasoning, strong privacy stance

**Fallback:** OpenAI GPT-4
- Used if Claude unavailable
- Configurable in .env

**Future:** Local models
- Llama 3, Mistral for offline operation
- Privacy-critical workflows

**Prompt structure:**
```
System: You are Petit Panthère, a personal AI agent...

User: Add task: film workout video

Tools available:
- add_task(text, priority, due_date)
- search_tasks(query)
- send_reminder(time, message)

Response format: [reasoning] → [tool_call] → [user_message]
```

---

### 4. Tool Executor (Plugin System)

**Purpose:** Execute actions in the real world

**Design:** Each tool is a Python class with standard interface

**Base Tool Interface:**
```python
class Tool:
    name: str
    description: str
    required_permissions: list[str]
    
    def validate_input(self, params: dict) -> bool:
        """Check if params are safe and valid"""
        
    def execute(self, params: dict) -> dict:
        """Run the tool, return result"""
        
    def rollback(self, execution_id: str):
        """Undo action if possible"""
```

**Initial Tools:**

1. **TaskTool** — Google Sheets integration
   - add_task, list_tasks, update_task, complete_task
   - Permissions: sheets.read, sheets.write

2. **SchedulerTool** — Cron-like scheduling
   - schedule_reminder, list_scheduled, cancel_scheduled
   - Permissions: scheduler.create

3. **EmailTool** — Notifications
   - send_email, send_summary
   - Permissions: email.send

**Adding new tools:**
1. Create tool class in `tools/`
2. Register in `tools/registry.py`
3. Update system prompt with tool description
4. Grant permissions in security config

---

### 5. Memory Layer

**Purpose:** Persistent storage of context, facts, and state

**Storage:**

1. **Conversation History** (SQLite)
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME,
  role TEXT, -- 'user' or 'assistant'
  content TEXT,
  session_id TEXT
);
```

2. **Long-term Facts** (JSON file + vector DB future)
```json
{
  "preferences": {
    "morning_routine_time": "7:00 AM",
    "preferred_tone": "supportive",
    "priority_tasks_first": true
  },
  "facts": [
    {"text": "Denise has a trip to Denver Feb 17-20", "timestamp": "2026-02-14"},
    {"text": "Prefers outdoor workout filming at Crissy Field", "timestamp": "2026-02-15"}
  ]
}
```

3. **Task State** (Google Sheets)
- External storage for tasks (accessible outside system)
- Columns: Task, Priority, Status, Due, Notes

**Future: Vector DB**
- Semantic search over conversation history
- "What did we decide about filming schedule?"
- Tech: ChromaDB or pgvector

---

## Data Flow

### Example: User sends Slack command

```
1. User: "/task add film workout video p1"
   └─> Slack API receives webhook

2. Interface Layer:
   └─> Parse Slack event
   └─> POST /agent/command to backend

3. Agent Backend:
   └─> Load user context (last 10 messages)
   └─> Check permissions (can user add tasks?)
   └─> Send to Intelligence Layer

4. Intelligence Layer (Claude):
   └─> Understand: User wants to add a task
   └─> Plan: Use TaskTool.add_task()
   └─> Generate response: "Task added!"

5. Tool Executor:
   └─> TaskTool.validate_input() ✓
   └─> TaskTool.execute()
       └─> Google Sheets API: Append row
   └─> Return success

6. Agent Backend:
   └─> Log action
   └─> Save message to memory
   └─> Return response to Interface Layer

7. Interface Layer:
   └─> Post message to Slack: "✅ Task added: Film workout video (p1, today)"
```

**Total latency:** ~2-3 seconds (mostly LLM + API calls)

---

## Security Architecture

See [SECURITY.md](SECURITY.md) for full threat model.

**Key mechanisms:**

1. **Tool Sandboxing:**
   - Each tool runs in isolated subprocess
   - Resource limits (CPU, memory, time)
   - No network access unless explicitly granted

2. **Permission System:**
   - Tools declare required permissions
   - User grants permissions per tool
   - Runtime enforcement (checked on every call)

3. **Confirmation Prompts:**
   - High-risk actions (delete, send email to external) require user approval
   - Backend pauses execution, sends Slack message with approve/deny buttons
   - Timeout after 5 minutes (auto-deny)

4. **Audit Logging:**
   - Every tool execution logged with timestamp, params, result
   - Stored in append-only log
   - Queryable: "Show all emails sent this week"

---

## Deployment

**Development:**
- Local machine (laptop)
- SQLite database
- `python main.py` (runs FastAPI on port 8000)

**Production:**
- Docker container
- Railway or Fly.io (always-on hosting)
- Environment variables for secrets
- Health check endpoint: `GET /health`

**Monitoring:**
- Logs piped to file (future: Loki/Grafana)
- Slack alerts on errors
- Weekly summary email (uptime, actions taken)

---

## Scalability

**Current scope:** Single-user personal agent

**Not goals (yet):**
- Multi-user support
- Enterprise features
- High-throughput workflows

**If needed later:**
- Replace SQLite with PostgreSQL
- Add Redis for session caching
- Kubernetes for orchestration

**Philosophy:** Build for current needs, architect for future flexibility.

---

## Comparison: Petit Panthère vs OpenClaw

| Feature | OpenClaw | Petit Panthère |
|---------|----------|----------------|
| **Focus** | General-purpose AI gateway | Personal agent platform |
| **Deployment** | Self-hosted gateway | Lightweight service |
| **Model Support** | Multi-provider | Claude-first, extensible |
| **Privacy** | Strong | Stronger (full control) |
| **Extensibility** | Skill system | Plugin system |
| **Target User** | Power users | Individual (you) |
| **Complexity** | Higher (full gateway) | Lower (focused scope) |

**Why build this?**
- OpenClaw founder at OpenAI → risk of reduced Claude support
- Learning opportunity (backend, agents, APIs)
- Custom features tailored to your workflows
- Ownership and control

---

## Next Steps

**Immediate (MVP):**
1. ✅ Architecture docs (this file)
2. ⏳ Slack bot skeleton (receives commands, echoes back)
3. ⏳ TaskTool implementation (Google Sheets integration)
4. ⏳ Basic LLM loop (Claude API → understand → route → respond)

**Week 1:**
- Full task management working
- Scheduled check-ins
- Memory persistence

**Month 1:**
- Dashboard UI
- Email notifications
- 5+ tools integrated

---

**Designed by Denise Mathews — Built to evolve** 🐾
