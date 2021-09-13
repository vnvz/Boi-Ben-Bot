import discord, youtube_dl
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # musicas
        self.is_playing = False

        # array das músicas
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'nonplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch: %s" %item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # pegar a primeira url
            m_url = self.music_queue[0][0]['source']

            # remover o primeiro elemento, já que ele está sendo tocado
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            # conectar ao canal de voz
            if self.vc == "" or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
            else:
                self.vc = await self.bot.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            # remover o primeiro elemento, já que ele está sendo tocado
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # confirmar se o usuário está conectado a um canal de voz
            await ctx.send("Conecte-se a um canal de voz!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Não foi possível reproduzir a música. Provavelmente porquê é uma playlist ou uma stream.")
            else:
                await ctx.send("Música adicionada à fila!")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Não há música na fila.")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            # tentar tocar a próxima música na fila, se existir uma
            await self.play_music()

    @commands.command()
    async def stop(self, ctx):
        if self.vc != "":
            self.vc.stop()

    @commands.command()
    async def loop(self, ctx): # comando de teste do loop
        if self.vc != "":
            self.vc.loop()
        