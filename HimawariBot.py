import discord
from discord.ext import commands
from datetime import datetime
import os
from dotenv import load_dotenv
import random
import asyncio
import pytz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Função para carregar frases de um arquivo
def load_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

async def digitando_a_mensagem(channel, message):
    async with channel.typing():
        await asyncio.sleep(2)  # Simular tempo de digitação
        await channel.send(message)

# Corrigindo a definição do comando
@bot.command(name="hora")
async def hora(ctx):
    timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(timezone).strftime('%H:%M:%S')  # Formatar o horário
    response = f"Agora são {current_time}, {ctx.author.mention}."
    await digitando_a_mensagem(ctx.channel, response)

bot.run(TOKEN)
