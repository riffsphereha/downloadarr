import os
import requests
import json
import time

import ytmusic
import functions
import ytdlp
import eyed3f

def create_artist_album_dir(base_dir, artist, album):
    artist_album_dir = os.path.join(base_dir, "audio", artist, album)
    os.makedirs(artist_album_dir, exist_ok=True)
    return artist_album_dir

def create_lidarr_dir(base_dir, artist):
    artist_album_dir = os.path.join(base_dir, "audio", artist)
    return artist_album_dir

def create_file_name(folder_path, tracknumber, title):
    filename = str(tracknumber).zfill(2) + " - " + title
    return os.path.join(folder_path, filename)

def get_missing_albums(lidarr_url, api_key):
    # Lidarr API endpoint for missing albums
    endpoint = f"{lidarr_url}/api/v1/wanted/missing"

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }

    missing_albums_list = []

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            missing_albums = response.json()
            for album in missing_albums["records"]:
                album_info = {
                    'artist': album['artist']['artistName'],
                    'album': album['title'],
                    'tracks': album['statistics']['trackCount'],
                    'id': album['id']
                }
                missing_albums_list.append(album_info)
            return missing_albums_list
        else:
            print(f"Failed to fetch missing albums: {response.status_code} - {response.text}")
            return missing_albums_list
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return missing_albums_list

def process_album(arr_url, arr_api_key, path):
    print(path)
    headers = {
        "X-Api-Key": arr_api_key,
        "Content-Type": "application/json"
    }

    data = {
        "name": "DownloadedAlbumsScan",
        "path": path
    }

    url = f"{arr_url}/api/v1/command"

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        return True
    else:
        return False

def youtube_download_missing_albums(lidarr_url, lidarr_api_key, downloaddir, lidarr_rootdir, quality, importdelay):
    print("Download missing lidarr albums from youtube.")
    # retrieve all missing albums from lidarr
    missing_albums_data = get_missing_albums(lidarr_url, lidarr_api_key)
    # if albums are missing
    if missing_albums_data:
        # iterate over all albums
        for album_data in missing_albums_data:
            album_id = album_data["id"]
            album_name = album_data['album']
            print(f"Searching album '{album_name}' ({album_data['tracks']} tracks).")
            # search for an album with the correct name and matching track count
            try:
                album_link = ytmusic.get_youtube_album_matching_track_count_link(album_name, album_data["tracks"])
            except:
                pass
            try:
                if album_link:
                    print(f"    Downloading album '{album_link}'.")
                    # create album download folder and get full path
                    artist_album_dir = create_artist_album_dir(downloaddir, functions.string_cleaner(album_data["artist"]), functions.string_cleaner(album_data['album']))
                    lidarr_dir = create_lidarr_dir(lidarr_rootdir, functions.string_cleaner(album_data["artist"]))
                    # get all youtube links for album
                    youtube_links = ytmusic.get_youtube_track_links(album_link)
                    for link in youtube_links:
                        filename = create_file_name(artist_album_dir, link["track"], functions.string_cleaner(link["title"]))
                        print(f"      Downloading '{filename}'")
                        if ytdlp.download_youtube_audio_track(link["youtube_link"], filename, quality):
                            eyed3f.add_metadata_to_mp3(filename + ".mp3", album_data['artist'], link["title"], album_data['album'], link["track"], str(album_data['tracks']))
                    print(f"    Import into lidarr.")
                    process_album(lidarr_url, lidarr_api_key, lidarr_dir)
                    print(f"    Giving lidarr {importdelay} seconds to process")
                    time.sleep(importdelay)
                else:
                    print(f"    No matching album found.")
            except:
                pass