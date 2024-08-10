import csv
import json

from datetime import datetime
import numpy as np

from preprocessing_tools import csv_to_dict
######################################################################################
######################################################################################
headers_data = ['COUNTY_FIPS_CODE','COUNTY_ANSICODE','COUNTY_NAME',
				'COUNTY_INTPTLAT','COUNTY_INTPTLONG','ABI_REGION','CUSTOM_REGION_ID',
				'CUSTOM_REGION_NAME', 'YEAR', 'PROPERTY', 'VALUE']

property_categories = [
	'POPESTIMATE', 'DOMESTICMIG', 
	'INTERNATIONALMIG', 'NETMIG',
	'DEATHS', 'BIRTHS']

path_customRegions = "%s%s" % (r"02_output\\","us_counties_stats.csv")

countyStats_dict = csv_to_dict(path_customRegions,headers_data)
countyStats_dict['CUSTOM_REGION_ID'] =  list(map(int,countyStats_dict['CUSTOM_REGION_ID']))
countyStats_dict['YEAR'] =  list(map(int,countyStats_dict['YEAR']))

custom_region_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9]
output = {}

yearStart = 2010
yearEnd = 2024
yearRange = range(yearStart, yearEnd+1, 1)
keys = []
for crid in custom_region_ids:
	for propKey in property_categories:
		for year in yearRange:
			keys.append([crid, propKey, year])

######################################################################################
write_dataOut = open("%s%s" % (r"02_output\\",'region_stats_summary.csv'), 'w',newline='', encoding='utf-8')
writer_dataOut = csv.writer(write_dataOut)
writer_dataOut.writerow(['CUSTOM_REGION_ID','PROPERTY', 'YEAR', 'TOTAL', 'MEAN','STD', 'MIN', 'MAX'])
######################################################################################
custom_regions_names = {
    '1': {'dodge_custom_region':'1-Northeast', 'abi_region':'Northeast'},
	'2': {'dodge_custom_region':'2-Mid-Atlantic', 'abi_region':'South'},
	'3': {'dodge_custom_region':'3-South-East', 'abi_region':'South'},
	'4': {'dodge_custom_region':'4-Midwest', 'abi_region':'Midwest'},
	'5': {'dodge_custom_region':'5-South-Central', 'abi_region':'South'},
	'6': {'dodge_custom_region':'6-Rocky Mountains', 'abi_region':'West'},
	'7': {'dodge_custom_region':'7-Southwest', 'abi_region':'West'},
	'8': {'dodge_custom_region':'8-Central West', 'abi_region':'West'},
	'9': {'dodge_custom_region':'9-Pacific Northwest', 'abi_region':'West'}}

for key in keys:
	try:
		idx_cridANDpropKey = [index for index, (e0, e1, e2) in 
				enumerate(zip(
					countyStats_dict['CUSTOM_REGION_ID'],
					countyStats_dict['PROPERTY'],
					countyStats_dict['YEAR'])) if 
					e0 == key[0] and e1 == key[1] and e2 == key[2]]
		if customRegionName == '4-Midwest':
			print('4-Midwest', len(idx_cridANDpropKey))
		
		if len(idx_cridANDpropKey) != 0:
			customRegionName = custom_regions_names[str(key[0])]['dodge_custom_region']
			#output[crid]['properties'][propKey] = {}
			get_propValues = list(map(lambda idx: int(countyStats_dict['VALUE'][idx]),idx_cridANDpropKey))
			get_years = list(map(lambda idx: int(countyStats_dict['YEAR'][idx]),idx_cridANDpropKey))
			sum_propValues = sum(get_propValues)
			mean_propValues = np.mean(get_propValues)
			std_propValues = np.std(get_propValues)
			min_propValues = min(get_propValues)
			max_propValues = max(get_propValues)

			writer_dataOut.writerow([
				customRegionName, key[1], key[2], 
				sum_propValues, mean_propValues, std_propValues, 
				min_propValues, max_propValues])
		
			#print(customRegionName, key[1], key[2], sum_propValues, mean_propValues, std_propValues, min_propValues, max_propValues)
		else:
			print(str(key[0]))
	except Exception as e:
		print(e)
		pass

print("DONE")
######################################################################################
######################################################################################