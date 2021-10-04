 #Import Dependencies
import json
import csv
import os
import requests
import time
from multiprocessing import Pool

	#Define our function to pull a particular tier of tokens
def pullSingleTier(i):
		#Instantiate function local variables.  coldData is raw data, coolData is returned data
	coldData = []
	coolData = []
	j = 1
	
		#Use passed value to determine Athlete (Yes a dictionary would be better)
	if i <= 10:
		athlete = "Brady"
	elif i <= 20:
		athlete = "Gretzky"
	elif i <= 30:
		athlete = "Osaka"
	elif i <= 40:
		athlete = "Biles"
	elif i <= 50:
		athlete = "Jeter"
	elif i <= 60:
		athlete = "Hawk"
	elif i <= 70:
		athlete = "Woods"
	elif i <= 80:
		athlete = "Bolt"
	elif i <= 90:
		athlete = "TBD"
	else:
		athlete = "Unknown"
	
		#Use passed value to determine tier, pages of data that need to be pulled. (Yes a dictionary would be better)
	if (i % 10) == 1:
		rarity = "Premier Carbon"
		fileCount = 100
	elif (i % 10) == 2:
		rarity = "Premier Platinum"
		fileCount = 50
	elif (i % 10) == 3:
		rarity = "Premier Emerald"
		fileCount = 30
	elif (i % 10) == 4:
		rarity = "Premier Sapphire"
		fileCount = 15
	elif (i % 10) == 5:
		rarity = "Premier Ruby"
		fileCount = 8
	elif (i % 10) == 6:
		rarity = "Signed Carbon"
		fileCount = 2
	elif (i % 10) == 7:
		rarity = "Signed Platinum"
		fileCount = 2
	elif (i % 10) == 8:
		rarity = "Signed Emerald"
		fileCount = 1
	elif (i % 10) == 9:
		rarity = "Signed Sapphire"
		fileCount = 1
	elif (i % 10) == 0:
		rarity = "Signed Ruby"
		fileCount = 1
	else:
		rarity = "Unknown"
		fileCount = 1
	
		#Pull data from The Standard Guide
	while j <= fileCount:
			#Print to track progress
		print(str(i) + ", " + str(j))
		
			#Reguest to the standard guide to return data in json format
		f = requests.get("https://services.thestandardguide.com/tsg-api/getMints/" + str(i) + "/" + str(j))
		
			#Parse json
		data = json.loads(f.content)
		
			#Dump mint data in json to dictionary
		coldData = data['content']
		
			#Iterate through each dictionary entry and dump requested data into array to be returned
		for k in coldData:
			rowData = []
			rowData.append(str(i))
			rowData.append(athlete)
			rowData.append(rarity)
			rowData.append(k.get("mint"))
			rowData.append(k.get("userName"))
			rowData.append(k.get("amount"))
			rowData.append(k.get("status"))
			rowData.append(k.get("listAmount"))
			rowData.append(k.get("timestamp"))
			coolData.append(rowData)
		j = j + 1
	return coolData
	
	#Main loop
if __name__ == "__main__":
	
		#Store start time of run for performance tracking
	startTime = time.strftime("%Y-%m-%d %H:%M:%S")
		#Instantiate variables.  l is counter to build final array, runArray feeds tiers to pull in preferred order
		#runLists are used to sort data to optimize end time of separate tiers, runAmnt sets end point of data pull
	l = 0
	runArray = []
	hotData = []
	runList1 = []
	runList2 = []
	runList3 = []
	runList4 = []
	runList5 = []
	runList6 = []
	runList = []
	runAmnt = 70

		#Loop arranges tiers into list, putting largest tiers first to optimize time to completion.
	for m in range(runAmnt):
		if m % 10 == 0:
			runList1.append(m)
		elif m % 10 == 1:
			runList2.append(m)
		elif m % 10 == 2:
			runList3.append(m)
		elif m % 10 == 3:
			runList4.append(m)
		elif m % 10 == 4:
			runList5.append(m)
		else:
			runList6.append(m)
	runList = runList1 + runList2 + runList3 + runList4 + runList5 + runList6
	
		#Sets up 4 helper pool to run 4 different tier pulls asyncronously, adding returned data to warmData
	with Pool(4) as p:
		runArray = [p.map_async(pullSingleTier, (d+1,)) for d in runList]
		warmData = [res.get() for res in runArray]
	
		#Write header to final array
	hotData.append(["tierId", "athlete", "rarity", "mint", "userName", "amount", "status", "listAmount", "timestamp"])
		
		#Write returned data to final array (in order of completion, not tier)
	while l < len(warmData):
		m = 0
		while m < len(warmData[l][0]):
			hotData.append(warmData[l][0][m])
			m = m + 1
		l = l + 1

		#Write array to CSV file
	with open("data.csv",'w', newline='') as csvfile:
		csvWriter= csv.writer(csvfile,delimiter=',')
		csvWriter.writerows(hotData)
	
		#Print start and end time for performance tracking.
	print("Start: " + startTime)
	print("  End: " + time.strftime("%Y-%m-%d %H:%M:%S"))
		