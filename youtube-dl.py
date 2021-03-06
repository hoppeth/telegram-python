# uses youtube-dl - https://github.com/ytdl-org/youtube-dl 
# and the python telebot api - https://github.com/eternnoir/pyTelegramBotAPI
# this is a demo, is not secure 

import telebot
import subprocess
import json
import os

API_TOKEN = 'your_token_here'

bot = telebot.TeleBot(API_TOKEN)

# users.txt with a numerical userid of authorised users, one id per line
with open('users.txt', 'r') as f:
    authorizedusers = [line.strip() for line in f]


print(authorizedusers)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    substring = "https://www.youtube"
    if str(message.from_user.id) in authorizedusers:
        print('Authorized: \n', 'UID: ', message.from_user.id, '\n', 'message content: ', message.text)
        authed = "yes"
    else:
        replymsg = ('not authorized: ', str(message.from_user.id), message)
        print(message)
        bot.reply_to(message, replymsg)
        return

    if substring in message.text:
        if "yes" in authed:
            print('found a url')
            bot.reply_to(message, 'found a url')
            url = message.text
            dir = str(message.from_user.id)
            if not os.path.exists(dir):
                os.makedirs(dir)

            output = subprocess.run(
                ['youtube-dl', '-r', '12M', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio', '--merge-output-format',
                 'mp4', url], cwd=dir, stdout=subprocess.PIPE)
            theoutput = str(output)[-60:]    
            bot.reply_to(message, theoutput)

        else:
            bot.reply_to(message, 'last response not accepted')
    print('end of first if block')

bot.polling()
