"""
Petit Panthère — Basic Slack Bot Demo
A minimal agent loop: Slack → LLM → Response

For Denver demo: Shows the core concept without full backend complexity.
"""

import os
import anthropic
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

# Load environment variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")  # Starts with xapp-
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

# Initialize clients
slack_client = WebClient(token=SLACK_BOT_TOKEN)
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# System prompt — defines the agent's personality and capabilities
SYSTEM_PROMPT = """You are Petit Panthère, a personal AI agent. Your name means "little panther" in French.

You are calm, capable, and supportive. You help your user (Denise) manage tasks, stay organized, and achieve her goals.

Right now you are a DEMO version. You can understand commands and respond helpfully, but you don't have access to real tools yet. When the user asks you to do something (like add a task), acknowledge it and explain what you would do once integrated with Google Sheets.

Be concise but warm. Use 🐾 emoji occasionally. Stay on brand: you're a panther — sleek, efficient, powerful but controlled.

Example interactions:
User: "Add task: film workout video"
You: "🐾 Got it! In the full version, I would add 'Film workout video' to your Google Sheet with priority p1 and due date today. Right now I'm in demo mode, but the architecture is ready for integration."

User: "What can you do?"
You: "Right now I'm a demo showing the agent loop: Slack → Claude → Response. Once fully built, I'll manage your tasks, schedule, emails, and more. Think of me as your personal Chief of Staff. 🐾"

Keep responses short (2-3 sentences usually). Be helpful and engaging.
"""


def get_agent_response(user_message: str) -> str:
    """
    Send user message to Claude and get response.
    This is the core "intelligence layer" of the agent.
    """
    try:
        message = claude_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ Error communicating with Claude: {str(e)}"


def process_message(client: SocketModeClient, req: SocketModeRequest):
    """
    Handle incoming Slack messages.
    This is the "interface layer" of the agent.
    """
    if req.type == "events_api":
        # Acknowledge the request
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        
        # Extract event data
        event = req.payload["event"]
        
        # Ignore messages from the bot itself
        if event.get("bot_id"):
            return
        
        # Only respond to direct messages or mentions
        if event.get("channel_type") != "im":
            # In channels, only respond if mentioned
            if f"<@{event.get('bot_id')}>" not in event.get("text", ""):
                return
        
        # Get user message
        user_message = event.get("text", "")
        channel = event.get("channel")
        
        # Get agent response from Claude
        agent_response = get_agent_response(user_message)
        
        # Send response back to Slack
        slack_client.chat_postMessage(
            channel=channel,
            text=agent_response
        )
        
        # Log for transparency (audit trail)
        print(f"[{event.get('user')}] {user_message}")
        print(f"[Petit Panthère] {agent_response}\n")


def main():
    """
    Start the Slack bot using Socket Mode.
    Socket Mode = no need for public URL/ngrok, easier for demos.
    """
    print("🐆 Petit Panthère starting...")
    print("Connecting to Slack...")
    
    # Create Socket Mode client
    socket_client = SocketModeClient(
        app_token=SLACK_APP_TOKEN,
        web_client=slack_client
    )
    
    # Register message handler
    socket_client.socket_mode_request_listeners.append(process_message)
    
    # Start listening
    socket_client.connect()
    
    print("✅ Petit Panthère is online! Send me a message in Slack.\n")
    
    # Keep running
    from threading import Event
    Event().wait()


if __name__ == "__main__":
    # Validate environment variables
    if not SLACK_BOT_TOKEN:
        print("❌ Error: SLACK_BOT_TOKEN not set")
        print("Get it from: https://api.slack.com/apps → OAuth & Permissions")
        exit(1)
    
    if not SLACK_APP_TOKEN:
        print("❌ Error: SLACK_APP_TOKEN not set")
        print("Get it from: https://api.slack.com/apps → Basic Information → App-Level Tokens")
        print("Make sure Socket Mode is enabled!")
        exit(1)
    
    if not CLAUDE_API_KEY:
        print("❌ Error: CLAUDE_API_KEY not set")
        print("Get it from: https://console.anthropic.com/")
        exit(1)
    
    # Start the bot
    main()
