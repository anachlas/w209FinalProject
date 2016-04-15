import json

f = open('./data/20160408.export.CSV')

locations = {}

for l in f:
	data = l.split('\t')
	loc = data[15][:3]
	if len(loc) !=3:
		continue
	if loc in locations.keys():
		locations[loc] += 1
	else:
		locations[loc] = 1
	print loc

loc_list = []
for l in locations.keys():
	loc_list.append([l,locations[l]])


with open('./data/20160408.locations.json', 'w') as fp:
    json.dump(loc_list, fp)