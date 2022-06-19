import json

my_dict = {}
my_dict["ip"] = 2345321
my_dict["port"] = 44443
my_dict["data_id"] = 2

json_str = json.dumps(my_dict)
print(json_str)
loaded_dict = json.loads(json_str)
print(loaded_dict)
ip = loaded_dict.get("ip")
port = loaded_dict.get("port")
print(ip)
print(port)
# json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
