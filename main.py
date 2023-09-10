import os
import nextcord
from nextcord.ext import commands
import sqlite3


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
AuthorID = 440057700697767947



#Значение в кавычках указывает название активности
activity = nextcord.Game(name="Base for bots")
#можно сменить префикс на свой. просто измени значение последней переменной (command_prefix)
client = nextcord.ext.commands.Bot(activity=activity, intents=intents, status=nextcord.Status.online, command_prefix="!")


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        client.load_extension(f"cogs.{fn[:-3]}")


@client.event
async def on_message(message):
    user = message.author
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM users WHERE mention = ?", (str(user),))
    data = cursor.fetchone()
    if data is None:
        cursor.execute('INSERT INTO users (mention, exp, warns) VALUES (?, ?, ?)', (str(user), 1, 0))
        conn.commit()
        conn.close()
    elif len(message.clean_content) >= 5:
        cursor.execute("SELECT * FROM users WHERE mention = ?", (str(user),))
        for row in cursor:
            result = row[1]
        result += 1
        if (result % 500 == 0) and (result < 1502):
            await user.send(f'Поздравляем с достижением {result // 100} уровня! используйте !claim, чтобы забрать награду')
        cursor.execute('''UPDATE users SET exp = ? WHERE mention = ?''', (int(result), str(user),))
        conn.commit()
        conn.close()
    await client.process_commands(message)



@client.command(name="author")
async def getcraetor(ctx):
    Creator = await client.fetch_user(AuthorID)
    crembed = nextcord.Embed(title=Creator.name,
                             description="Contact me if you want to add custom discord bot on your server! https://t.me/spiritlz",
                             color=0x00fbff)
    crembed.set_image(url=Creator.avatar.url)
    await ctx.send(embed=crembed)


@client.command(name="server")
async def servinfo(ctx):
    guild = ctx.message.author.guild
    embed = nextcord.Embed(title=guild.name, color=nextcord.Color.blurple())
    ServerData = {
        "Владелец": guild.owner.mention,
        "Каналов": len(guild.channels),
        "Участников": guild.member_count,
        "Создана": guild.created_at.strftime("%b, %d, %Y, %T")
    }
    for [fieldName, fieldVal] in ServerData.items():
        embed.add_field(name=fieldName + ":", value=fieldVal, inline=True)
    embed.set_footer(text=f"id: {guild.id}")
    embed.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    embed = nextcord.Embed(color=nextcord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        embed.title = "Такой комманды не существует"
        embed.description = "Проверьте не опечатались ли вы"
        await ctx.send(embed=embed)


if __name__ == '__main__':
    client.run("MTEzNjk5OTUyODc5NzU4MTM0Mg.G1tOBy.sGGAjvgxW_ZlTnUREM76Lc53winVcqz4PcFE6Y")
