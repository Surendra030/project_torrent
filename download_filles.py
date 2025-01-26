import libtorrent as lt
import time
import os
import shutil

TORRENT_FILE = "file.torrent"  # Update to your torrent file's name
DOWNLOAD_DIR = "downloads"     # Directory to store downloaded files
ZIP_FILE_NAME = "downloads.zip"  # Name of the zip file


def download_with_libtorrent():
    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Create the download directory if it doesn't exist

        # Create session and add torrent
        ses = lt.session()
        ses.listen_on(6881, 6891)

        print(f"Loading torrent: {TORRENT_FILE}")
        try:
            info = lt.torrent_info(TORRENT_FILE)
            handle = ses.add_torrent({'ti': info, 'save_path': DOWNLOAD_DIR})
        except Exception as e:
            print(f"Error loading torrent file '{TORRENT_FILE}': {e}")
            return

        print(f"Starting torrent download: {info.name()}")

        # Monitor progress
        while not handle.is_seed():
            status = handle.status()
            print(f"Progress: {status.progress * 100:.2f}% | Download rate: {status.download_rate / 1000:.2f} kB/s")
            time.sleep(5)

        print(f"Download complete: {info.name()}")

        # Zip the downloaded files
        zip_downloads()

    except Exception as e:
        print(f"An error occurred during the torrent download process: {e}")


def zip_downloads():
    try:
        if os.path.exists(ZIP_FILE_NAME):
            os.remove(ZIP_FILE_NAME)  # Remove the zip file if it already exists

        print(f"Zipping the downloaded files into {ZIP_FILE_NAME}...")
        shutil.make_archive("downloads", 'zip', DOWNLOAD_DIR)
        print(f"Files zipped successfully as {ZIP_FILE_NAME}.")

    except Exception as e:
        print(f"An error occurred while zipping the files: {e}")


if __name__ == "__main__":
    download_with_libtorrent()
    files = os.listdir(DOWNLOAD_DIR)
    
    if files:
        print("Files downloaded:")
        for file in files:
            print(file)
    else:
        print("No files found in the download directory.")
