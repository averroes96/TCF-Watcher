import smtplib, ssl, requests, time
from datetime import datetime

def difference(a, b): #function allowing to calculate an index of difference between 2 strings
    if(a == b):
        return 0
	
    cpt=0
    u=zip(a,b)
    for i,j in u:
        if i!=j:
            cpt+=1
    return cpt/(min(len(a), len(b)))
"""*************************************************"""
def sendEmail():
	port = 465
	# Creating a secure SSL context
	context = ssl.create_default_context()

	login = "login@email.here" #sending gmail address, must have the option "allow non-secure applications" enabled
	password = "password" #password of the sending gmail box
	receiver = "receiver@email.here" #reception email address, preferably linked to your phone to be notified
	
	message = "Subject: TCF-Bot Update\nUn changement à été déctecté".encode('utf-8') #subject and body of the notification email.

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			server.login(login, password) #connection to the gmail sending box
			server.sendmail("TCF-Bot", receiver, message) # sending email
"""*************************************************"""
s = requests.Session()
url = 'https://portail.if-algerie.com/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
cookie = {'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6ImN0a3gyQThmZW9rNnV5UUJUZkhXV2c9PSIsInZhbHVlIjoicU9TOFphWGV6UFJrUFFiYUthb0I2XC9yY004N2Q3eStPT1ErcDEwQm5tYUU4aTlYN2VRZjZXS2h2WFlVNHh6elFCXC9UYytwS1ZIXC9keThmNDB5bmQrazBqV3JycmU2Vmw0aGh1cmg3Qkgrb2V5aEhFSFVtbG9CMHVKZ010SGlqb3kyb0pwRkYzbW9MaHE1WEU2TTF2a0NMTzAxOGpvSWg2dDdyOVVnY0VhbzBVNFJQVU0yYjF2dmx6dFZ5VnlWbjlFIiwibWFjIjoiOTkyMDYwMWE0OThlMTcxNDVjMzk2Yzc4YTM0NTVlMmFlYThlNDZjNjZmNmVjZDFhM2ExOWIwMDJlMmUyZTJlNiJ9'}

x = s.get(url, headers=header, cookies=cookie)
if("TCF".encode('utf-8') in x.content):
    print("Cookie valide.")
else:
    print("Cookie invalide. Veuillez vous déconnecter/reconnecter au niveau de votre navigateur et mettre à jour le cookie.")
    exit()

nbReqs = 0
nbVersions = 1
nbIgnored = 0
delay = 60*5 #check once every 5min
print("Vérifié", nbReqs, "fois,", nbVersions, "version(s) recontrée(s) et", nbIgnored, "version(s) ignorée(s)")
while(True):
    time.sleep(delay)
    try:
        y = s.get(url, headers=header, cookies=cookie)
        nbReqs += 1
        diff = difference(x.content, y.content)
        if(diff >= 0.1): #0.1 to ignore minor changes
            sendEmail()
            now = datetime.now()
            print(now, ": Nouvelle version détectée avec différence de", diff)
            nbVersions += 1
        elif(diff > 0):
            now = datetime.now()
            print(now, ": Nouvelle version ignorée avec différence de", diff)
            nbIgnored += 1
        x=y
    except:
        print("Une erreur est survenue, itération ignorée...")
    print("Vérifié", nbReqs, "fois,", nbVersions, "version(s) recontrée(s) et", nbIgnored, "version(s) ignorée(s)")
