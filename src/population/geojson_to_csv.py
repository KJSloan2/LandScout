import csv
import json

from datetime import datetime
import numpy as np

from preprocessing_tools import csv_to_dict

import fiona

path_customRegions = "%s%s" % (r"02_output\\","24042301_Corgan_DodgeCustomRegions.csv")
headers_customRegions = ['COUNTY_FIPS_CODE','COUNTY_ANSICODE','COUNTY_NAME','COUNTY_STATE',
						 'COUNTY_INTPTLAT','COUNTY_INTPTLONG','ABI_REGION','DODGE_CUSTOM_REGION']
#'YEAR', 'POPESTIMATE', 'DOMESTICMIG', 'INTERNATIONALMIG', 'NETMIG'
customRegions_dict = csv_to_dict(path_customRegions,headers_customRegions)

select_headers = [
	'POPESTIMATE', 'DOMESTICMIG', 'INTERNATIONALMIG',
	'NETMIG','DEATHS','BIRTHS']

yearStart = 2010
yearEnd = 2023
yearRange = range(2010, yearEnd+1, 1)

data_to_get = {
	'POPESTIMATE':[],'DOMESTICMIG':[],'INTERNATIONALMIG':[],
	'NETMIG':[],'DEATHS':[],'BIRTHS':[]}

headers_output = ['COUNTY_FIPS_CODE','COUNTY_ANSICODE','COUNTY_NAME', 'STATE_NAME',
				  'COUNTY_INTPTLAT','COUNTY_INTPTLONG','ABI_REGION','CUSTOM_REGION_ID',
				  'CUSTOM_REGION_NAME', 'YEAR', 'PROPERTY', 'VALUE'
				  ]

for year in yearRange:
	for propCategory in select_headers:
		propKey = propCategory+str(year)
		data_to_get[propCategory].append(propKey)
		#headers_output.append(header)

write_dataOut = open("%s%s" % (r"02_output/population/",'counties_popStats.csv'), 'w',newline='', encoding='utf-8')
writer_dataOut = csv.writer(write_dataOut)
writer_dataOut.writerow(headers_output)


fPath_countyStats = "%s%s" % (r'01_data\Feature_Collections\\','us_counties_stats.geojson')
with fiona.open(fPath_countyStats) as fc_countyStats:
	for feature in fc_countyStats:
		feature_properties = feature['properties']
		countyNs = str(feature_properties['COUNTYNS'])
		if countyNs in customRegions_dict['COUNTY_ANSICODE']:
			idx = customRegions_dict['COUNTY_ANSICODE'].index(countyNs)
			customRegionId = customRegions_dict['DODGE_CUSTOM_REGION'][idx]
			fips = customRegions_dict['COUNTY_FIPS_CODE'][idx]
			ansi = customRegions_dict['COUNTY_ANSICODE'][idx]
			countyName = customRegions_dict['COUNTY_NAME'][idx]
			state = customRegions_dict['COUNTY_STATE'][idx]
			lat = customRegions_dict['COUNTY_INTPTLAT'][idx]
			lon = customRegions_dict['COUNTY_INTPTLONG'][idx]
			for propCategory, propKeys in data_to_get.items():
				for propKey in propKeys:
					year = int(propKey[-4:])
					val = feature_properties[propKey]
					writer_dataOut.writerow([
						fips, ansi, countyName, state, lat, lon, 
						abiRegion, customRegionId, customRegionName,
						year, propCategory, val
						])
print("DONE")