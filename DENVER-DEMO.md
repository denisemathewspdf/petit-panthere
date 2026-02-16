# 🐆 Petit Panthère — Denver Demo Guide

**How to pitch your AI agent platform at ETH Denver & Blockchain Unmasked meetings**

---

## The Hook (30 seconds)

> "I'm building my own AI agent platform. It's called Petit Panthère — French for 'little panther.' Think of it as your personal Chief of Staff who manages tasks, schedules, and workflows autonomously. I wanted full control over my AI stack and a deeper understanding of agent systems, so I'm building it from scratch. Want to see it?"

**Why this works:**
- Instantly interesting (building, not just using)
- Memorable name + visual (panther = capable, independent)
- Invites engagement ("want to see it?")

---

## The Context (1 minute)

**Why you're building this:**

> "I've been using OpenClaw — it's an amazing AI gateway. But the founder just joined OpenAI, and I got concerned about long-term Claude support. That sparked the idea: what if I built my own agent platform? Not just for security reasons, but as a learning opportunity. I want to deeply understand agent architecture, LLM orchestration, and tool integration. Plus, I can customize it exactly for my workflows."

**What makes Petit Panthère different:**

> "It's privacy-first by design. Every tool runs sandboxed with explicit permissions. High-risk actions require user confirmation. All actions are audited. I own my data — nothing leaves my control unless I approve it. And it's built to be extensible: adding new capabilities should be as simple as dropping in a new plugin."

---

## The Architecture (2 minutes)

**Pull up on your phone/laptop:** `/Users/denisem/Desktop/Katarina's Projects/petit-panthere/README.md`

**Walk through the stack diagram:**

```
Interface Layer (Slack, future dashboard)
     ↓
Agent Backend (FastAPI orchestration)
     ↓
Intelligence Layer (Claude API)
     ↓
Tool Executor (Google Sheets, email, scheduler...)
     ↓
Memory Layer (SQLite + long-term storage)
```

**Explain each layer in one sentence:**
- **Interface:** How I talk to the agent (Slack now, dashboard later)
- **Backend:** Routes requests, enforces security, manages state
- **Intelligence:** Claude does the reasoning and planning
- **Tools:** Integrate with real systems (Sheets, calendar, email)
- **Memory:** Remembers context and facts across sessions

**Key point:**
> "It's modular. If Claude disappears tomorrow, I swap in GPT or a local model. If Slack goes down, I use the dashboard. No single point of failure."

---

## The Security Model (2 minutes)

**This is your differentiator — emphasize this for Blockchain Unmasked (they care about security)**

**Pull up:** `/Users/denisem/Desktop/Katarina's Projects/petit-panthere/SECURITY.md`

**Key points:**

1. **Least privilege:**
   > "Every tool declares what permissions it needs. I review and approve once. It can't do anything beyond that."

2. **Sandboxing:**
   > "Tools run in isolated processes with resource limits. If a plugin is compromised, it can't access the main system or other tools."

3. **Confirmation prompts:**
   > "High-risk actions pause execution and ask me first. Like sending an email to someone outside my domain — it shows me the draft and waits for approval."

4. **Audit logging:**
   > "Every action is logged with timestamp and parameters. I can query: 'Show me all emails sent this week' or 'When did I last update that task?' Full transparency."

5. **Prompt injection defense:**
   > "The agent is hardened against attacks where someone tries to trick the LLM into ignoring security rules. System prompts are immutable, and suspicious commands get flagged."

**Why this matters:**
> "For a crypto forensics company, security isn't optional. I built this with a threat model from day one. If I can secure my personal agent, I can think about securing customer-facing systems."

---

## The Demo (1 minute)

**If you have Slack bot working:**

1. Pull up Slack on your phone
2. Send command: "Add task: follow up with Blockchain Unmasked team"
3. Agent responds: "✅ Task added: Follow up with Blockchain Unmasked team (p1, due today)"
4. Show Google Sheet updating in real-time
5. "That's the loop: Slack → Backend → Claude understands intent → Tool executes → Response. Right now it's simple, but the architecture supports complex workflows."

**If Slack bot not ready:**

1. Show architecture docs (README.md)
2. Walk through tool sandbox code (SECURITY.md example)
3. "It's not live yet, but the design is solid. I'm two weeks in. Next milestone is scheduled autonomy — morning briefings, proactive reminders."

---

## The Vision (1 minute)

**Where this is going:**

> "Short-term: Task management, scheduling, email integration. I want morning briefings, nightly summaries, proactive check-ins.
>
> Medium-term: Dashboard UI, 10+ tool integrations, smart workflow orchestration. Like 'I have a trip next week' → agent moves tasks, creates packing list, sets reminders.
>
> Long-term: Voice interface, mobile app, maybe open-source it. I want Petit Panthère to feel like a real team member — someone who knows my priorities, anticipates my needs, and handles routine work autonomously."

