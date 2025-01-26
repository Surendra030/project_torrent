from mega import Mega
import os

keys = os.getenv("M_TOKEN")

if not keys:
    print("Error: MEGA token not found in environment variables.")
    exit(1)

keys = keys.split("_")

try:
    mega = Mega()
    m = mega.login(keys[0], keys[1])
except Exception as e:
    print(f"Error logging into MEGA: {e}")
    exit(1)

try:
    files = os.listdir()
    for file in files:
        if '.zip' in file:
            print(f"Uploading {file} to MEGA...")
            m.upload(file)
            print(f"Uploaded {file} successfully.")
except Exception as e:
    print(f"Error uploading files: {e}")
    exit(1)
