import datetime, asyncio, random, string, discord, re
from discord.ext import commands
from discord import app_commands
from etc import *

class Sacuma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
        self.deleteCount = {}
        self.timeoutUserId = []
    async def deleteChannelName(self, channel:discord.abc.GuildChannel, deleteName:str, id:str):
        if deleteName in channel.name:
            try:
                await channel.delete()
                self.deleteCount[id][0] += 1
            except:
                self.deleteCount[id][1] += 1
    async def timeoutOrBan(self, member:discord.Member):
        until = datetime.datetime.now() + datetime.timedelta(days=7)
        try:
            if not member.id in self.timeoutUserId:
                self.timeoutUserId.append(member.id)
                await member.timeout(until)
            else:
                await member.ban(delete_message_days=7)
        except:
            pass
    def isSequentialUrl(self, messages:list[discord.Message]) -> bool:
        urls = []
        for message in messages:
            urls.append(re.findall(URL_PATTERN, message.content))
        for url in urls:
            if not len(url) == 0:
                return all(url == urls[0] for url in urls)
        return False
    def isSequentialMessage(self, messages:list[discord.Message]) -> bool:
        contents = []
        for message in messages:
            content = message.content
            content = re.compile(MEMTION_PATTERN).sub("", content)
            content = "\n".join([line for line in content.split('\n') if calcEntropy(line) <= ENTROPY_THRESHOLD])
            contents.append(content)
        return all(content == contents[0] for content in contents)
    @app_commands.command(name="help", description="Show help")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(HELP_MESSAGE, ephemeral=True)
    @app_commands.command(name="dc", description="Deletes all channels including the specified channel name.")
    async def deleteChannel(self, interaction: discord.Interaction, channelname:str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Error: You aren't Administrator", ephemeral=True)
            return
        id = "".join(random.choice(string.ascii_lowercase) for _ in range(12))
        self.deleteCount[id] = [0,0]
        await asyncio.gather(*(self.deleteChannelName(channel, channelname, id) for channel in interaction.guild.channels))
        await interaction.response.send_message(f"{self.deleteCount[id][0]} Success.\n{self.deleteCount[id][1]} Failed.", ephemeral=True)
    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        for channel in guild.text_channels:
            await channel.send(f"# Hi im Sacuma\nI can delete trolling Message/Channel.\n{HELP_MESSAGE}")
            break
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not str(message.guild.id) in self.messages:
            self.messages[str(message.guild.id)] = []
        self.messages[str(message.guild.id)].append(message)
        tempMessages = self.messages[str(message.guild.id)]
        if len(tempMessages) > 5:
            tempMessages = tempMessages[-6:]
        else:
            return
        checkResults = self.isSequentialMessage(tempMessages), self.isSequentialUrl(tempMessages)
        for result in checkResults:
            if result:
                try:
                    await asyncio.gather(*(self.timeoutOrBan(message.author) for message in tempMessages))
                    await asyncio.gather(*(message.delete() for message in tempMessages))
                except:
                    pass
                break