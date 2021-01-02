import json

with open('./jquery.json') as f:
    data = json.load(f)
with open('./jquery.json', 'w') as n_f:
    json.dump(data, n_f, indent=2)
