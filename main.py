import discord
import requests
import os

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Get the token from environment variables
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')  # Get the API key from environment variables
MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def get_mistral_response(prompt):
    headers = {
        'Authorization': f'Bearer {MISTRAL_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'mistral-medium',  # Replace with the model you want to use
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant. Your name is Munir, your wife is Rita, she works as a cleaner. You have 3 kids, Lord, Lion, and Theresa. Lord has autism and loves lea. Lion is cool and Theresa is very beautiful.'},  # Personality instruction
            {'role': 'user', 'content': prompt}  # User's message
        ]
    }
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f'<@{client.user.id}>', '').strip()
        response = get_mistral_response(prompt)
        await message.channel.send(response)

client.run(DISCORD_BOT_TOKEN)
