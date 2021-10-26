import discord
import logging
import json
import server
import asyncio
import time
from discord.ext import commands
from datetime import datetime
from server import keep_alive

# Client
client = commands.Bot(command_prefix='$')
client.launch_time = datetime.utcnow()
client.remove_command('help')
logging.basicConfig(level=logging.INFO)

# Help Tab
@client.command(name='help')
async def help(context):
  myEmbed = discord.Embed(color=0xd4af37)
  myEmbed.add_field(name="$help",value="The client's help command.")
  myEmbed.add_field(name="$fillout",value="Allows user to fillout a census form")
  await context.author.send(embed=myEmbed)

# Create
@client.command(name='create')
async def create(context, *, cenname):
  with open("census.json","r+") as f:
    db = json.load(f)

    def check(m):
      return m.author.id == context.author.id

    if cenname == None:
      await context.send("Enter in name for census. (format: OCT2021)")
      name = await client.wait_for("message", check=check)
      cenname = name.content.upper()
      
      db['censuses'].append({
        "name":cenname,
        "responses": []
      })

      f.seek(0)
      json.dump(db, f, indent=4)
      f.truncate()
      await context.send("Created new census in the database.")
    else:
      db['censuses'].append({
        "name":cenname,
        "responses": []
      })

      f.seek(0)
      json.dump(db, f, indent=4)
      f.truncate()
      await context.send("Created new census in the database.")

