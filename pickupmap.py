import gmplot
import pandas as pd
from ipywidgets.embed import embed_minimal_html
#gmaps.configure(api_key="AI...")

pickupData = pd.read_csv('Uber_Rides.csv', usecols = [9], names = ['latlong'])
dropoffData = pd.read_csv('Uber_Rides.csv', usecols = [10], names = ['ll'])


#pickupDf = pickupData[:,0].str.split(',',1,expand = true)
#pickupDf = pd.DataFrame()
#dropoffDf = pd.DataFrame()
#pickupDf["Latitude"] = pickupData.latlong.str.split(',').str.get(0)
#pickupDf["Longitude"] = pickupData.latlong.str.split(',').str.get(1)

lata = pickupData.latlong.str.split(',').str.get(0)
longit = pickupData.latlong.str.split(',').str.get(1)
lata = pd.to_numeric(lata, errors = 'coerce')
longit = pd.to_numeric(longit, errors = 'coerce')

#print pickupDf.dtypes
#pickupDf.head()

#map = gmaps.figure(map_type='HYBRID')
#heatmap_layer = gmaps.heatmap_layer(pickupDf)
#map.add_layer(heatmap_layer)

gmap = gmplot.GoogleMapPlotter(42.33129, -71.10307, 10)
gmap.heatmap(lata, longit, threshold = 0.01, radius = 50, opacity = 1, dissipating = True) 
gmap.draw("pickups.html")

lat = dropoffData.ll.str.split(',').str.get(0)
longi = dropoffData.ll.str.split(',').str.get(1)
lat = pd.to_numeric(lat, errors = 'coerce')
longi = pd.to_numeric(longi, errors = 'coerce')

gmap = gmplot.GoogleMapPlotter(42, -71, 10)
gmap.heatmap(lat, longi, threshold = 0.01, radius = 50, opacity = 1, dissipating = True) 
gmap.draw("dropoffs.html")

totalLat = pd.concat([lata, lat])
totalLong = pd.concat([longit, longi])

gmap = gmplot.GoogleMapPlotter(42, -71, 10)
gmap.heatmap(totalLat, totalLong, threshold = 0.01, radius = 50, opacity = 1, dissipating = True) 
gmap.draw("combined.html")