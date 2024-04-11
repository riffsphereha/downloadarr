import eyed3

def add_metadata_to_mp3(mp3_file, artist, title, album, track_num, total_tracks):
    print(f"        Adding metadata to {mp3_file}")
    audiofile = eyed3.load(mp3_file)
    
    if audiofile.tag is None:
        audiofile.initTag()
    
    audiofile.tag.artist = artist
    audiofile.tag.title = title
    audiofile.tag.album = album
    audiofile.tag.track_num = track_num  # Track number

    audiofile.tag.save()