import discord
from discord.ext import commands
from kodland_utils import *
import os, random, requests


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def generate_password(ctx):
    await ctx.send(pass_gen(10))

@bot.command()
async def flip(ctx):
    await ctx.send(flip_coin())

@bot.command()
async def rps(ctx):
    choices = ['✊', '✋', '✌️']  # batu, kertas, gunting
    bot_choice = random.choice(choices)

    message = await ctx.send("Let's play Rock-Paper-Scissors! React with your choice:")
    for choice in choices:
        await message.add_reaction(choice)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in choices

    reaction, user = await bot.wait_for('reaction_add', check=check)
    user_choice = str(reaction.emoji)
    result = determine_winner(user_choice, bot_choice)
    await ctx.send(f'You chose {user_choice}, I chose {bot_choice}. {result}')

def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a tie!"
    elif (user_choice == '✊' and bot_choice == '✌️') or \
         (user_choice == '✋' and bot_choice == '✊') or \
         (user_choice == '✌️' and bot_choice == '✋'):
        return "You win! 🎉"
    else:
        return "I win! 😎"

@bot.command()
async def meme(ctx):
    selected = random.choice(os.listdir('images'))
    with open(f'images/{selected}', 'rb') as f:
        pictures = discord.File(f)
    await ctx.send(file=pictures)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)


#Daftar Sampah
organik = ['sayur busuk', 'dedaunan', 'sisa makanan', 'kulit buah', 'kotoran hewan']
kertas = ['kardus', 'paper bag', 'kertas', 'tisu', 'koran bekas']
plastik = ['kresek', 'botol plastik', 'cup plastik', 'kemasan makanan', 'bungkus permen']
logam = ['kaleng', 'baterai', 'alat elektronik', 'besi berkarat', 'kabel']

@bot.command()
async def tanya_sampah(ctx):
    await ctx.send('Sampah apa yang ingin diperiksa?')
    message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    message = str(message.content)

    #Check
    if message.lower() in organik:
        await ctx.send('Itu sampah **ORGANIK**')
        await ctx.send('Sampah itu bisa jadi *PUPUK*')
    elif message.lower() in kertas:
        await ctx.send('Itu sampah **KERTAS**')
        await ctx.send('itu bisa buat di daur ulang jadi kertas lagi')
        await ctx.send('Atau bisa dibuat jadi kerajinan unik, banyak kok referensinya!')
    elif message.lower() in plastik:
        await ctx.send('Itu sampah **PLASTIK**')
        await ctx.send('bisa di buat jadi kerajinan tangan tuh!')
        await ctx.send('contohnya kaya bunga plastik yang bagus banget')
    elif message.lower() in logam:
        await ctx.send('Itu sampah **LOGAM**')
        await ctx.send('kumpulin aja dlu, ntar bisa di daur ulang buat kerajinan!')
        await ctx.send('buat pengolahannya ada banyak di YT')
    else:
        await ctx.send("Sampahnya gaada di daftar sistemnya nih, tunggu apdet yah:>")

bot.run()