# Fillout 
@client.command(name='fillout')
async def fillout(context):
  with open("census.json","r+") as f:
    db = json.load(f)

    userid = context.author.id
    dsuser = str("{}#{}".format(context.author.name,context.author.discriminator))
    await context.author.send("Welcome to the Polperro Islands Census - 2021 October Census...")
    time.sleep(2)
    await context.author.send("This is the official client for the Polperro Census. It is quick, simple, and straight-forward. Your responses will remain anonymous. Please complete this census form to the best of your ability to ensure that the submitted data is as accurate as possible.")
    time.sleep(5)
    await context.author.send("Type next to procced with the census...")

    def check(m):
      return m.author.id == context.author.id

    typemessage = await client.wait_for("message", check=check)
    if typemessage.content.lower() == "next":
      await context.author.send("What is your minecraft username?")

      ausername = await client.wait_for("message", check=check)
      await context.author.send("What is your gender? A: Male, B: Female, C: Trans, D: Non-binary, E: Prefer Not to Say")

      agender = await client.wait_for("message", check=check)

      def rgender():
        with open("legend.json","r") as f:
          db = json.load(f)

          for leg in db['legend']:
            for response in leg['gender']:
              respa = response['genkey']
              if agender.content.upper() == respa:
                rgender = response['genvalue']
                return rgender
      
      rgender = rgender()

      if agender.content.upper() == "A" or "B" or "C" or "D" or "E":
        await context.author.send("What is your age as of September 2021?")
        aage = await client.wait_for("message", check=check)
        if aage.content >= "13":
          await context.author.send("Which nation do use currently reside? A - Catalina, B - Boblandia, C - Ho'okele, D - Cape Corsair, E - Unaffiliated")
          anresidence = await client.wait_for("message", check=check)

         
          def rresidence():
            with open("legend.json","r+") as f:
              db = json.load(f)

              for legkey in db['legend']:
                for response in legkey['residence']:
                  respa = response['genkey']
                  respb = response['genvalue']
                  if anresidence.content.upper() == respa:
                    rresidence = respb
                    return rresidence
          
          rresidence = rresidence()

          await context.author.send("What is your residence status? A - Natural Citizen, B - Dual Citizen, C - Immigrant, D - Asylum Seeker")
          asresidence = await client.wait_for("message", check=check)

          def rsresidence():
            with open("legend.json","r+") as f:
              db = json.load(f)

              for legkey in db['legend']:
                for response in legkey['statusres']:
                  respa = response['genkey']
                  respb = response['genvalue']
                  if asresidence.content.upper() == respa:
                    rsresidence = respb
                    return rsresidence

          rsresidence = rsresidence()

          await context.author.send("What is your employment status? A - Government Employee, B - Private Employee, C - Unemployed")
          asemployment = await client.wait_for("message", check=check)

          def remployment():
            with open("legend.json","r+") as f:
              db = json.load(f)

              for legkey in db['legend']:
                for response in legkey['employment']:
                  respa = response['genkey']
                  respb = response['genvalue']
                  if asemployment.content.upper() == respa:
                    remployment = respb
                    return remployment
          
          remployment = remployment()

          await context.author.send("Are you a business owner? (Y/N)")
          aabusiness = await client.wait_for("message", check=check)

          def rbusiness():
            with open("legend.json","r+") as f:
              db = json.load(f)

              for legkey in db['legend']:
                for response in legkey['business']:
                  respa = response['genkey']
                  respb = response['genvalue']
                  if aabusiness.content.upper() == respa:
                    rbusiness = respb
                    return rbusiness
          
          rbusiness = rbusiness()

          await context.author.send("Are you registered to vote? (Y/N)")
          aavote = await client.wait_for("message", check=check)

          def rregvote():
            with open("legend.json","r+") as f:
              db = json.load(f)

              for legkey in db['legend']:
                for response in legkey['registered']:
                  respa = response['genkey']
                  respb = response['genvalue']
                  if aavote.content.upper() == respa:
                    rregvote = respb
                    return rregvote
          
          rregvote = rregvote()

          await context.author.send("Have you voted in any elections before? (Y/N)")
          aaele = await client.wait_for("message", check=check)

          def rvotebefore():
            with open("legend.json","r+") as f:
              db = json.load(f)

              for legkey in db['legend']:
                for response in legkey['votebefore']:
                  respa = response['genkey']
                  respb = response['genvalue']
                  if aaele.content.upper() == respa:
                    rvotebefore = respb
                    return rvotebefore
          
          rvotebefore = rvotebefore()

          await context.author.send("How many hours daily - on average -do you paly the Polperro Islands Server?")
          aahours = await client.wait_for("message", check=check)


          await context.author.send("By submitting this form, you, the undersigned participant, acknowledge that your response is truthful. Type your minecraft username in all caps.")
          sign = await client.wait_for("message", check=check)

          username = ausername.content
          age = int(aage.content)
          gender = rgender
          nresidence = rresidence
          sresidence = rsresidence
          semployment = remployment
          abusiness = rbusiness
          avote = rregvote
          aele = rvotebefore
          ahours = aahours.content
          disname = context.author.name

          channel = client.get_channel()

          myEmbed = discord.Embed(color=0xd4af37)
          myEmbed.set_author(name=disname)
          myEmbed.add_field(name="What is your minecraft username?", value=username, inline=False)
          myEmbed.add_field(name="What is your age as of September 2021?", value=f'{age} years old', inline=False)
          myEmbed.add_field(name="What is your gender?", value=gender, inline=False)
          myEmbed.add_field(name="Which nation do use currently reside?", value=nresidence, inline=False)
          myEmbed.add_field(name="What is your residence status?", value=sresidence, inline=False)
          myEmbed.add_field(name="What is your employment status?", value=semployment, inline=False)
          myEmbed.add_field(name="Are you a business owner?", value=abusiness, inline=False)
          myEmbed.add_field(name="Are you registered to vote?", value=avote, inline=False)
          myEmbed.add_field(name="Have you voted in any elections before?", value=aele, inline=False)
          myEmbed.add_field(name="How many hours daily - on average -do you paly the Polperro Islands Server?", value=f'{ahours} hour(s)', inline=False)
          await channel.send(embed=myEmbed)

          for census in db['censuses']:
            census_name = census['name']
            if census_name == "OCT2021":
              census['responses'].append({
                "username": username,
                "discorduser": dsuser,
                "id": userid,
                "response": [
                  {
                    "age": age,
                    "gender": gender,
                    "current_residence": nresidence,
                    "residence_status": sresidence,
                    "employment_status": semployment,
                    "business_owner": abusiness,
                    "registered_to_vote": avote,
                    "voted_before": aele,
                    "game_play_avg": ahours
                  }
                ]    
              })
                    
              f.seek(0)
              json.dump(db, f, indent=4)
              f.truncate()

              await context.send("Test worked")
 


# Presence & Status
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('Running a census test...'))
  print('Connection Established')

  

keep_alive()
client.run(TOKEN)
