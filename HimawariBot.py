import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from discord.ext import commands
from datetime import datetime
import os
from dotenv import load_dotenv
import random
import asyncio
import pytz
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL  # Substituir youtube_dl por yt_dlp


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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-read-private",
))

playlists = sp.current_user_playlists()
for playlist in playlists['items']:
    print(f"Playlist: {playlist['name']}")

# Configuração para yt-dlp
yt_dlp_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}
ffmpeg_options = {
    'options': '-vn',
}
ytdl = YoutubeDL(yt_dlp_options)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name="musica")
async def play_music(ctx, *, search: str):
    # Conecta no canal de voz do autor
    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()

    # Busca a música no YouTube
    try:
        await ctx.send(f"Procurando por: {search}")
        info = ytdl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        url = info['url']
        title = info['title']
    except Exception as e:
        await ctx.send(f"Erro ao buscar música: {e}")
        return

    # Toca a música
    voice_client = ctx.voice_client
    source = FFmpegPCMAudio(url, **ffmpeg_options)
    if not voice_client.is_playing():
        voice_client.play(source, after=lambda e: print(f"Término: {e}"))
        await ctx.send(f"Tocando agora: **{title}**")
    else:
        await ctx.send("Já estou tocando uma música. Aguarde o término para tocar outra.")

# Comando para parar e desconectar
@bot.command(name="parar")
async def stop_music(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot desconectado do canal de voz.")
    else:
        await ctx.send("Não estou conectado a nenhum canal de voz.")



bot.run(TOKEN)
