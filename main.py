import discord
import requests
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
import os
import youtube_dl
from youtube_search import YoutubeSearch
from TOKEN import *
from asyncio import sleep
import json
import sqlite3
from discord_components import Button,DiscordComponents,ButtonStyle

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.' , intents = intents)
conn = sqlite3.connect("Discord.sql")
cursor = conn.cursor()
print(f"SQlite v {sqlite3.sqlite_version}")

# функция для боздания бд
def data():

    cursor.execute("""CREATE TABLE "users" (
                "id"	INT,
                "nickname"	TEXT,
                "mention"	TEXT,
                "account"	TEXT,
                "steam"  TEXT,
                "vk"  TEXT,
                "lvl"	INT
            )""")
    conn.commit()
#data()
#^
#|
#|
#Убрать комментарий в случаи отсутствия БД

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x01140))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    DiscordComponents(bot)
    for guild in bot.guilds:
        print(guild.id)
        serv=guild
        for member in guild.members:
            cursor.execute(f"SELECT id FROM users where id={member.id}")
            if cursor.fetchone()==None:
                cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>','S','S','S',0)")
            else:
                pass
            conn.commit()
@bot.event
async def on_member_join(member):
    cursor.execute(f"SELECT id FROM users where id={member.id}")
    if cursor.fetchone()==None:
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>','S','S','S',0)")
    else:
        pass
    conn.commit()

@bot.command()
async def add(ctx ,service,teg):
    uid = ctx.author.id
    if service == "faceit":
        if cursor.execute(f"UPDATE users SET account=? where id=?", (teg,uid)):
            await ctx.send(f"[LOG] ADD FACEIT PROFILE")
        else:
            await ctx.send(f"[LOG] NOT ADD ACCOUNT")
    elif service == "steam":
        if cursor.execute(f"UPDATE users SET steam=? where id=?", (teg,uid)):
            await ctx.send(f"[LOG] ADD STEAM PROFILE")
        else:
            await ctx.send(f"[LOG] NOT ADD ACCOUNT")
    elif service == "vk":
        if cursor.execute(f"UPDATE users SET vk=? where id=?", (teg,uid)):
            await ctx.send(f"[LOG] ADD VK PROFILE")
        else:
            await ctx.send(f"[LOG] NOT ADD ACCOUNT")
    else:
        await ctx.send(f"[LOG] ШО ЗА ХУЙНЯ ???")
    conn.commit()

