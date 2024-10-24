import aiohttp
import discord
import asyncio
from redbot.core import commands
from redbot.core.bot import Red

class GameServerMetrics(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.api_url = None
        self.update_status_task = None

    def cog_unload(self):
        if self.update_status_task:
            self.update_status_task.cancel()

    async def update_status(self):
        while True:
            if not self.api_url:
                await asyncio.sleep(300)
                continue
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.api_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            player_count = data['data']['attributes']['players']
                            max_players = data['data']['attributes']['maxPlayers']
                            status_message = f"{player_count}/{max_players} players online"
                            await self.bot.change_presence(activity=discord.Game(name=status_message))
                        else:
                            print(f"Failed to fetch server data. Status code: {response.status}")
            except Exception as e:
                print(f"An error occurred while updating bot status: {e}")
            await asyncio.sleep(300)

    @commands.command()
    async def setapiurl(self, ctx, url: str):
        self.api_url = url
        await ctx.send(f"API URL has been updated to: {url}")
        if not self.update_status_task:
            self.update_status_task = self.bot.loop.create_task(self.update_status())

async def setup(bot: Red):
    await bot.add_cog(MyCog(bot))