import discord
from discord.ext import commands
import hashlib
import requests
import random
import asyncio

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

def check_password(password):
    sha_password = hashlib.sha1(password.encode()).hexdigest()
    sha_prefix = sha_password[:5]
    sha_postfix = sha_password[5:].upper()

    url = "https://api.pwnedpasswords.com/range/" + sha_prefix

    try:
        response = requests.get(url)

        pwnd_dict = {}
        pwnd_list = response.text.split("\r\n")
        for pwnd_pass in pwnd_list:
            pwnd_hash = pwnd_pass.split(":")
            pwnd_dict[pwnd_hash[0]] = pwnd_hash[1]

        if sha_postfix in pwnd_dict.keys():
            return int(pwnd_dict[sha_postfix])
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print("\033[91mErreur de connexion au service Pwned Passwords :", e, "\033[0m")
        return -1
@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command()
async def p(ctx: commands.Context, *,message: str):
    compromised_count = check_password(message)
    if compromised_count > 0:
        await ctx.send("```diff\n- " + "Le mot de passe " + message + " a été compromis " + str(compromised_count) + " fois. Il est recommandé de ne pas l'utiliser." + "\n```")
    else:
        await ctx.send("```diff\n+ " + "Le mot de passe " + message+ " n'a pas été trouvé. Vous pouvez l'utiliser." + "\n```")

@bot.command()
async def f(ctx : commands.context,file : str):
    try:
        ValidPasswd = []
        with open(file, 'r') as f:
            passwords = f.readlines()
        for password in passwords:
            password = password.strip()
            compromised_count = check_password(password)
            if compromised_count > 0:
                await ctx.send("```diff\n- " + "Le mot de passe " + password + " a été compromis " + str(compromised_count) + " fois. Il est recommandé de ne pas l'utiliser." + "\n```")
            else:
                await ctx.send("```diff\n+ " + "Le mot de passe " + password + " n'a pas été trouvé. Vous pouvez l'utiliser." + "\n```")
                ValidPasswd.append(password)
        await ctx.send("\nMots de passe qui peuvent être utilisés:")
        for PasswdValid in ValidPasswd: 
            await ctx.send("```diff\n+ "+ PasswdValid +"\n```")
    except FileNotFoundError:
        print("\033[91mLe fichier spécifié n'a pas été trouvé.\033[0m")

@bot.command()
async def g(ctx: commands.context):
    await ctx.send("Quelle est la longueur du mot de passe que vous voulez générer?")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit()
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        mdp_range = int(msg.content)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé. Veuillez réessayer.")
        return
    except ValueError:
        await ctx.send("Veuillez saisir un nombre valide.")
        return
    if mdp_range <= 0:
        await ctx.send("La longueur du mot de passe doit être supérieure à 0.")
    else:
        while True:
            mdp_generate = ""
            for i in range(mdp_range):
                caracter = chr(random.randint(32, 126))
                mdp_generate += caracter
            await ctx.send("Le mot de passe généré est : " + mdp_generate)

            compromised_count = check_password(mdp_generate)
            if compromised_count > 0:
                await ctx.send("```diff\n- " + "Le mot de passe " + mdp_generate + " a été compromis " + str(compromised_count) + " fois. Il est recommandé de ne pas l'utiliser." + "\n```")
            else:
                await ctx.send("```diff\n+ " + "Le mot de passe " + mdp_generate + " n'a pas été trouvé. Vous pouvez l'utiliser." + "\n```")
                break

if __name__ == "__main__":
    while True:
        print("Vous devez avoir créé un bot Discord pour cette fonctionnalité.\nEntrez exit si ce n'est pas fait.")
        BotToken = input("Veuillez entrez le token du bot discord : ")
        if BotToken == "exit":
            break
        elif BotToken:
            try: 
                bot.run(BotToken)
                break
            except:
                print("WRONG TOKEN.")
                break
        
    
