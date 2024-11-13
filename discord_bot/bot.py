import discord
from discord.ext import commands
from config import TOKEN
from controllers import commands_controller, events_controller

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load controllers
commands_controller.setup(bot)
events_controller.setup(bot)

if __name__ == "__main__":
    bot.run(TOKEN)
