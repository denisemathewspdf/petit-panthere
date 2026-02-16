# 🔧 Petit Panthère Setup Guide

**Get the Slack bot demo running in 15 minutes**

---

## Prerequisites

- **Python 3.11+** (check: `python3 --version`)
- **Slack workspace** where you can create apps
- **Claude API key** (from Anthropic)

---

## Step 1: Create Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name it **"Petit Panthère"**
4. Select your workspace

### Configure Bot Permissions

1. Go to **OAuth & Permissions**
2. Scroll to **Bot Token Scopes**
3. Add these scopes:
   - `chat:write` — Send messages
   - `im:history` — Read DM history
   - `im:read` — Access DMs
   - `app_mentions:read` — See mentions (if using in channels)

4. Scroll up and click **"Install to Workspace"**
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
   - Save this for later

### Enable Socket Mode

1. Go to **Socket Mode** in sidebar
2. Toggle **"Enable Socket Mode"**
3. Go to **Basic Information** in sidebar
4. Scroll to **App-Level Tokens**
5. Click **"Generate Token and Scopes"**
   - Name: `socket-token`
   - Scope: `connections:write`
6. Copy the token (starts with `xapp-`)
   - Save this for later

### Subscribe to Events

1. Go to **Event Subscriptions** in sidebar
2. Toggle **"Enable Events"** → ON
3. Under **Subscribe to bot events**, add:
   - `message.im` — Direct messages to bot
   - `app_mention` — When bot is mentioned (optional)
4. Click **"Save Changes"**

---

## Step 2: Get Claude API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to **API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-`)

---

## Step 3: Clone & Configure

```bash
# Navigate to project folder
cd "/Users/denisem/Desktop/Katarina's Projects/petit-panthere"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Now edit `.env` and fill in your credentials:

```bash
SLACK_BOT_TOKEN=xoxb-YOUR-TOKEN
SLACK_APP_TOKEN=xapp-YOUR-TOKEN
CLAUDE_API_KEY=sk-ant-YOUR-KEY
```

**IMPORTANT:** Never commit `.env` to git! (Already in `.gitignore`)

---

## Step 4: Run the Bot

```bash
# Make sure virtual environment is active (you should see "(venv)" in terminal)
source venv/bin/activate

# Run the bot
python slack_bot.py
```

You should see:
```
🐆 Petit Panthère starting...
Connecting to Slack...
✅ Petit Panthère is online! Send me a message in Slack.
```

---

## Step 5: Test It

1. Open Slack
2. Go to **Apps** in sidebar
3. Find **Petit Panthère**
4. Send a DM: `"Hello!"`

The bot should respond! 🎉

**Try these commands:**
- `"Add task: film workout video"`
- `"What can you do?"`
- `"Tell me about your architecture"`

---

## Troubleshooting

### Error: "SLACK_BOT_TOKEN not set"
- Make sure `.env` file exists (copy from `.env.example`)
- Check that you saved the file after editing
- Restart the bot

### Error: "Invalid token"
- Double-check you copied the full token (no extra spaces)
- Make sure you're using the **Bot User OAuth Token** (xoxb-), not the signing secret

### Bot doesn't respond to messages
- Check Socket Mode is enabled in Slack app settings
- Verify you subscribed to `message.im` event
- Make sure the bot is installed to your workspace (reinstall if needed)

### Error: "429 Too Many Requests" (Claude API)
- You hit rate limit. Wait a minute and try again.
- Consider using Claude Sonnet instead of Opus (cheaper, faster)

### Bot responds twice
- Probably subscribed to both `message.im` and `message.channels` events
- Remove `message.channels` if you only want DMs

---

## Stopping the Bot

Press **Ctrl+C** in the terminal.

---

## Denver Demo Tips

**Keep the bot running during your trip:**

Option 1: **Run on laptop during demos**
- Before showing: `cd petit-panthere && source venv/bin/activate && python slack_bot.py`
- Keep terminal window open
- Demo in Slack on phone

Option 2: **Deploy to Railway** (always-on)
- Create Railway account (free tier)
- Connect GitHub repo
- Set environment variables in Railway dashboard
- Bot runs 24/7 even when laptop is closed

**Demo flow:**
1. Pull up Slack on phone
2. Send message to Petit Panthère
3. Show response
4. Explain: "That's the agent loop. Slack → Claude → Response. Next step is adding tool integrations."

---

## Next Steps (Post-Demo)

Once basic bot works, you can extend it:

1. **Add memory:** Store conversation history in SQLite
2. **Add task tool:** Integrate with Google Sheets
3. **Add scheduling:** APScheduler for autonomous check-ins
4. **Build dashboard:** React UI for visual task management

See [ROADMAP.md](ROADMAP.md) for full development plan.

---

## Security Note

**Never share your tokens publicly!**

- Don't commit `.env` to git
- Don't screenshot tokens
- Don't paste in public Slack channels
- Rotate tokens if accidentally exposed

---

**Questions? Check the docs or ask Katarina!** 🐾

*Last updated: 2026-02-15*
