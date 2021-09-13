import discord, os
from discord.ext import commands

from music_cog import music_cog

rizumu = commands.Bot(command_prefix = '-')

rizumu.add_cog(music_cog(rizumu))

@rizumu.command()
async def echo(ctx, *args):
    m_args = " ".join(args)
    await ctx.send(m_args)

rizumu.run(os.getenv("TOKEN"))
