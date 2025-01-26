from mega import Mega
import os

keys= os.getenv("M_TOKEN")

keys = keys.split("_")

try:

    mega = Mega()
    m = mega.login(keys[0],keys[1])
except Exception as e:
    print("Error failed to login...")
    
try:
    files = os.listdir()
    for file in files:
        if '.zip' in file:
            
            m.upload(file)
except Exception as e:
    print("Error failed to upload...")

