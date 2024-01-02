import discord
import os
import requests
import json 
import random
from replit import db
from keep_alive import keep_alive


intents = discord.Intents.default()
client = discord.Client(intents=intents)

#defined list full of sad words
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "upset"]

starter_encouragements = [
  "Cheer up!",
  "You got this!",
  "Don't give up!"
]
#function to get quote from zenquote api
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

#function to update encouraging messages
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

#function to deleted added encouraging messages
def delete_encouragement(index):
  try:
    index = int(index)
    encouragements = db["encouragements"]
    if len(encouragements) > index:
      del encouragements[index]
      db["encouragements"] = encouragements
    else:
      print("Index out of range")
  except ValueError:
    print("Invalid index")



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  if message.content.startswith('!How mean is Dia'):
    await message.channel.send('So mean :(')
  
#calls get_quote function and sends an inspirational quote back to user
  if message.content.startswith('!Inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])


#checks if there is any sad words, and responds with encouraging words  
  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(options))

  if message.content.startswith("!new"):
    encouraging_message = message.content.split("!new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = message.content.split("!del",1)[1]
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

keep_alive()
my_secret = os.environ['KEY']
client.run(my_secret)