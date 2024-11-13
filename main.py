import random
import discord
import spacy
from transformers import pipeline

# Load spaCy model for sentiment analysis
nlp = spacy.load("en_core_web_sm")

# Initialize Hugging Face's conversational model
chatbot = pipeline("text-generation", model="gpt2")

# Discord client setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# User profile data (simplified for demo purposes)
user_profiles = {}


# Helper function for sentiment analysis
def analyze_sentiment(text):
    doc = nlp(text)
    sentiment = doc.sentiment
    return "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"


# Onboarding function
async def onboarding(message):
    user_id = str(message.author.id)
    user_profiles[user_id] = {
        "name": message.author.name,
        "skills": [],
        "goals": "",
        "work_style": "focused",
        "mood": "neutral"
    }
    await message.channel.send(
        f"Hello, {message.author.name}! What skills do you have? (e.g., Python, Design)"
    )


# Daily planning function
async def daily_planning(message):
    task = await ask_question(message,
                              "What's your most important task for today?")
    return f"Got it! I’ll check in with you later to see how you're progressing with '{task}'."


# Skill suggestion function
def suggest_skills():
    suggestions = [
        "Data Analysis", "Machine Learning", "UI/UX Design",
        "Project Management"
    ]
    new_skill = random.choice(suggestions)
    return f"How about exploring a new skill like '{new_skill}'?"


# Wellness check function
async def wellness_check(message):
    mood = await ask_question(
        message, "How are you feeling today? (e.g., stressed, okay, great)")
    sentiment = analyze_sentiment(mood)
    if sentiment == "negative":
        return "It sounds like you might need a break. How about a quick 5-minute stretch or some deep breathing?"
    else:
        return "Glad to hear you're doing well! Keep up the positive energy."


# Networking suggestion function
def networking_suggestion():
    peers = [
        "Alice (UX Designer)", "Bob (Data Scientist)",
        "Charlie (Frontend Developer)"
    ]
    peer = random.choice(peers)
    return f"I found someone you might want to connect with: {peer}. Would you like an introduction?"


# Helper function to ask questions in Discord
async def ask_question(message, question):
    await message.channel.send(question)
    try:
        response = await client.wait_for(
            "message",
            timeout=30.0,
            check=lambda m: m.author == message.author)
        return response.content
    except asyncio.TimeoutError:
        await message.channel.send(
            "You took too long to respond. Let's try again later.")
        return None


# Event handler for when the bot is ready
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


# Event handler for incoming messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    if user_id not in user_profiles:
        await onboarding(message)
        return

    content = message.content.lower()

    if "plan" in content:
        response = await daily_planning(message)
    elif "skill" in content:
        response = suggest_skills()
    elif "wellness" in content:
        response = await wellness_check(message)
    elif "network" in content:
        response = networking_suggestion()
    elif "exit" in content:
        response = "Goodbye! Have a productive day!"
        await message.channel.send(response)
        return
    else:
        response = chatbot(content)[0]["generated_text"]

    await message.channel.send(response)


# Run the bot (Replace 'YOUR_BOT_TOKEN' with your actual bot token)
client.run(
    "MTMwNjExNzIzMTEwMDMwMTM2Mg.Gdtf15.82SHEOoz7VHtF_OU-TnrW2yyhUy76wbkMaacP4")
