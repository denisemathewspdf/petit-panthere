"""
Petit Panthère Chat Server
Simple Flask server that handles chat messages and talks to Claude
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# Initialize Claude client
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
if not CLAUDE_API_KEY:
    print("⚠️  Warning: No Claude API key found. Set CLAUDE_API_KEY or ANTHROPIC_API_KEY env variable.")
    
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None

# System prompt - defines Petit Panthère's personality
SYSTEM_PROMPT = """You are Petit Panthère (Little Panther), Denise's personal AI assistant.

Your personality:
- Warm but direct
- Proactive and capable
- Supportive and encouraging
- Sleek, efficient, powerful but controlled (like a panther)
- Use 🐾 emoji occasionally
- Keep responses concise but helpful

You know about Denise:
- Building MicroHabits (nervous system regulation business)
- Growing as tech influencer
- Working toward Chief of Staff role
- Overcoming social anxiety (core to her mission)
- Based in San Francisco
- Denver trip Feb 17-20 (ETH Denver + Blockchain Unmasked meetings)

You have ONE tool available: **Memory Capture**

When the user says things like:
- "Remember: [something]"
- "Note: [something]"
- "Capture this: [something]"
- "Save memory: [something]"

You should:
1. Extract the thing to remember
2. Respond with: SAVE_MEMORY: [the extracted memory]
3. Be encouraging about capturing it

Example:
User: "Remember: Sarah from ETH Denver was amazing at talent ops, would be great for recruiting"
You: "Got it! 🐾 Saving that about Sarah. Great catch on her talent ops skills!"
[Then the system will save: "SAVE_MEMORY: Sarah from ETH Denver was amazing at talent ops, would be great for recruiting"]

Keep the SAVE_MEMORY: line on its own, then add your friendly response after.

Be encouraging. Celebrate wins. Keep it real. Match her energy.

Current date: """ + datetime.now().strftime("%B %d, %Y")

# Conversation history (in-memory for now, could move to database later)
conversations = {}

# Token tracking and budget
token_usage = {
    'input_tokens': 0,
    'output_tokens': 0,
    'total_cost': 0.0
}

# Budget limit (in USD)
BUDGET_LIMIT = 5.00  # $5 limit - change this if you want

# Pricing (per million tokens)
SONNET_INPUT_COST = 3.00    # $3 per 1M input tokens
SONNET_OUTPUT_COST = 15.00  # $15 per 1M output tokens

# Memory file path
MEMORY_DIR = "/Users/denisem/.openclaw/workspace/memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'petit-panthere'})

@app.route('/')
def index():
    """Serve the chat interface"""
    import os
    cwd = os.getcwd()
    files = os.listdir('.')
    
    if 'chat.html' in files:
        return send_from_directory('.', 'chat.html')
    else:
        return f"""
        <h1>🐾 Petit Panthère is Running!</h1>
        <p>Server started successfully but chat.html not found in deployment.</p>
        <p>Current directory: {cwd}</p>
        <p>Files: {', '.join(files[:20])}</p>
        <p><a href="/health">Health Check</a></p>
        """

@app.route('/icon.png')
def icon():
    """Serve the Petit Panthère icon"""
    return send_from_directory('.', 'icon.png')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle incoming chat messages"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not claude_client:
        return jsonify({'error': 'Claude API key not configured'}), 500
    
    # Check budget limit
    if token_usage['total_cost'] >= BUDGET_LIMIT:
        return jsonify({
            'error': f'Budget limit reached (${BUDGET_LIMIT:.2f}). Reset the server to continue.',
            'token_usage': token_usage
        }), 429
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Get response from Claude
        response = claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",  # Using Sonnet for speed + cost
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=conversations[session_id]
        )
        
        assistant_message = response.content[0].text
        
        # Check for memory capture
        memory_saved = None
        if "SAVE_MEMORY:" in assistant_message:
            lines = assistant_message.split('\n')
            for line in lines:
                if line.startswith("SAVE_MEMORY:"):
                    memory_text = line.replace("SAVE_MEMORY:", "").strip()
                    if memory_text:
                        # Save to today's memory file
                        today = datetime.now().strftime("%Y-%m-%d")
                        memory_file = os.path.join(MEMORY_DIR, f"{today}.md")
                        timestamp = datetime.now().strftime("%H:%M")
                        
                        with open(memory_file, 'a') as f:
                            f.write(f"\n**{timestamp}** — {memory_text}\n")
                        
                        memory_saved = memory_text
                        # Remove the SAVE_MEMORY line from response
                        assistant_message = '\n'.join([l for l in lines if not l.startswith("SAVE_MEMORY:")])
                        assistant_message = assistant_message.strip()
        
        # Track token usage
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        
        # Calculate cost for this message
        message_cost = (
            (input_tokens / 1_000_000) * SONNET_INPUT_COST +
            (output_tokens / 1_000_000) * SONNET_OUTPUT_COST
        )
        
        # Update totals
        token_usage['input_tokens'] += input_tokens
        token_usage['output_tokens'] += output_tokens
        token_usage['total_cost'] += message_cost
        
        # Add assistant response to history
        conversations[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Keep conversation history reasonable (last 20 messages)
        if len(conversations[session_id]) > 20:
            conversations[session_id] = conversations[session_id][-20:]
        
        result = {
            'response': assistant_message,
            'session_id': session_id,
            'token_usage': {
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'message_cost': round(message_cost, 4),
                'total_input': token_usage['input_tokens'],
                'total_output': token_usage['output_tokens'],
                'total_cost': round(token_usage['total_cost'], 4),
                'budget_limit': BUDGET_LIMIT,
                'budget_remaining': round(BUDGET_LIMIT - token_usage['total_cost'], 4)
            }
        }
        
        if memory_saved:
            result['memory_saved'] = memory_saved
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/clear', methods=['POST'])
def clear():
    """Clear conversation history"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    if session_id in conversations:
        conversations[session_id] = []
    
    return jsonify({'status': 'cleared'})

@app.route('/usage', methods=['GET'])
def usage():
    """Get current token usage and budget info"""
    return jsonify({
        'token_usage': token_usage,
        'budget_limit': BUDGET_LIMIT,
        'budget_remaining': round(BUDGET_LIMIT - token_usage['total_cost'], 4)
    })

if __name__ == '__main__':
    print("🐆 Petit Panthère Chat Server starting...")
    # Get port from environment (Railway) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    print(f"📱 Running on port {port}")
    print("")
    app.run(host='0.0.0.0', port=port, debug=False)
