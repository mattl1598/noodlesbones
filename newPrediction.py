from pprint import pprint

import numpy
from matplotlib import pyplot as plt
from pandas import DataFrame, read_csv
from firebase import firebase

lines = open("db_url.txt").readlines()
firebase_url = lines[0]

fb = firebase.FirebaseApplication(firebase_url, None)
results = fb.get('/history', None)

y = []
for date in results.keys():
	if results[date]["status"] == "bones":
		y.append(1)
	else:
		y.append(0)

x = list(range(0, len(y)))

lookup = {}
sample_len = 3

for i in range(0, len(y) - sample_len):
	print(f"{i+2}/{len(y)}")
	try:
		test = lookup[str(y[i:i+sample_len])]
		lookup[str(y[i:i+sample_len])] = (test + 2*y[i + sample_len])/3
	except KeyError:
		lookup[str(y[i:i+sample_len])] = y[i+sample_len]

pprint(lookup)
pprint(str(y[-sample_len:]))
pprint(lookup[str(y[-sample_len:])])
