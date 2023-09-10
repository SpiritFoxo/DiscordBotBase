import datetime
import nextcord
from nextcord.ext import commands
import humanfriendly
import sqlite3



class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Mute
    @commands.command(name="mute")
    @commands.has_guild_permissions(deafen_members=True)
    async def mute(self, ctx, member: nextcord.Member, time, reason):
        time = humanfriendly.parse_timespan(time)
        await member.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time))
        if reason is None:
            await ctx.send(f"{member.mention} был отправлен отправлен подумать о своем поведении")
        else:
            await ctx.send(f"{member.mention} был отправлен отправлен подумать о своем поведении по причине {reason}")

    @mute.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('Недостаточно прав или такого пользователя не существует')

    # Unmute
    @commands.command(name="unmute")
    @commands.has_guild_permissions(deafen_members=True)
    async def unmute(self, ctx, member: nextcord.Member):
        await member.edit(timeout=None)
        await ctx.send(f"{member.mention} больше не в муте")

    @unmute.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('Недостаточно прав или такого пользователя не существует')

    # Ban
    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: nextcord.Member = None, *, reason=None):
        if user is None:
            await ctx.send("укажите имя пользователя")
            return
        await user.ban(reason=reason)
        await ctx.send(f"@{ctx.author} забанил пользователя {user.name} по причине {reason}")

    @ban.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('Недостаточно прав или такого пользователя не существует')

    # Kick
    @commands.command(name="kick")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: nextcord.Member = None, *, reason=None):
        if user is None:
            await ctx.send("укажите имя пользователя")
            return
        await user.kick(reason=reason)
        await ctx.send(f"@{ctx.author} кикнул пользователя {user.name} по причине {reason}")

    @kick.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('Недостаточно прав или такого пользователя не существует')

    # warn
    @commands.command(name='warn')
    @commands.has_guild_permissions(kick_members=True)
    async def warn(self, ctx, user: nextcord.Member = None):
        if user is None:
            await ctx.send("Укажите имя пользователя")
            return
        name = user.name + '#' + user.discriminator
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE mention = ?", (name,))
        for row in cursor:
            result = row[2]
        result += 1
        if result < 3:
            cursor.execute('''UPDATE users SET warns = ? WHERE mention = ?''', (int(result), name,))
            conn.commit()
            conn.close()
            if result == 1:
                await ctx.send(f'Теперь у юзера {user.mention} {result} предупреждение из 3')
            else:
                await ctx.send(f'Теперь у юзера {user.mention} {result} предупреждения из 3')
        else:
            cursor.execute('DELETE FROM users WHERE mention = ?', (name,))
            conn.commit()
            conn.close()
            await user.kick(reason='вы достигли лимита предупреждений')

    @warn.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('Недостаточно прав или такого пользователя не существует')

    # unwarn
    @commands.command(name='unwarn')
    @commands.has_guild_permissions(kick_members=True)
    async def unwarn(self, ctx, user: nextcord.Member = None):
        if user is None:
            await ctx.send("Укажите имя пользователя")
            return
        name = user.name + '#' + user.discriminator
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE mention = ?", (name,))
        for row in cursor:
            result = row[2]
        result = result - 1
        if result != 0:
            cursor.execute('''UPDATE users SET warns = ? WHERE mention = ?''', (int(result), name,))
            conn.commit()
            conn.close()
            if result == 1:
                await ctx.send(f'Теперь у юзера {user.mention} {result} предупреждение')
            else:
                await ctx.send(f'Теперь у юзера {user.mention} отсутствуют предупреждения')

        else:
            await ctx.send('У выбранного пользователя нет предупреждений')

    @unwarn.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('Недостаточно прав или такого пользователя не существует')

    # Get profile
    @commands.command(name='profile')
    async def profile(self, ctx, user: nextcord.Member = None):
        if user is None:
            user = ctx.author
            name = user.name + '#' + user.discriminator
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE mention = ?", (name,))
            for row in cursor:
                currentexp = row[1]
                warnscount = row[2]
            conn.close()
            level = currentexp // 100
            hundreeds = currentexp // 100
            currentexp = currentexp - hundreeds * 100
            exptonewlevel = 100 - currentexp
            useravatar = user.avatar.url

            embed = nextcord.Embed(title='Профиль пользователя ' + user.display_name + '!', color=0x00ccff)
            embed.set_thumbnail(url=useravatar)
            embed.add_field(name="Опыта до следующего уровня:", value=exptonewlevel, inline=True)
            embed.add_field(name="Текущий Уровень:", value=level, inline=True)
            embed.add_field(name="Количество предупреждений:", value=warnscount, inline=True)
            await ctx.send(embed=embed)
        else:
            name = user.name + '#' + user.discriminator
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE mention = ?", (name,))
            for row in cursor:
                currentexp = row[1]
                warnscount = row[2]
            conn.close()
            level = currentexp // 100
            hundreeds = currentexp // 100
            currentexp = currentexp - hundreeds * 100
            exptonewlevel = 100 - currentexp
            useravatar = user.avatar.url

            embed = nextcord.Embed(title='Профиль пользователя ' + user.display_name + '!', color=0x00ccff)
            embed.set_thumbnail(url=useravatar)
            embed.add_field(name="Опыта до следующего уровня:", value=exptonewlevel, inline=True)
            embed.add_field(name="Текущий Уровень:", value=level, inline=True)
            embed.add_field(name="Количество предупреждений:", value=warnscount, inline=True)
            await ctx.send(embed=embed)

    # set exp
    @commands.command(name='setexp')
    @commands.has_guild_permissions(manage_roles=True)
    async def setexp(self, ctx, exp, user: nextcord.Member = None):
        if user is None:
            user = ctx.author
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE mention = ?", (str(user),))
            cursor.execute('''UPDATE users SET exp = ? WHERE mention = ?''', (int(exp), str(user),))
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE mention = ?", (str(user),))
            cursor.execute('''UPDATE users SET exp = ? WHERE mention = ?''', (int(exp), str(user),))
            conn.commit()
            conn.close()
        await ctx.send(f'Количество опыта у участника {user} изменено на {exp}')

    # role for exp
    @commands.command(name='claim')
    async def claimrole(self, ctx, user: nextcord.Member = None):
        if user is None:
            user = ctx.author
            guild = ctx.message.author.guild

            #role list
            role5 = ctx.guild.get_role(974352220512485446)
            role10 = ctx.guild.get_role(1139203641014755338)
            role15 = ctx.guild.get_role(1139203723176976476)

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE mention = ?", (str(user),))
            for row in cursor:
                currentexp = row[1]
            conn.close()
            #for 5 lvl
            if 500 < currentexp < 1000:
                await user.add_roles(role5)
            #for 10 lvl
            if 1000 < currentexp < 1500:
                await user.add_roles(role10)
            #for 15 lvl
            if 1500 < currentexp:
                await user.add_roles(role15)
            else:
                await ctx.send('У вас недостаточно опыта для получения роли')


def setup(bot):
    bot.add_cog(Moderation(bot))