@bot.command()
async def account(ctx):

    for row in cursor.execute(f"SELECT nickname,lvl,account,steam,vk FROM users where id={ctx.author.id}"):
        embed = discord.Embed(title="Данные:", color=discord.Color.red())
        embed.add_field(name=ctx.author.name,value=ctx.author.id,inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(
            embed = embed,
            components = [
                Button(style=ButtonStyle.URL, label="FACEIT", url="https://www.faceit.com/ru/players/" + row[2]),
                Button(style=ButtonStyle.URL, label="STEAM", url="https://steamcommunity.com/id/" + row[3]),
                Button(style=ButtonStyle.URL, label="VK", url="https://vk.com/" + row[4])
            ]
        )

@bot.command()
async def oldplay(ctx , *,zapr ):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Ты не законектился придурок")
        return
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.send('Реконекта не требует 🙂')
    else:
        voice = await channel.connect()
        await ctx.send(f"Канал {channel}")
    result = YoutubeSearch(zapr, max_results=1).to_dict()
    res = result[0]['url_suffix']
    title = result[0]['title']
    icon = result[0]['thumbnails'][0]
    url = "https://www.youtube.com" + res
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send('⛔ Дождитесь окончания текущего воспроизведения трека или воспользуйтесь командой ".stop"⛔')
        return
    await ctx.send("🎶 Готовлю все, скоро начну воспроизведение музыки 🎶")
    print("Кто-то хочет играть музыку, позвольте мне приготовить для них это ...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.add_field(name="URL", value=url, inline=False)
    embed.set_image(url=icon)
    await ctx.send(embed = embed)

@bot.command()
async def hello(ctx):

    author = ctx.message.author

    await ctx.send(
        f'Привет, {author.mention}!')

@bot.command()
@commands.has_permissions(view_audit_log=True)
async def ban(ctx ,member:discord.Member,reason:str):
    embed = discord.Embed(title=f'Пользователь {member} получил бан',color=0xFF64C8)
    embed.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
    embed.add_field(name="Нарушитель", value=member.mention, inline=False)
    embed.add_field(name="Причина", value=reason, inline=False)
    await member.ban(reason=reason)
    await ctx.send(embed=embed)

@bot.command()
async def members(ctx):
    server_members = ctx.guild.members
    data = "\n".join([i.name for i in server_members])
    embed = discord.Embed(title=f'Участники сервера', description=f"{data}", color=discord.Color.green())

    await ctx.send(embed=embed)

@bot.command()
async def myroles(ctx):
    member = ctx.message.author
    member_roles = "\n".join([i.name for i in member.roles])
    embed = discord.Embed(title=f'Список ролей', description=f"{member_roles}", color=discord.Color.dark_green())
    await ctx.send(embed=embed)


@bot.command()
async def stop(ctx):
    global voice
    voice.stop()
    await ctx.send("🔈 Off 🔈")

@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Линул из {channel}")
    else:
        await ctx.send("Не думайте, что я нахожусь в голосовом канале")

@bot.command()
async def faceit(ctx , nick: str):
    uid = ctx.author.id
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(faceit_api),
    }

    if nick == "*":
        for row in cursor.execute(f"SELECT account FROM users where id={uid}"):
            nick = row[0]
    else:
        nick = nick
    params = (
        ('nickname', nick),
        ('game', 'csgo'),
    )

    response = requests.get('https://open.faceit.com/data/v4/players', headers=headers , params = params)

    data = response.json()


    if data['games']['csgo']['faceit_elo'] > 1100:
        col = 0xff9900
    if data['games']['csgo']['faceit_elo'] < 1101:
        col = 0x0015F300
    if data['games']['csgo']['faceit_elo'] > 1701:
        col = 0x00F30A0D
    if data['games']['csgo']['faceit_elo'] < 801:
        col = 0x00E8F7FF

    elo = data['games']['csgo']['faceit_elo']
    lvl = data['games']['csgo']['skill_level']
    name = data['nickname']
    avatar = data['avatar']
    player_id = data['player_id']

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer d062b0f9-0b54-4df0-95c9-6e4df9dc0e54',
    }

    response = requests.get('https://open.faceit.com/data/v4/players/'+player_id+'/stats/csgo',
                            headers=headers)
    data = response.json()
    kd = data["lifetime"]["Average K/D Ratio"]
    hs = data["lifetime"]["Average Headshots %"]
    winrate = data["lifetime"]["Win Rate %"]

    embed = discord.Embed(color=col, title='Stats' , description = f"ELO: {elo}\nK/D: {kd}\nHS: {hs}%\nWin Rate: {winrate}%")

    if lvl == 1:
       file = discord.File("lvl/level_1.png", filename="level_1.png")
       embed.set_author(name=name, icon_url='attachment://level_1.png')
    if lvl == 2:
        file = discord.File("lvl/level_2.png", filename="level_2.png")
        embed.set_author(name=name, icon_url='attachment://level_2.png')
    if lvl == 3:
        file = discord.File("lvl/level_3.png", filename="level_3.png")
        embed.set_author(name=name, icon_url='attachment://level_3.png')
    if lvl == 4:
        file = discord.File("lvl/level_4.png", filename="level_4.png")
        embed.set_author(name=name, icon_url='attachment://level_4.png')
    if lvl == 5:
        file = discord.File("lvl/level_5.png", filename="level_5.png")
        embed.set_author(name=name, icon_url='attachment://level_5.png')
    if lvl == 6:
        file = discord.File("lvl/level_6.png", filename="level_6.png")
        embed.set_author(name=name, icon_url='attachment://level_6.png')
    if lvl == 7:
        file = discord.File("lvl/level_7.png", filename="level_7.png")
        embed.set_author(name=name, icon_url='attachment://level_7.png')
    if lvl == 8:
        file = discord.File("lvl/level_8.png", filename="level_8.png")
        embed.set_author(name=name, icon_url='attachment://level_8.png')
    if lvl == 9:
        file = discord.File("lvl/level_9.png", filename="level_9.png")
        embed.set_author(name=name, icon_url='attachment://level_9.png')
    if lvl == 10:
        file = discord.File("lvl/level_max.png", filename="level_max.png")
        embed.set_author(name=name, icon_url='attachment://level_max.png')

    if avatar == '':
        embed.set_thumbnail(url='https://assets.faceit-cdn.net/hubs/avatar/1b588a32-e207-4596-80b9-a2ff9eabf28d_1607167905245.jpg')
    else:
        embed.set_thumbnail(url=avatar)

    await ctx.send(file = file, embed=embed,components =
    [
                Button(style=ButtonStyle.URL, label="FACEIT",url="https://www.faceit.com/ru/players/" + nick)
    ])


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.command()
async def play(ctx, *,zapr):

    print('Запрос: {}'.format(zapr))
    result = YoutubeSearch(zapr, max_results=1).to_dict()
    res = result[0]['url_suffix']
    title = result[0]['title']
    icon = result[0]['thumbnails'][0]
    url = "https://www.youtube.com" + res


    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("**Ты не законектился придурок**")
        return
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        pass
    else:
        voice = await channel.connect()
        await ctx.send(f"**Канал** {channel}")
    try:
        voice_channel = ctx.message.author.voice.channel
        voice = await voice_channel.connect()

    except:
        print('Уже подключен или не удалось подключиться')

    if voice.is_playing():
        pass
    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\ffmpeg.exe", source=URL,**FFMPEG_OPTIONS))
        embed = discord.Embed(title=title, color=discord.Color.red())
        embed.add_field(name="**URL**", value=url, inline=False)
        embed.set_image(url=icon)
        await ctx.send(embed=embed)
        while voice.is_playing():
            await sleep(1)
        if not voice.is_stop():
            await voice.disconnect()

