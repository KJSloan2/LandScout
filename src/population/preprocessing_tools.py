import numpy as np
import csv
from datetime import datetime
# Requires Numpy
def interpolate_conStarts(inputData, header, steps):
	newData = {'DATE':[], 'MONTH':[], 'YEAR':[]}
	newData[header] = []
	column = inputData[header]
	if len(column) > 1:
		years_argSort = np.argsort(inputData['YEAR'])
		years_sorted = list(map(lambda idx: inputData['YEAR'][idx], years_argSort))
		column_sorted = list(map(lambda idx: column[idx], years_argSort))
		for i in range(0, len(column_sorted) - 1):
			startVal = column_sorted[i]
			endVal = column_sorted[i + 1]
			startYear = years_sorted[i]
			endYear = years_sorted[i + 1]
			values_interpolated = np.linspace(startVal, endVal, 12)
			delta = endVal-startVal
			stepSize = delta/steps+1
			for j, interp in enumerate(values_interpolated):
				month = j + 1
				if month < 10:
					month_str = "0" + str(month)
				else:
					month_str = str(month)
				#year = startYear + (j * (endYear - startYear) // steps)
				date = month_str + "/01/" + str(startYear)
				if date not in newData['DATE']:
					newData[header].append(int(interp))
					newData['DATE'].append(date)
					newData['MONTH'].append(month)
					newData['YEAR'].append(startYear)
	return newData

def interpolate_tween_months(vals, years, steps):
	newData = {'DATE':[], 'MONTH':[], 'YEAR':[], 'VALUE':[]}
	if len(vals) > 1:
		years_argSort = np.argsort(years)
		years_sorted = list(map(lambda idx: years[idx], years_argSort))
		vals_sorted = list(map(lambda idx: vals[idx], years_argSort))
		for i in range(0, len(vals_sorted) - 1):
			startVal = vals_sorted[i]
			endVal = vals_sorted[i + 1]
			startYear = years_sorted[i]
			endYear = years_sorted[i + 1]
			values_interpolated = np.linspace(float(startVal), float(endVal), steps)
			#delta = endVal-startVal
			#stepSize = delta/steps+1
			for j, interp in enumerate(values_interpolated):
				month = j + 1
				if month < 10:
					month_str = "0" + str(month)
				else:
					month_str = str(month)
				#year = startYear + (j * (endYear - startYear) // steps)
				date = month_str + "/01/" + str(startYear)
				if date not in newData['DATE']:
					newData['VALUE'].append(int(interp))
					newData['DATE'].append(date)
					newData['MONTH'].append(month)
					newData['YEAR'].append(startYear)
	return newData

def generate_dates(year_range):
	output = []
	for y in range(year_range[0],year_range[1],1):
		for m in range(1,13,1):
			if m < 10:
				m = "0"+str(m)
			else:
				m = str(m)
			date = str(m+'/01/'+str(y))
			output.append(date)
	return output


def csv_to_dict(dataPath,headers):
	headersLen = len(headers)
	output = {}
	with open(dataPath, 'r', newline='') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter = ',')
		csv_headers = []
		for row in csv_reader:
			csv_headers.append(row)
			break
		csv_headers = csv_headers[0]
		index_dict = {}
		for header in headers:
			if header in csv_headers:
				idx = csv_headers.index(header)
				index_dict[header] = idx
				output[header] = []
		next(csv_reader)
		for row in csv_reader:
			if len(row) == headersLen:
				for header, idx in index_dict.items():
					output[header].append(row[idx])
	return output


def is_date_in_range(date_str, start_date_str, end_date_str):
    date_format = '%m/%d/%Y'
    date = datetime.strptime(date_str, date_format)
    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)
    return start_date <= date <= end_date