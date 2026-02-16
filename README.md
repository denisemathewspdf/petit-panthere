# 🐆 Petit Panthère

**A privacy-first, extensible AI agent platform**

*Little Panther — calm, capable, always watching your back.*

---

## What Is This?

Petit Panthère is a personal AI agent designed to function as your digital operator. It's not just a task manager or chatbot — it's an extensible platform that can execute multi-step workflows, integrate with external systems, maintain memory, and operate autonomously.

**Think of it as:** Your own OpenClaw, built your way.

---

## Why Build This?

**Control:** Own your AI stack. No vendor lock-in, no platform risk.

**Privacy:** Your data stays yours. Sandboxed execution, explicit permissions.

**Learning:** Hands-on experience building agent systems, APIs, and integrations.

**Flexibility:** Add capabilities as you need them. Built to evolve.

---

## Core Capabilities (Planned)

### Phase 1: Foundation
- Natural language task management via Slack
- Scheduled check-ins and reminders
- Morning briefings and nightly summaries
- Persistent memory and context

### Phase 2: Intelligence
- Multi-step workflow orchestration
- Proactive monitoring and alerts
- Knowledge base integration
- Complex reasoning and planning

### Phase 3: Expansion
- Custom tool integrations
- File and document operations
- API orchestration
- System-level automation (within security limits)

---

## Architecture

```
┌─────────────────────────────────────────────┐
│           Interface Layer                   │
│  (Slack / Dashboard / CLI / Messaging)      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Agent Backend (FastAPI)             │
│  • Prompt orchestration                     │
│  • State management                         │
│  • Security enforcement                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│       Intelligence Layer (LLM)              │
│  • Claude (primary)                         │
│  • GPT (fallback)                           │
│  • Local models (future)                    │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│            Tool Executor                    │
│  • Google Sheets  • Calendar                │
│  • Email          • Scheduler               │
│  • File system    • APIs                    │
│  (Extensible plugin system)                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Memory Layer                      │
│  • Conversation history                     │
│  • Long-term facts                          │
│  • Task state                               │
└─────────────────────────────────────────────┘
```

---

## Security Model

- **Least-privilege access:** Tools only get permissions they need
- **Sandboxed execution:** Tool runs isolated from core system
- **Explicit confirmations:** High-impact actions require user approval
- **Transparent logging:** Full audit trail of all actions
- **Credential isolation:** Secrets stored separately from runtime

See [SECURITY.md](SECURITY.md) for full details.

---

## Tech Stack

**Backend:** Python + FastAPI  
**Intelligence:** Claude API (Anthropic) + OpenAI fallback  
**Storage:** SQLite (local) + Google Sheets (external)  
**Interface:** Slack SDK + future web dashboard  
**Deployment:** Docker + Railway / Fly.io  

---

## Getting Started

### Prerequisites
- Python 3.11+
- Slack workspace + bot token
- Claude API key (Anthropic)

### Setup
```bash
cd petit-panthere
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

---

## Project Status

**Current phase:** Early MVP  
**Next milestone:** Slack → Google Sheets task loop working  
**Demo ready:** Architecture docs + basic Slack bot  

---

## Philosophy

Petit Panthère is inspired by OpenClaw but built with different priorities:

- **Privacy-first:** Your data, your control
- **Extensible:** Built to add capabilities over time
- **Transparent:** Open architecture, clear security model
- **Personal:** Designed for individual use, not enterprise scale

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plan.

---

## Documentation

- [Architecture](ARCHITECTURE.md) — System design and technical details
- [Security](SECURITY.md) — Security model and threat analysis
- [Roadmap](ROADMAP.md) — Development phases and milestones
- [Contributing](CONTRIBUTING.md) — How to extend and customize

---

Built with 🐾 by Denise Mathews