**Personal benefit:**
> "I'm building this for me first. If it works, it becomes a portfolio piece. But more importantly, I'm learning systems design, security architecture, and agent development hands-on. That's worth more than any course."

---

## Handling Questions

**"Why not just use existing tools like Zapier or Notion?"**
> "Those are great for connecting apps, but they're not intelligent. Petit Panthère understands natural language, reasons about context, and adapts to my needs. It's more like a team member than a workflow automation tool."

**"How is this different from OpenClaw?"**
> "OpenClaw is a full-featured gateway with multi-user support and tons of integrations. Petit Panthère is lighter, more focused, and built specifically for my workflows. I also wanted to own the entire stack and learn by building it myself."

**"What if Claude API gets expensive or goes away?"**
> "That's exactly why I architected it this way. The intelligence layer is swappable. I can use GPT, local Llama models, or any LLM with an API. No vendor lock-in."

**"Is this for personal use or will you sell it?"**
> "Personal first. But if it works well, I could open-source it or turn it into a product. Right now, I'm focused on making it bulletproof for me."

**"What's the hardest part?"**
> "Security and reliability. It's easy to build a chatbot. It's hard to build one you trust with your calendar, email, and tasks. That's why I spent so much time on sandboxing, permissions, and audit logging."

**"Can you integrate with blockchain tools?"**
> "Absolutely. The tool system is extensible. If there's an API or CLI, I can wrap it as a plugin. For crypto forensics, imagine an agent that monitors on-chain activity, flags suspicious transactions, and alerts your team. That's totally feasible."

---

## What to Bring to Denver

1. **Laptop or tablet** — easier to show docs/code
2. **Phone with Slack** — if you have bot demo working
3. **Business card or LinkedIn QR** — for follow-ups
4. **This doc** — reference if you forget talking points

---

## Opening Lines (Networking)

**At ETH Denver:**
> "Hey! I'm Denise. I'm building an AI agent platform for personal automation. Are you working with AI at all?"

**At Blockchain Unmasked meetings:**
> "I've been thinking about how agent systems could help with crypto forensics — like autonomous monitoring and alerting. Have you explored AI for investigation workflows?"

**If someone asks what you do:**
> "I'm in consulting right now, focused on operations and talent. But I'm also building an AI agent platform on the side — learning systems design and backend development. It's called Petit Panthère. Want to hear about it?"

---

## Follow-Up Strategy

**After demo, if they're interested:**

1. **Exchange contact:** "Let me send you the GitHub link when I open-source it."
2. **Ask about their use case:** "What would you use an agent like this for?"
3. **Offer to connect later:** "I'm still building it out, but happy to show you updates in a few weeks."

**For Blockchain Unmasked specifically:**

> "If you're interested, I can write up a design doc on how agent systems could integrate with crypto forensics workflows. Would that be useful?"

---

## Pitch Hierarchy (Most to Least Important)

1. **Architecture & security** — shows systems thinking
2. **Learning initiative** — shows drive and curiosity
3. **Working demo** — shows execution (if you have it)
4. **Vision** — shows you think long-term
5. **Name & branding** — memorable, but secondary

---

## Confidence Boosters

**Remember:**
- You don't need a perfect demo. Architecture docs alone show you understand system design.
- "I'm two weeks in" is impressive, not a disclaimer. Most people never start.
- Blockchain Unmasked is early-stage — they value hustle and learning over perfect polish.
- This conversation opener works even if Petit Panthère isn't live yet: "I'm building..." is more interesting than "I use..."

---

## Quick Reference Card (Fit on Phone Screen)

**Name:** Petit Panthère (little panther)

**Tagline:** Privacy-first AI agent platform

**Why I built it:** Control my AI stack + learn agent systems

**Architecture:** Interface → Backend → LLM → Tools → Memory

**Security:** Sandboxed tools, explicit permissions, audit logging

**Status:** 2 weeks in, architecture done, basic demo working

**Next:** Scheduling, dashboard UI, tool expansion

**Vision:** Personal Chief of Staff who operates autonomously

**Demo:** Slack → Claude → Google Sheets (if working)

**Ask:** "What would you use an agent like this for?"

---

## Final Prep (Night Before)

1. Read through this doc once
2. Practice 30-second pitch out loud (seriously, say it in the mirror)
3. Test Slack bot if you have it working
4. Charge laptop/phone
5. Screenshot key docs (README architecture diagram) in case WiFi sucks
6. Get good sleep — confidence comes from rest

---

**You got this. 🐾**

**Petit Panthère is a conversation starter, a learning project, and a portfolio piece. Even if it's not "done," talking about it shows systems thinking, initiative, and technical depth. That's what they'll remember.**

---

*Last updated: 2026-02-15*
