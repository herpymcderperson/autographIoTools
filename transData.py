import json
import csv
import os
import requests

	#Instantiate variables.  coldData used for raw data, hotData used for combined data, i and j used for athlete/tier selection and iteration
coldData = []
hotData = []
athlete = ""
rarity = ""
i = 0
j = 0
fileCount = 1

	#Input to select athlete
while 1 > i or i > 9:
	i = int(input("Select Athlete: (1: Brady, 2: Gretzky, 3: Osaka, 4: Biles, 5: Jeter, 6: Hawk, 7: Woods, 8: Bolt, 9: ????)\n"))

	#store athlete selection
if i == 1:
	athlete = "Brady "
elif i == 2:
	athlete = "Gretzky "
elif i == 3:
	athlete = "Osaka "
elif i == 4:
	athlete = "Biles "
elif i == 5:
	athlete = "Jeter "
elif i == 6:
	athlete = "Hawk "
elif i == 7:
	athlete = "Woods "
elif i == 8:
	athlete = "Bolt "
elif i == 9:
	athlete = "???? "
else:
	athlete = "Unknown "

	#First calculation to set tier being pulled.  The standard guide labels athletes by first digit 0-8, and tiers by last digit 1-10.  Subtract 1 from i then multiply by 10 to set first digit
i = (i-1)*10

	#Set whether to pull signed or premier tier
while 1 > j or j > 2:
	j = int(input("Premier or Signed: (1: Premier, 2: Signed)\n"))
	
	#Store type selection
if j == 1:
	rarity = "Premier "
elif j == 2:
	rarity = "Signed "
else:
	rarity = "Unknown "
	
	#Second calculation to set tier being pulled.  If premier we do nothing, if Signed we add 5 to i as premier tiers are 1-5, and signed are 6-10.  Reset j after calculation
i = ((j-1) * 5) + i
j = 0

	#Set tier to pull
while 1 > j or j > 5:
	j = int(input("Select Tier: (1: Carbon, 2: Platinum, 3: Emerald, 4: Sapphire, 5: Ruby)\n"))

	#Store tier selection
if j == 1:
	rarity = rarity + "Carbon "
elif j == 2:
	rarity = rarity + "Platinum "
elif j == 3:
	rarity = rarity + "Emerald "
elif j == 4:
	rarity = rarity + "Sapphire "
elif j == 5:
	rarity = rarity + "Ruby "
elif i == 6:
	rarity = rarity + "Unknown "

	#Final calculation to set tier being pulled.  Add tier to current value to finalize tier being pulled.
i = i + j

	#Write header for final data array
hotData.append(["userName", "mint", "prevUserName", "amount", "timestamp"]) 

	#Initial request to the standard guide, pull first page
j = requests.get("https://services.thestandardguide.com/tsg-api/getTransactionsStandard/" + str(i) + "/1")

	#From first page, load content and select the total number of pages for the tier selected
temp = json.loads(j.content)
k = int(temp['totalPages'])

	#Iterate through amount of pages to pull transactions
while k > 0:
		#Print k for status update
	print(k)
		#Request page from the standard guide and parse json
	f = requests.get("https://services.thestandardguide.com/tsg-api/getTransactionsStandard/" + str(i) + "/" + str(k))
	data = json.loads(f.content)
	
		#write parsed json to dictionary
	coldData = data['content']
	
		#Select wanted data from dictionary, write to final array
	for l in coldData:
		rowData = []
		rowData.append(l.get("userName"))
		rowData.append(l.get("mint"))
		rowData.append(l.get("prevUserName"))
		rowData.append(l.get("amount"))
		rowData.append(l.get("timestamp"))
		hotData.append(rowData)
	k = k - 1

	#Write final array to CSV
with open(athlete + rarity + "Data.csv",'w', newline='') as csvfile:
	csvWriter= csv.writer(csvfile,delimiter=',')
	csvWriter.writerows(hotData)
		