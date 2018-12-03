import gmplot
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

priceByType = {
	"uberpool" : 0.80,
	"uberx" : 0.88,
	"uberxl" : 2.30,
	"uberblack" : 4.00,
	"ubertaxi" : 2.80,
	"ubersuv" : 4.35
}

maGasPrice = 2.56
myMpg = 25
averageCar = 5000
averageMpg = 24.7

uberType = pd.read_csv('Uber_Rides.csv', usecols = [2], names = ['type'])
uberType = uberType['type'].astype(str)
uberType = uberType.str.lower()

mpg = pd.read_csv('Uber_Rides.csv', usecols = [11], names = ['mpg'])
mpg = mpg.mpg
mpg = pd.to_numeric(mpg, errors = 'coerce')

pickupData = pd.read_csv('Uber_Rides.csv', usecols = [9], names = ['latlong'])
dropoffData = pd.read_csv('Uber_Rides.csv', usecols = [10], names = ['ll'])

lata = pickupData.latlong.str.split(',').str.get(0)
longit = pickupData.latlong.str.split(',').str.get(1)
lata = pd.to_numeric(lata, errors = 'coerce')
lata = lata.rename("plat")
longit = pd.to_numeric(longit, errors = 'coerce')
longit  = longit.rename("plong")


lat = dropoffData.ll.str.split(',').str.get(0)
longi = dropoffData.ll.str.split(',').str.get(1)
lat = pd.to_numeric(lat, errors = 'coerce')
lat = lat.rename("dlat")
longi = pd.to_numeric(longi, errors = 'coerce')
longi = longi.rename("dlong")

frame = pd.concat([uberType, mpg, lata, longit, lat, longi], axis=1, sort=False)
print frame

differential = []
differentialneg = []
tripNum = []

num = 1
for index, row in frame.iterrows():
	uberGasUsed = geodesic((row["plat"], row["plong"]), (row["dlat"], row["dlong"])).miles / row["mpg"]
	myGasUsed = geodesic((row["plat"], row["plong"]), (row["dlat"], row["dlong"])).miles / myMpg

	dif = myGasUsed - uberGasUsed
	if(dif >= 0):
		differential = np.append(differential, dif)
		differentialneg = np.append(differentialneg, 0)
	if(dif < 0):
		differential = np.append(differential, 0)
		differentialneg = np.append(differentialneg, dif)

	tripNum = np.append(tripNum, num)
	num = num + 1

	#gasCost = round(((distance/ averageMpg) * maGasPrice),2)
	#print "cost of trip for average car owner: ",
	#print(round((averageCar/frame.shape[0]) + gasCost,2))
	
x = range(differential.size)
fig = plt.figure()
ax = plt.subplot(111)
ax.bar(x, differential, width=1, color='g')
ax.bar(x, differentialneg, width=1, color='r')
plt.title('Gas usage differential: My car vs. uber')
plt.xlabel('Trip #')
plt.ylabel('Gallons of gas')
plt.savefig('diff.png', bbox_inches='tight')