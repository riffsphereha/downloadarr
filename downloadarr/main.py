# Global modules
import sys
import os

# My modules
import functions
import lidarr
import readarr

debug = os.environ.get("DEBUG")

if debug=="True":
    print("Running in debug mode")
    configdir="/code/downloadarr2"
else:
    configdir="/config"

configfile=configdir+"/config.yml"

config = functions.load_config(configfile)
if config is None:
    sys.exit(1)

downloaddir = config["downloadarr"]["downloaddir"]

if "lidarr_album_from_youtube" in config["downloadarr"]["download"]:    
    lidarr_album_from_youtube = config["downloadarr"]["download"]["lidarr_album_from_youtube"]
else:
    lidarr_album_from_youtube = False
if lidarr_album_from_youtube:
    if "lidarr" in config:
        if config["lidarr"] != None:
            if "url" in config["lidarr"]:
                lidarr_url = config["lidarr"]["url"]
            else:
                print("Lidarr URL not set, exiting")
                sys.exit(1)
            if "api" in config["lidarr"]:
                lidarr_api_key = config["lidarr"]["api"]
            else:
                print("Lidarr API not set, exiting")
                sys.exit(1)
            if "importdir" in config["lidarr"]:
                lidarr_rootdir = config["lidarr"]["importdir"]
            else:
                print(f"Lidarr importdir not set, using downloaddir '{downloaddir}'")
                lidarr_rootdir = downloaddir
            if "quality" in config["youtube_music"]:
                quality = config["youtube_music"]["quality"]
            else:
                print("Youtube music quality not set, defaulting to 192kbps ")
                quality = 192
            if "importdelay" in config["lidarr"]:
                lidarr_importdelay = config["lidarr"]["importdelay"]
            else:
                print("Lidarr importdelay not set, defaulting to 5 seconds")
                lidarr_importdelay = 5
        else:
            print("Lidarr config missing")
            sys.exit(1)
    else:
        print("Lidarr config missing")
        sys.exit(1)
    lidarr.youtube_download_missing_albums(lidarr_url, lidarr_api_key, downloaddir, lidarr_rootdir, quality, lidarr_importdelay)
else:
    print("Downloading missing music albums from youtube is disabled, skipping.")


if "readarr_books_from_libgen" in config["downloadarr"]["download"]:
    readarr_books_from_libgen = config["downloadarr"]["download"]["readarr_books_from_libgen"]
else:
    readarr_books_from_libgen = False
if readarr_books_from_libgen:
    if "readarr" in config:
        if config["readarr"] != None:
            if "url" in config["readarr"]:
                readarr_url = config["readarr"]["url"]
            else:
                print("Readarr URL not set, exiting")
                sys.exit(1)
            if "api" in config["readarr"]:
                readarr_api_key = config["readarr"]["api"]
            else:
                print("Readarr API not set, exiting")
                sys.exit(1)
            if "importdir" in config["readarr"]:
                readarr_rootdir = config["readarr"]["importdir"]
            else:
                print(f"Readarr importdir not set, using downloaddir '{downloaddir}'")
                readarr_rootdir = downloaddir
            if "importdelay" in config["readarr"]:
                readarr_importdelay = config["readarr"]["importdelay"]
            else:
                print("Readarr importdelay not set, defaulting to 15 seconds")
                readarr_importdelay = 15
        else:
            print("Readarr config missing")
            sys.exit(1)
    else:
        print("Readarr config missing")
        sys.exit(1)
    readarr.libgen_download_missing_books(readarr_url, readarr_api_key, downloaddir, readarr_rootdir, readarr_importdelay)
else:
    print("Downloading missing books from libgen is disabled, skipping.")
