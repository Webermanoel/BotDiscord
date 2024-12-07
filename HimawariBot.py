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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return []

# para carregar frases de ativação e resposta
ATIVACAO = load_phrases('ativacao.txt')
RESPOSTA = load_phrases('resposta.txt')

# função que simula a digitação
async def digitando_a_mensagem(channel, message):
    async with channel.typing():
        await asyncio.sleep(2)
        await channel.send(message)

# função que mostra a hora quando o comando for !hora
@bot.command(name="hora")
async def hora(ctx):
    timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(timezone).strftime('%H:%M:%S')  # Formatar o horário
    response = f"Agora são {current_time}, {ctx.author.mention}."
    await digitando_a_mensagem(ctx.channel, response)

# função que mostra o bot conectado
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Mensagem recebida: {message.content}")  # Log para depuração

    content_lower = message.content.lower()

    for trigger, response in zip(ATIVACAO, RESPOSTA):
        print(f"Checando ativação: {trigger}")  # Verificar cada ativação
        if trigger.lower() in content_lower:  # Comparação case-insensitive
            formatted_response = response.replace("{author}", message.author.mention)
            print(f"Ativação encontrada: {trigger}. Respondendo com: {formatted_response}")
            await send_typing_message(message.channel, formatted_response)
            break

    await bot.process_commands(message)

async def send_typing_message(channel, message):
    async with channel.typing():
        await asyncio.sleep(2)  # Simular tempo de digitação
        await channel.send(message)


bot.run(TOKEN)
