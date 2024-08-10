import csv
import json
import time
from datetime import datetime
import numpy as np

import fiona
######################################################################################
######################################################################################
datasets_names = ['co-est2020-alldata_utf8.csv','co-est2023-alldata_utf8.csv']

output_geo = {
	"type": "FeatureCollection",
	"name": "Landsat 8, LST and NDVI Temportal Analysis",
	"features": []
}
store_features = []
#Dataset 1 Headers: SUMLEV,REGION,DIVISION,STATE,COUNTY,STNAME,CTYNAME,CENSUS2010POP,ESTIMATESBASE2010,POPESTIMATE2010,POPESTIMATE2011,POPESTIMATE2012,POPESTIMATE2013,POPESTIMATE2014,POPESTIMATE2015,POPESTIMATE2016,POPESTIMATE2017,POPESTIMATE2018,POPESTIMATE2019,POPESTIMATE2020,NPOPCHG_2010,NPOPCHG_2011,NPOPCHG_2012,NPOPCHG_2013,NPOPCHG_2014,NPOPCHG_2015,NPOPCHG_2016,NPOPCHG_2017,NPOPCHG_2018,NPOPCHG_2019,NPOPCHG_2020,BIRTHS2010,BIRTHS2011,BIRTHS2012,BIRTHS2013,BIRTHS2014,BIRTHS2015,BIRTHS2016,BIRTHS2017,BIRTHS2018,BIRTHS2019,BIRTHS2020,DEATHS2010,DEATHS2011,DEATHS2012,DEATHS2013,DEATHS2014,DEATHS2015,DEATHS2016,DEATHS2017,DEATHS2018,DEATHS2019,DEATHS2020,NATURALINC2010,NATURALINC2011,NATURALINC2012,NATURALINC2013,NATURALINC2014,NATURALINC2015,NATURALINC2016,NATURALINC2017,NATURALINC2018,NATURALINC2019,NATURALINC2020,INTERNATIONALMIG2010,INTERNATIONALMIG2011,INTERNATIONALMIG2012,INTERNATIONALMIG2013,INTERNATIONALMIG2014,INTERNATIONALMIG2015,INTERNATIONALMIG2016,INTERNATIONALMIG2017,INTERNATIONALMIG2018,INTERNATIONALMIG2019,INTERNATIONALMIG2020,DOMESTICMIG2010,DOMESTICMIG2011,DOMESTICMIG2012,DOMESTICMIG2013,DOMESTICMIG2014,DOMESTICMIG2015,DOMESTICMIG2016,DOMESTICMIG2017,DOMESTICMIG2018,DOMESTICMIG2019,DOMESTICMIG2020,NETMIG2010,NETMIG2011,NETMIG2012,NETMIG2013,NETMIG2014,NETMIG2015,NETMIG2016,NETMIG2017,NETMIG2018,NETMIG2019,NETMIG2020,RESIDUAL2010,RESIDUAL2011,RESIDUAL2012,RESIDUAL2013,RESIDUAL2014,RESIDUAL2015,RESIDUAL2016,RESIDUAL2017,RESIDUAL2018,RESIDUAL2019,RESIDUAL2020,GQESTIMATESBASE2010,GQESTIMATES2010,GQESTIMATES2011,GQESTIMATES2012,GQESTIMATES2013,GQESTIMATES2014,GQESTIMATES2015,GQESTIMATES2016,GQESTIMATES2017,GQESTIMATES2018,GQESTIMATES2019,GQESTIMATES2020,RBIRTH2011,RBIRTH2012,RBIRTH2013,RBIRTH2014,RBIRTH2015,RBIRTH2016,RBIRTH2017,RBIRTH2018,RBIRTH2019,RBIRTH2020,RDEATH2011,RDEATH2012,RDEATH2013,RDEATH2014,RDEATH2015,RDEATH2016,RDEATH2017,RDEATH2018,RDEATH2019,RDEATH2020,RNATURALINC2011,RNATURALINC2012,RNATURALINC2013,RNATURALINC2014,RNATURALINC2015,RNATURALINC2016,RNATURALINC2017,RNATURALINC2018,RNATURALINC2019,RNATURALINC2020,RINTERNATIONALMIG2011,RINTERNATIONALMIG2012,RINTERNATIONALMIG2013,RINTERNATIONALMIG2014,RINTERNATIONALMIG2015,RINTERNATIONALMIG2016,RINTERNATIONALMIG2017,RINTERNATIONALMIG2018,RINTERNATIONALMIG2019,RINTERNATIONALMIG2020,RDOMESTICMIG2011,RDOMESTICMIG2012,RDOMESTICMIG2013,RDOMESTICMIG2014,RDOMESTICMIG2015,RDOMESTICMIG2016,RDOMESTICMIG2017,RDOMESTICMIG2018,RDOMESTICMIG2019,RDOMESTICMIG2020,RNETMIG2011,RNETMIG2012,RNETMIG2013,RNETMIG2014,RNETMIG2015,RNETMIG2016,RNETMIG2017,RNETMIG2018,RNETMIG2019,RNETMIG2020
#Dataset 2 Headers: SUMLEV,REGION,DIVISION,STATE,COUNTY,STNAME,CTYNAME,ESTIMATESBASE2020,POPESTIMATE2020,POPESTIMATE2021,POPESTIMATE2022,POPESTIMATE2023,NPOPCHG2020,NPOPCHG2021,NPOPCHG2022,NPOPCHG2023,BIRTHS2020,BIRTHS2021,BIRTHS2022,BIRTHS2023,DEATHS2020,DEATHS2021,DEATHS2022,DEATHS2023,NATURALCHG2020,NATURALCHG2021,NATURALCHG2022,NATURALCHG2023,INTERNATIONALMIG2020,INTERNATIONALMIG2021,INTERNATIONALMIG2022,INTERNATIONALMIG2023,DOMESTICMIG2020,DOMESTICMIG2021,DOMESTICMIG2022,DOMESTICMIG2023,NETMIG2020,NETMIG2021,NETMIG2022,NETMIG2023,RESIDUAL2020,RESIDUAL2021,RESIDUAL2022,RESIDUAL2023,GQESTIMATESBASE2020,GQESTIMATES2020,GQESTIMATES2021,GQESTIMATES2022,GQESTIMATES2023,RBIRTH2021,RBIRTH2022,RBIRTH2023,RDEATH2021,RDEATH2022,RDEATH2023,RNATURALCHG2021,RNATURALCHG2022,RNATURALCHG2023,RINTERNATIONALMIG2021,RINTERNATIONALMIG2022,RINTERNATIONALMIG2023,RDOMESTICMIG2021,RDOMESTICMIG2022,RDOMESTICMIG2023,RNETMIG2021,RNETMIG2022,RNETMIG2023
######################################################################################
#Create a dict of headers found in the datasets.
dataCategoryKeys = [
	'POPESTIMATE', 'DOMESTICMIG', 
    'INTERNATIONALMIG', 'NETMIG',
	'BIRTHS', 'DEATHS']

