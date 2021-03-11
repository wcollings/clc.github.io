import json

f=json.load(open("json_record.json"))
n=0
for x in f:
	print("{}+".format(len(x)),end='')
	n+=len(x)

print(n)