@bot.command()
async def pause(ctx):
    global voice
    voice.pause()
    print("[ffmpeg] Pause")
    await ctx.send(":pause_button: **Pause**")

@bot.command()
async def info(ctx,member:discord.Member = None, guild: discord.Guild = None):
    await ctx.message.delete()
    if member == None:
        emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
        emb.add_field(name="Имя:", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=ctx.message.author.id,inline=False)
        t = ctx.message.author.status
        if t == discord.Status.online:
            d = " В сети"

        t = ctx.message.author.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = ctx.message.author.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = ctx.message.author.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"

        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="Информация о пользователе", color=member.color)
        emb.add_field(name="Имя:", value=member.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=member.id,inline=False)
        t = member.status
        if t == discord.Status.online:
            d = " В сети"

        t = member.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = member.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = member.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"
        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=member.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)


@bot.command()
async def playlist(ctx):
    with open("music.json") as f:
        data_a = json.load(f)
        result = data_a
        result1 = YoutubeSearch(data_a[0], max_results=1).to_dict()
        result2 = YoutubeSearch(data_a[1], max_results=1).to_dict()
        res1 = result1[0]['url_suffix']
        res = result2[0]['url_suffix']
        title = result[0]['title']
        icon = result[0]['thumbnails'][0]
        url1 = "https://www.youtube.com" + res1

@bot.command()
async def resume(ctx):
    global voice
    voice.resume()
    print("[ffmpeg] **Resume**")
    await ctx.send(":play_pause: **Resume**")


bot.run(ds)
