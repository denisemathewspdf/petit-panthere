# 🐆 Petit Panthère — Architecture Diagram

**Visual system design — show this on your phone during demos**

---

## The Stack (Top to Bottom)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              👤 USER (Denise)                       │
│           "Add task: film workout video"           │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          🔌 INTERFACE LAYER                         │
│                                                     │
│   Slack              Dashboard         CLI          │
│   (now)              (future)        (future)       │
│                                                     │
│   Receives commands → Sends responses               │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         ⚙️ AGENT BACKEND (Orchestrator)            │
│                                                     │
│   • Parse incoming commands                         │
│   • Check permissions (is this allowed?)            │
│   • Route to LLM or tools                           │
│   • Enforce security policies                       │
│   • Log all actions (audit trail)                   │
│   • Manage conversation context                     │
│                                                     │
│   Tech: FastAPI (Python)                            │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│        🧠 INTELLIGENCE LAYER (LLM)                  │
│                                                     │
│   Claude Opus       Claude Sonnet      GPT-4        │
│   (reasoning)       (speed)          (fallback)     │
│                                                     │
│   Understands intent:                               │
│   "Add task..." → call add_task()                   │
│   "What's due?" → call list_tasks(due=today)        │
│   "Remind me..." → call schedule_reminder()         │
│                                                     │
│   Tech: Anthropic API (primary)                     │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         🔧 TOOL EXECUTOR (Plugin System)            │
│                                                     │
│   Each tool runs in sandbox (isolated subprocess)   │
│                                                     │
│   ┌──────────────┐  ┌──────────────┐               │
│   │  TaskTool    │  │ SchedulerTool│               │
│   │  (Sheets)    │  │  (Cron jobs) │               │
│   └──────────────┘  └──────────────┘               │
│                                                     │
│   ┌──────────────┐  ┌──────────────┐               │
│   │  EmailTool   │  │ CalendarTool │               │
│   │  (Gmail)     │  │  (GCal)      │               │
│   └──────────────┘  └──────────────┘               │
│                                                     │
│   ┌──────────────┐  ┌──────────────┐               │
│   │   WebTool    │  │   FileTool   │               │
│   │  (Search)    │  │  (Local FS)  │               │
│   └──────────────┘  └──────────────┘               │
│                                                     │
│   Extensible: Add new tools by dropping in plugins  │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         💾 MEMORY LAYER (Persistent State)          │
│                                                     │
│   Conversation History       Long-term Facts        │
│   (SQLite)                   (JSON / Vector DB)     │
│                                                     │
│   Task State                 User Preferences       │
│   (Google Sheets)            (Config files)         │
│                                                     │
│   Audit Logs                                        │
│   (Append-only SQLite)                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Data Flow Example

**User command:** "Add task: film workout video"

```
1. USER types in Slack
   ↓
2. INTERFACE LAYER receives message
   ↓
3. AGENT BACKEND:
   - Loads context (last 10 messages)
   - Checks: Can user add tasks? ✓
   - Sends to Intelligence Layer
   ↓
4. INTELLIGENCE LAYER (Claude):
   - Understands: User wants to add a task
   - Plans: Use TaskTool.add_task()
   - Generates: Parameters (text="Film workout video", priority="p1")
   ↓
5. TOOL EXECUTOR:
   - Validates: Is input safe? ✓
   - Executes: TaskTool runs in sandbox
   - Google Sheets: Append row to task list
   - Returns: Success
   ↓
6. AGENT BACKEND:
   - Logs action to audit trail
   - Saves message to conversation history
   - Sends response to Interface Layer
   ↓
7. INTERFACE LAYER posts to Slack:
   "✅ Task added: Film workout video (p1, due today)"
   ↓
8. USER sees confirmation
```

**Total time:** ~2-3 seconds (mostly LLM + API calls)

---

## Security Model (Show This for Blockchain Unmasked!)

