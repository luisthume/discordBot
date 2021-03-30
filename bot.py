import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.tasks import loop

import logging
import os
import requests
import json
import time
import re
import emoji

if os.environ.get('TOKEN'):
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = 'ODI0NDMwNjM5MDIwMjQ1MDAy.YFvQ3Q.SNVVxbsDaPvejbhCWPF0qTUXAVI'

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
intents = discord.Intents().all()
client = commands.Bot(command_prefix='?', intents=intents)

def nameToHours(member):
    emoji_dic = {
        '0' : '\U0001F55B',
        '1' : '\U0001F550',
        '2' : '\U0001F551',
        '3' : '\U0001F552',
        '4' : '\U0001F553',
        '5' : '\U0001F554',
        '6' : '\U0001F555',
        '7' : '\U0001F556',
        '8' : '\U0001F557',
        '9' : '\U0001F558'
    }
    request = requests.get('http://127.0.0.1/api/hours/code/{}'.format(member.id))
    if request.status_code == 200:
        request = request.json()
        hours = '{:02d}'.format(int(request['minutes']/60))
        #await message.channel.send('{}{}'.format(emoji_dic[hours[0]], emoji_dic[hours[1]]))
        if member.nick:
            nick = str(member.nick)
        else:
            nick = str(member.name)
        if nick[-1] in emoji_dic.values() and nick[-2] in emoji_dic.values():
            nick = nick[:-3]
            print(nick)
        return '{0} {1}{2}'.format(nick, emoji_dic[hours[0]], emoji_dic[hours[1]])
    else:
        print('Sem conexão')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_update(before, after):
    if str(before.status) == "online":
        if str(after.status) == "offline":
            timestr = time.strftime("%Y%m%d-%H%M%S")
            logging.info("{} has gone {} at date-time {}.".format(after.name,
                  after.status, timestr))
    if str(before.status) == "offline":
        if str(after.status) == "online":
            timestr = time.strftime("%Y%m%d-%H%M%S")
            logging.info("{} has arrived {} at date-time {}.".format(after.name,
                  after.status, timestr))


@loop(seconds=60)
async def runtime_background_task():
    await client.wait_until_ready()
    data = requests.get('http://127.0.0.1/api/users/').json()
    for guild in client.guilds:
        for member in guild.members:
            if str(member.id) in [i['code'] for i in data]:
                if str(member.status) == 'online':
                    requests.get('http://127.0.0.1/api/minutes/code/{}'.format(member.id))                    
            else:
                requests.post('http://127.0.0.1/api/users/', data={
                    "code": str(member.id),
                    "name" : str(member.name)
                })


@client.event
async def on_message(message):
    if message.content.startswith('!hours'):
        content = message.content.split(' ')
        if len(content) == 1 and content[0] == '!hours':
            request = requests.get('http://127.0.0.1/api/hours/code/{}'.format(message.author.id))
            if request.status_code == 200:
                request = request.json()
                minutes = request['minutes']
                await message.channel.send('{0} tem {1} horas no servidor!'.format(message.author.name, int(minutes/60)))
            else:
                await message.channel.send('Sem conexão com db')
        else:
            ids = [''.join(re.findall(r'[0-9]+', i)) for i in content][1:]
            for i in ids:
                data = requests.get('http://127.0.0.1/api/hours/code/{}'.format(i)).json()
                minutes = int(data['minutes'])
                name = data['name']
                await message.channel.send('{0} tem {1} horas no servidor!'.format(name, int(minutes/60)))

    if message.content.startswith('!updateName'):
        data = requests.get('http://127.0.0.1/api/users/?code={}'.format(message.author.id)).json()
        pk = data[0]['id']
        requests.patch('http://127.0.0.1/api/users/{}/'.format(pk), data={
            "name" : message.author.name
        })

    if message.content.startswith('!updateAllNames'):
        for guild in client.guilds:
            for member in guild.members:
                data = requests.get('http://127.0.0.1/api/users/?code={}'.format(member.id)).json()
                pk = data[0]['id']
                requests.patch('http://127.0.0.1/api/users/{}/'.format(pk), data={
                    "name" : member.name
                })

    if message.content.startswith('!hoursToName'):
        nick = nameToHours(message.author)
        await message.author.edit(nick=nick)


runtime_background_task.start()
client.run(TOKEN)
