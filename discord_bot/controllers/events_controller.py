from views import responses

def setup(bot):
    @bot.event
    async def on_ready():
        print(f"{bot.user.name} is now online!")
        
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        # Allow commands to be processed
        await bot.process_commands(message)