```
┌─────────────────────────────────────────────────────┐
│              🛡️ SECURITY LAYERS                     │
└─────────────────────────────────────────────────────┘

Layer 1: AUTHENTICATION
├─ Slack webhook signature verification
├─ User ID whitelist
└─ Session tokens (dashboard/CLI)

Layer 2: PERMISSIONS
├─ Tools declare required permissions
│  Example: TaskTool needs [sheets.read, sheets.write]
├─ User grants access (one-time approval)
└─ Runtime enforcement (checked on every call)

Layer 3: TOOL SANDBOXING
├─ Each tool runs in isolated subprocess
├─ Resource limits (CPU, memory, time)
├─ No network access unless explicitly granted
└─ Can't access parent process or other tools

Layer 4: CONFIRMATION PROMPTS
├─ High-risk actions pause execution
│  Example: Sending email to external address
├─ Slack message with Approve/Deny buttons
├─ Timeout after 5 minutes (auto-deny)
└─ User has final control

Layer 5: AUDIT LOGGING
├─ Every action logged (timestamp + params + result)
├─ Append-only storage (can't be modified)
├─ Queryable: "Show all emails sent this week"
└─ Sensitive data redacted (API keys → ***)

Layer 6: PROMPT INJECTION DEFENSE
├─ Hardened system prompt (security rules immutable)
├─ Input validation (detect malicious patterns)
├─ Monitoring (alert on unusual activity)
└─ LLM can be tricked, but confirmations + logs catch it
```

---

## Key Design Principles

```
┌────────────────────────────────────────┐
│   MODULARITY                           │
│   Components can be swapped            │
│   Example: Switch LLM without          │
│   rewriting the whole system           │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│   EXTENSIBILITY                        │
│   Adding new tools is simple           │
│   Just drop in a new plugin            │
│   No core system changes needed        │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│   SECURITY                             │
│   Least-privilege by default           │
│   Defense in depth (multiple layers)   │
│   Fail secure (deny if uncertain)      │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│   TRANSPARENCY                         │
│   Every action auditable               │
│   Logs show exactly what happened      │
│   User always has visibility           │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│   SIMPLICITY                           │
│   Build what's needed, not more        │
│   Avoid over-engineering               │
│   Clear, readable architecture         │
└────────────────────────────────────────┘
```

---

## Tech Stack Summary

| Layer | Tech | Why |
|-------|------|-----|
| **Interface** | Slack SDK, React (future) | User-friendly, widely used |
| **Backend** | FastAPI (Python) | Fast, async, easy to extend |
| **Intelligence** | Claude API (Anthropic) | Best reasoning, privacy-focused |
| **Tools** | Plugin system | Extensible, sandboxed |
| **Memory** | SQLite, Google Sheets | Simple, reliable, accessible |
| **Deployment** | Railway / Fly.io | Free tier, easy setup, always-on |

---

## Comparison: Petit Panthère vs Others

```
┌──────────────────┬─────────────┬─────────────┬─────────────┐
│                  │   OpenClaw  │    Zapier   │   Petit P.  │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Intelligence     │   High      │    Low      │    High     │
│ Privacy          │   Strong    │   Weak      │   Strongest │
│ Extensibility    │   High      │   Medium    │    High     │
│ Learning curve   │   Steep     │    Easy     │   Medium    │
│ Customization    │   Medium    │    Low      │    Full     │
│ Control          │   Partial   │   None      │    Total    │
│ Cost             │   Free      │ $20-100/mo  │    Free     │
└──────────────────┴─────────────┴─────────────┴─────────────┘
```

---

## Roadmap Timeline

```
Phase 0: DENVER DEMO (2 days) ✅
├─ Architecture docs
├─ Basic Slack bot
└─ Security model

Phase 1: CORE LOOP (Week 1)
├─ Task management working
├─ Google Sheets integration
└─ Memory persistence

Phase 2: AUTONOMY (Week 2)
├─ Scheduled check-ins
├─ Morning briefings
└─ Custom reminders

Phase 3: INTELLIGENCE (Week 3)
├─ Multi-step workflows
├─ Context-aware suggestions
└─ Learning from feedback

Phase 4: TOOL EXPANSION (Week 4)
├─ Email, Calendar, Web, Files
├─ Permission system live
└─ Confirmation prompts

Phase 5: DASHBOARD UI (Month 2)
├─ React frontend
├─ Visual task board
└─ Mobile-friendly

Phase 6: PRODUCTION (Month 3)
├─ 99.9% uptime
├─ Polish & performance
└─ Ready to share
```

---

## Questions to Spark Conversation

**Show this diagram, then ask:**

1. "What would you add to this architecture?"
2. "For crypto forensics, what tools would be most valuable?"
3. "How would you handle real-time blockchain monitoring in this system?"
4. "What security concerns do you have with AI agents?"
5. "Want to see the code or security model?"

---

**This diagram shows systems thinking, security awareness, and clear communication. Perfect for Chief of Staff conversations.** 🐾

---

*Last updated: 2026-02-15 | Ready for Denver*
