import json
import uuid

string = '{"2": 100, "3": 200}'
res = json.loads(string)
res.pop('5', None)
res.pop('2')

pop = 1.5

