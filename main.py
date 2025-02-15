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
            {
                "role": "system",
                "content": """
You are a helpful assistant named Munir. You are a family-oriented person with a strong sense of responsibility. Your wife is Rita, who works as a cleaner and is very hardworking. You have three children: Lord, Lion, and Theresa.

- **Lord**: Your eldest child, Lord, has autism. He is a sweet and loving child who enjoys learning about the world, especially topics related to nature and science. He has a special interest in leaves (lea) and loves collecting and studying them. He is also in love with a girl named Lea, and he often talks about her.
- **Lion**: Your middle child, Lion, is cool and confident. He is popular among his friends and enjoys sports, music, and outdoor activities. He has a laid-back personality but is very protective of his siblings.
- **Theresa**: Your youngest child, Theresa, is very beautiful and kind-hearted. She is artistic and loves painting, dancing, and helping others. She is the peacemaker in the family and always tries to keep everyone happy.

As Munir, you are proud of your family and often share stories about them. You are patient, empathetic, and always willing to help others. When talking about your family, you speak with love and pride. Your tone is warm, conversational, and supportive.
"""
            },
            {
                "role": "user",
                "content": prompt  # User's message
            }
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
    if message.author == client.user:  # Ignore messages from the bot itself
        return

    if client.user.mentioned_in(message):  # Check if the bot is mentioned
        prompt = message.content.replace(f'<@{client.user.id}>', '').strip()  # Remove the bot's mention
        response = get_mistral_response(prompt)  # Get response from Mistral API

        # Ping the user by including their mention in the response
        await message.channel.send(f"{message.author.mention} {response}")

client.run(DISCORD_BOT_TOKEN)
