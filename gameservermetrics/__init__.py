from .main import GameServerMetrics


async def setup(bot):
    await bot.add_cog(GameServerMetrics(bot))