from ytmusicapi import YTMusic

import functions

def get_youtube_album_link(album_name, wanted_match=1):
    ytmusic = YTMusic()
    match = 0
    try:
        # Search for the album
        search_results = ytmusic.search(album_name, filter='albums')
        for item in search_results:
            if functions.string_cleaner(album_name).lower() == functions.string_cleaner(item["title"]).lower():
                match = match + 1
                if match==wanted_match:
                    return item["browseId"], match
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, 0

    return None, 0

def get_youtube_track_links(browse_id):
    ytmusic = YTMusic()
    trackcounter=0
    
    # Get the album tracks
    album_info = ytmusic.get_album(browse_id)
    
    if album_info and 'tracks' in album_info:
        tracks = album_info['tracks']
        youtube_links = []
        for track in tracks:
            trackcounter = trackcounter + 1
            title = track['title']
            video_id = track['videoId']
            youtube_link = f"https://www.youtube.com/watch?v={video_id}"
            youtube_links.append({'title': title, 'youtube_link': youtube_link, 'track': trackcounter})
        
        return youtube_links
    else:
        print("Album tracks not found.")
        return None

def get_youtube_album_matching_track_count_link(album_name, trackcount):
    # Function to iterate over all albums with the correct name, and verify track count is right.
    album_downloaded = False
    album_link, match = get_youtube_album_link(album_name, 1)
    while album_link and not album_downloaded:
        youtube_links = get_youtube_track_links(album_link)
        if youtube_links:
            print(f"  Album '{album_link}' has {len(youtube_links)} tracks, expecting {trackcount}.")
            if len(youtube_links) == trackcount:
                for link in youtube_links:
                    album_downloaded = True
                    return album_link
        else:
            return None
        if not album_downloaded:
            album_link, match = get_youtube_album_link(album_name, match + 1)
    if not album_downloaded:
        return None

