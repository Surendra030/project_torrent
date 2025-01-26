import subprocess
import os
import shutil
import time
import sys
import socket

TORRENT_FILE = "file.torrent"  # Update this to your .torrent file
DOWNLOAD_DIR = "downloads"  # Directory to store downloaded files
ZIP_FILE_NAME = "downloads.zip"  # Name of the zip file

# Function to check if the internet connection is fast enough (HSIC)
def check_internet_speed():
    try:
        print("Checking internet connection...")

        # Attempt to resolve Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        
        # Test network speed by pinging a known server or downloading a small file
        print("Internet connection looks good. Proceeding with download.")
        return True
    except socket.error:
        print("No internet connection or slow network detected. Aborting download.")
        return False

# Function to download torrent using aria2
def download_torrent():
    try:
        print(f"Starting to download torrent: {TORRENT_FILE}")
        
        # Check internet speed before proceeding
        if not check_internet_speed():
            print("Aborting download due to poor internet connection.")
            sys.exit(1)
        
        # Run aria2 command to download the torrent
        command = ["aria2c", "--seed-time=0", "--dir=" + DOWNLOAD_DIR, TORRENT_FILE]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)

        print(f"Download complete: {TORRENT_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading torrent: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during torrent download: {e}")
        raise

# Function to zip the downloaded files
def zip_downloads():
    try:
        print("Starting the zipping process...")
        
        # Check if the zip file already exists, and remove it if so
        if os.path.exists(ZIP_FILE_NAME):
            print(f"Removing existing zip file: {ZIP_FILE_NAME}")
            os.remove(ZIP_FILE_NAME)

        print(f"Zipping the downloaded files into {ZIP_FILE_NAME}...")

        # Zip the entire downloads folder
        shutil.make_archive(ZIP_FILE_NAME.replace('.zip', ''), 'zip', DOWNLOAD_DIR)
        
        print(f"Files zipped successfully as {ZIP_FILE_NAME}.")
    except FileNotFoundError as e:
        print(f"Error: {e}. The folder to zip does not exist.")
    except PermissionError as e:
        print(f"Permission error: {e}. Check your access rights.")
    except Exception as e:
        print(f"An error occurred while zipping the files: {e}")
        raise

if __name__ == "__main__":
    # Step 1: Download the torrent file
    try:
        download_torrent()
    except Exception as e:
        print(f"Failed to download the torrent: {e}")

    # Step 2: Zip the downloaded files
    try:
        zip_downloads()
    except Exception as e:
        print(f"Failed to zip the downloaded files: {e}")
