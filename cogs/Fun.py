import nextcord
from nextcord.ext import commands
import aiohttp
import random



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#foxes sender
    @commands.command(name="fox")
    async def sendfoxpic(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://randomfox.ca/floof')
            foxjson = await request.json()
            embed = nextcord.Embed(title="Foxo!", color=nextcord.Color.orange())
            embed.set_image(url=foxjson['image'])
            await ctx.send(embed=embed)

#gay meter
    @commands.command(name="gay")
    async def checkgayness(self, ctx, user: nextcord.Member = None):
        percent = random.randint(0, 100)
        if user is None:
            user = ctx.author
            await ctx.send(f"{user.mention} гей на {percent}%")
        else:
            await ctx.send(f"{user.mention} гей на {percent}%")

#stick
    @commands.command(name="stick")
    async def stickmeter(self, ctx, user: nextcord.Member = None):
        lenght = random.randint(1, 100)
        lenght2 = random.randint(0, 25)
        lenght3 = random.randint(0, 15)
        totallenght = (lenght+lenght2+lenght3)/3
        roundlenght = round(totallenght, 1)
        if user is None:
            user = ctx.author
            await ctx.send(f"Длина пользователя {user.mention} - {roundlenght}см")
            if roundlenght > 20:
                await ctx.send('Таким и убить можно!')
        else:
            await ctx.send(f"Длина пользователя {user.mention} - {roundlenght}см")
            if roundlenght > 20:
                await ctx.send('Таким и убить можно!')

#booba
    @commands.command(name="boobs")
    async def boobmeter(self, ctx, user: nextcord.Member = None):
        size1 = random.randint(1, 10)
        size2 = random.randint(0, 5)
        sizesum = (size1+size2)/2
        totalsize = round(sizesum, 1)
        if user is None:
            user = ctx.author
            await ctx.send(f"Размер груди пользователя {user.mention} - {totalsize}")
            if totalsize > 6:
                await ctx.send('Твоя спина точно целая?')
        else:
            await ctx.send(f"Размер груди пользователя {user.mention} - {totalsize}")
            if totalsize > 20:
                await ctx.send('Твоя спина точно целая?')

#pfp
    @commands.command(name="pfp")
    async def getpfp(self, ctx, user: nextcord.Member = None):
        if user is None:
            await ctx.send("Введите имя пользователя")
        else:
            UserAvatar = user.avatar.url
            avaEmbed = nextcord.Embed(title=f"Аватар пользователя {user.display_name}")
            avaEmbed.set_image(url=UserAvatar)
            await ctx.send(embed=avaEmbed)

#8ball
    @commands.command(name="ball")
    async def predict(self, ctx):
        descision = random.randint(0, 1)
        if descision == 1:
            await ctx.send("Да")
        else:
            await ctx.send("Нет")

#height
    @commands.command(name='height')
    async def height(self, ctx, user: nextcord.Member = None):
        hght = random.randint(100, 250)
        hght = hght / 100
        if user is None:
            user = ctx.author
            await ctx.send(f"Рост пользователя {user.mention} - {hght}м")
        else:
            await ctx.send(f"Рост пользователя {user.mention} - {hght}м")

#random
    @commands.command(name='rand', )
    async def rand(self, ctx, a: int, b: int):
        number = random.randint(a, b)
        await ctx.send(number)



def setup(bot):
    bot.add_cog(Fun(bot))