yearStart = 2010
yearEnd = 2024
yearRange = range(2010, yearEnd, 1)
data_to_get = {}
for year in yearRange:
	data_to_get[year] = []
	for dataHeader in dataCategoryKeys:
		data_to_get[year].append(str(dataHeader+str(year)))
######################################################################################
fPath_referenceGeometry = "%s%s" % (r'00_resources/geo_features/','counties.geojson')
geoid_ref = []
with fiona.open(fPath_referenceGeometry) as fc_referenceGeometry:
	for feature in fc_referenceGeometry:
		feature_obj = {"type": "Feature", 'properties':{}, 'geometry':{}}
		geoid = feature["properties"]["GEOID"]
		geoid_ref.append(str(geoid))
		for propKey, propVal in feature["properties"].items():
			feature_obj['properties'][propKey] = propVal
		feature_obj['geometry']['type'] = feature['geometry']['type']
		feature_obj['geometry']['coordinates'] = feature['geometry']['coordinates']
		for year, dataHeaders in data_to_get.items():
			for dataHeader in dataHeaders:
				feature_obj['properties'][dataHeader] = None
		#output_geo['features'].append(feature_obj)
		store_features.append(feature_obj)
######################################################################################
headers_regionRef = [
	'COUNTY_FIPS_CODE','COUNTY_ANSICODE','COUNTY_NAME','COUNTY_STATE',
	'COUNTY_INTPTLAT','COUNTY_INTPTLONG','ABI_REGION','DODGE_CUSTOM_REGION']

write_dataOut = open("%s%s" % (r"02_output/population/",'counties_popStats.csv'), 'w',newline='', encoding='utf-8')
writer_dataOut = csv.writer(write_dataOut)
writer_dataOut.writerow(["GEOID", "COUNTY_FIPS_CODE", "STATE_CODE", "YEAR"]+dataCategoryKeys)
######################################################################################
countiesNotFound = 0
for f in datasets_names:
	print(f)
	with open("%s%s" % (r"01_data/population/",f), 'r', newline='', encoding='utf-8') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		csv_headers = next(csv_reader)
		csv_headers = list(map(str.strip, csv_headers))
		idx_countyHeader = csv_headers.index('COUNTY')
		idx_stateHeader = csv_headers.index('STATE')
		for row in csv_reader:
			countyId = str(row[idx_countyHeader])
			stateId = str(row[idx_stateHeader])
			geoid = str(stateId+countyId)
			
			if geoid in geoid_ref:
				idx = geoid_ref.index(geoid)
				feature = store_features[idx]
				
				for year, dataHeaders in data_to_get.items():
					output_csv = [geoid, countyId, stateId, year]
					outputValid = True
					for dataHeader in dataHeaders:
						if dataHeader in csv_headers:
							idx = csv_headers.index(dataHeader)
							val = row[idx]
							feature['properties'][dataHeader] = val
							output_csv.append(val)
						else:
							outputValid = False
					if outputValid == True:
						writer_dataOut.writerow(output_csv)
				output_geo['features'].append(feature)
			else:
				countiesNotFound+=1
	csvfile.close()
######################################################################################
output_path = "%s%s%s" % (r"02_output/population/",'counties_popStats',".geojson")

with open(output_path, "w") as f:
    json.dump(output_geo, f)
######################################################################################
######################################################################################
print("combine_countyStats.py... Done")