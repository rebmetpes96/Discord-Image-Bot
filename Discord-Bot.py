import discord
from bs4 import BeautifulSoup
from requests import get
import io
import collections
import string
import re


client = discord.Client()

players = {}
channelID = "ChannelID"
fourhp = "CHAT_AREA_ID"


@client.event
async def on_ready():
    print("Eingeloggt als: {}, mit der ID: {} \n ------------------------------------".format(client.user.name , client.user.id))
    await client.send_message(discord.Object(id=fourhp_channelID),"I am online bitchez")
    #discord.Object(id= [], "content") LÄSST EINEN NACHRICHTEN AN KANÄLEN SCHICKEN.


@client.event
async def on_message(message):
    #get an image by input
    if message.content.startswith("?bild"):
        mess = message.content[5:]

        names = mess
        SUFIX = "&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi9ley5ipnZAhXCKFAKHXLzAAoQ_AUIDCgD&biw=1536&bih=759"
        PREFIX = "https://www.google.de/search?q="

        if " " in names:
            names = names.replace(" ", "%20")
            FullURL = PREFIX + names + SUFIX
        else:
            FullURL = PREFIX + names + SUFIX

        source_code = get(FullURL)
        plain_text = source_code.text
        #print(plain_text)
        soup = BeautifulSoup(plain_text)
        link = soup.find("img")["src"]
        response = get(link,stream=True)
        #print(link)

        try:
            names = names.replace("%20"," ")
        except:
            pass

        #await client.send_typing(message.channel)
        await client.send_message(message.channel, " Hier ist ein Bild von: "+names.upper())
        await client.send_file(message.channel, io.BytesIO(response.raw.read()),filename="img.jpg",content=None)

    if message.content.startswith("?clear"):
        await client.purge_from(message.channel, limit=600,check=None, before=None, after=None, around=None)
        await client.send_message(message.channel, "Alle Nachrichten gelöscht!")

    if message.content.startswith("?def"):
        #get the definition of a subject. The code below just detects umlauts and other unaccepted characters in the link
        names = message.content[4:]
        table = collections.defaultdict(lambda: None)
        table.update({
            ord('é'): 'e',
            ord('ô'): 'o',
            ord('í'):'i',
            ord('ý'): 'y',
            ord(' '): ' ',
            ord('\N{NO-BREAK SPACE}'): ' ',
            ord('\N{EN SPACE}'): ' ',
            ord('\N{EM SPACE}'): ' ',
            ord('\N{THREE-PER-EM SPACE}'): ' ',
            ord('\N{FOUR-PER-EM SPACE}'): ' ',
            ord('\N{SIX-PER-EM SPACE}'): ' ',
            ord('\N{FIGURE SPACE}'): ' ',
            ord('\N{PUNCTUATION SPACE}'): ' ',
            ord('\N{THIN SPACE}'): ' ',
            ord('\N{HAIR SPACE}'): ' ',
            ord('\N{ZERO WIDTH SPACE}'): ' ',
            ord('\N{NARROW NO-BREAK SPACE}'): ' ',
            ord('\N{MEDIUM MATHEMATICAL SPACE}'): ' ',
            ord('\N{IDEOGRAPHIC SPACE}'): ' ',
            ord('\N{IDEOGRAPHIC HALF FILL SPACE}'): ' ',
            ord('\N{ZERO WIDTH NO-BREAK SPACE}'): ' ',
            ord('\N{TAG SPACE}'): ' ',
            ord('/'): '/',
            ord(':'): ':',
            ord('.'): '.',
            ord('_'):'_',
            ord('+'):'+'
        })
        table.update(dict(zip(map(ord, string.ascii_uppercase), string.ascii_uppercase)))
        table.update(dict(zip(map(ord, string.ascii_lowercase), string.ascii_lowercase)))
        table.update(dict(zip(map(ord, string.digits), string.digits)))

        prefix = "https://www.google.de/search?q="
        FullUrl = prefix + names + " Wikipedia"
        print(FullUrl)
        if " " in FullUrl:
            FullUrl = FullUrl.replace(" ", "+")
            print(FullUrl)

        source_code = get(FullUrl)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        k = (soup.find("cite"))
        k = k.text
        # print(k.translate(table,))
        k = k.translate(table, )
        print(k)
        source_code2 = get(k)
        plain_text2 = source_code2.text
        spou = BeautifulSoup(plain_text2)
        l=(spou.find("p").text)
        await client.send_message(message.channel, l)



client.run(fourhp)
