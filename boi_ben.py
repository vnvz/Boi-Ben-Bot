import discord, os
from discord.ext import commands

from music_cog import music_cog

boi_ben = commands.Bot(command_prefix = '-')

boi_ben.add_cog(music_cog(boi_ben))

@boi_ben.command()
async def echo(ctx, *args):
    m_args = " ".join(args)
    await ctx.send(m_args)

boi_ben.run(os.getenv("TOKEN"))