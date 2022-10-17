# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
import datetime
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)


date_object = datetime.date.today()
date_object = str(date_object)
monthsofyear = ["January", "February",'March','April','May','June','July','August','September','October','November','December']
dateotoday = date_object.split('-')
print(dateotoday)
if dateotoday[2][0] == '0':
    day = dateotoday[2][1]
else:
    day = dateotoday[2]
todaysdate = f'{monthsofyear[int(dateotoday[1])-1]} {day}'
print(todaysdate)




#birthday class
class Birthday:
    def __init__(self,name,month,day):
        self._name = name
        self._birthday = f"{month} {day}"
    def get_name(self):
        return self._name
    def get_birthday(self):
        return self._birthday

#place all birthdays in dict
birthdaylist = []
birthdayfile = open('birthdays.csv','r')
for line in birthdayfile:
    if line[0] != '#':
        line = line.strip('\n')
        line = line.split(',')
        monthandday = line[1].split(' ')
        bday = Birthday(line[0],monthandday[0],monthandday[1])
        birthdaylist.append(bday)

for obj in birthdaylist:
    print(obj.get_name())

date_object = datetime.date.today()
date_object = str(date_object)
monthsofyear = ["January", "February",'March','April','May','June','July','August','September','October','November','December']
dateotoday = date_object.split('-')
print(dateotoday)
if dateotoday[2][0] == '0':
    day = dateotoday[2][1]
else:
    day = dateotoday[2]
todaysdate = f'{monthsofyear[int(dateotoday[1])-1]} {day}'
print(todaysdate)
for obj in birthdaylist:
    if obj.get_birthday() == todaysdate:
        print("Birthday Found!")

@tasks.loop(hours=12)
async def checkbirthdayandping():
    channel = bot.get_channel(1026643743136301087)
    await channel.send('THIS IS WORKING!')
    date_object = datetime.date.today()
    date_object = str(date_object)
    monthsofyear = ["January", "February",'March','April','May','June','July','August','September','October','November','December']
    dateotoday = date_object.split('-')
    print(dateotoday)
    if dateotoday[2][0] == '0':
        day = dateotoday[2][1]
    else:
        day = dateotoday[2]
    todaysdate = f'{monthsofyear[int(dateotoday[1])-1]} {day}'
    print(todaysdate)
    for obj in birthdaylist:
        if obj.get_birthday() == todaysdate:
            print("Birthday Found!")
            fileopen = open('userlist.csv','r')
            for user in users:
                await channel.send(f'{user.mention} Today is {obj.get_name()} birthday')
            
            
#global userlist
users = []

#add a user to the list of pings. may need to be changed into a file later
@bot.command()
async def adduser(ctx):
    fileopen = open('userlist.csv','a')
    fileopen.write(f'{ctx.author}\n')
    users.append(ctx.author)
    fileopen.close()
    await ctx.send('User added!')

#return a list of users
@bot.command()
async def getusers(ctx):
    fileopen = open('userlist.csv','a')
    for user in users:
        await ctx.send(user.mention)
    fileopen.close()
    
def ping_users(users):
    pass
    
#returns all the birthdays in the list
@bot.command()
async def listbirthday(ctx):
    birthdayfile = open('birthdays.csv','r')
    for line in birthdayfile:
        if line[0] != '#':
            await ctx.send(line)
    birthdayfile.close()

#add a birthday to the file
@bot.command()
async def addbirthday(ctx):
    birthdayfile = open('birthdays.csv','a')
    months = ["january", "february",'march','april','may','june','july','august','september','october','november','december']
    await ctx.send("Please Enter a Name")
    # This will make sure that the response will only be registered if the following conditions are met:
    def checkname(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    name = await bot.wait_for("message", check=checkname)
    await ctx.send("Please Enter a Month and Day")
    def checkdate(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel \
        and msg.content[0:(msg.content.index(' '))].lower() in months and \
        int(msg.content[(msg.content.index(' '))+1:]) in range(1,31)
    date = await bot.wait_for('message',check=checkdate)
    await ctx.send(date.content)
    birthdayfile.write(f'{name.content},{date.content}\n')
    datesplit = date.content.split(' ')
    bday = Birthday(name.content,datesplit[0],datesplit[1])
    birthdaylist.append(bday)
    await ctx.send('Done!')
    birthdayfile.close()

#just tells me if the bot has connected
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    checkbirthdayandping.start()

#ping!
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

#some testing code
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday!')

    elif message.content == 'raise-exception':
        raise discord.DiscordException 
    
    await bot.process_commands(message)



bot.run(TOKEN)



