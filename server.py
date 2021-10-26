import asyncio
from flask import Flask
from threading import Thread
from datetime import datetime
from discord.ext import commands


app = Flask('')
client = commands.Bot(command_prefix='.')
client.launch_time = datetime.utcnow()


def sysuptime():
  delta_uptime = datetime.utcnow() - client.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  return f'{days}d, {hours}h, {minutes}m, {seconds}s'


uptime = sysuptime()

@app.route('/')
def home():
  return f"testing {uptime}"

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()