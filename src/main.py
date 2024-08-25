import discord, asyncio, sacuma
from discord.ext import commands
from etc import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def main():
    @bot.event
    async def on_ready():
        await bot.tree.sync()
    asyncio.run(bot.add_cog(sacuma.Sacuma(bot)))
    bot.run(TOKEN)
    
if __name__ == "__main__":
    main()