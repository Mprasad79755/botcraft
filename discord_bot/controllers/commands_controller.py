from discord.ext import commands
from views import responses

def setup(bot):
    @bot.command(name="calcy")
    async def calculate(ctx, expression: str):
        try:
            result = eval(expression)  # Warning: eval can be unsafe in production
            await ctx.send(responses.result_message(result))
        except Exception as e:
            await ctx.send(responses.error_message(str(e)))

    @bot.command(name="about")
    async def about(ctx):
        await ctx.send(responses.about_message())
