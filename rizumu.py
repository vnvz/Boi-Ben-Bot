<<<<<<< HEAD
import discord, os
from discord.ext import commands

from music_cog import music_cog

rizumu = commands.Bot(command_prefix = '-')

rizumu.add_cog(music_cog(rizumu))

@rizumu.command()
async def echo(ctx, *args):
    m_args = " ".join(args)
    await ctx.send(m_args)

#token = ""
#with open("token.txt") as file: 
#    token = file.read()

rizumu.run(os.getenv("TOKEN"))
=======
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
>>>>>>> 792316e870169ec41f91018b4df2f653f7361bc5
