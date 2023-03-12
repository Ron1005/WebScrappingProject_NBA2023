# Imports
from bs4 import BeautifulSoup
import requests
import csv

# connect to the ESPN website
URL = "https://www.espn.in/nba/stats/player"
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "DNT":"1",
            "Connection":"close"}
page = requests.get(URL,headers)

soup1 = BeautifulSoup(page.content,"html.parser")

#Code for getting player names
playernames =[]
for a in soup1.find_all(class_="Table__TR Table__TR--sm Table__even"):
    for b in a.find_all('td'):
        for c in b.find_all('a'):
            playernames.append(c.text)

#Code for getting player positions
positions= []
for a in soup1.find_all(class_="Table__TR Table__TR--sm Table__even"):
    for b in a.find_all('td'):
        for c in b.find_all(class_="position"):
           positions.append(c.text)

#Code for getting playet Stats
allstats = []
for a in soup1.find_all(class_="Table__TR Table__TR--sm Table__even"):
    for b in a.find_all(class_="Table__TD"):
        try:
            allstats.append(float(b.text))
        except:
            pass

#Data Cleaning for player stats array
newstats = allstats[50:]


#Mapping player to player stats using dictionary
playertostats ={}
start = 0
end = 19
for player in playernames:
    playertostats[player]=newstats[start:end]
    start=end
    end = end +19

#Getting Column Headers
headers=[]
for x in soup1.find_all('th'):
    headers.append(x.text)

#Exporting all the data to CSV file
data = []
with open('NBAPointsLeaderDataset2022-23.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for x in range(len(playernames)):
        stats = playertostats[playernames[x]]
        data.append(x+1)
        data.append(playernames[x])
        data.append(positions[x])
        for y in range(len(stats)):
            data.append(stats[y])

        # data=[x+1,playernames[x],poistions[x],stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],
        #       stats[6],stats[7],stats[8],stats[9],stats[10],stats[11],stats[12],stats[13],
        #       stats[14],stats[15],stats[16],stats[17],stats[18]]
        writer.writerow(data)
        data.clear()







