from pathlib import Path
from configparser import ConfigParser
import json


ini_file = Path('../mysql.ini')
cfg = ConfigParser()
cfg.read(ini_file)

# d = {}
# for i in cfg.items():
#     d[i[0]] = dict(cfg.items(i[0]))
# print(d)
d = {i[0]: dict(cfg.items(i[0])) for i in cfg.items()}
print(json.dumps(d))
