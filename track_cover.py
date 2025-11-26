import requests
import os

# Last.fm API key - read from environment variable (set by Home Assistant addon)
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")


def get_track_cover(artist, track):
    """
    Fetches the album cover URL from Last.fm API.
    
    Args:
        artist (str): The artist name
        track (str): The track/song name
    
    Returns:
        str: URL of the extralarge album cover image, or None if not found
    """
    try:
        # Query Last.fm API for track info
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "track.getInfo",
            "api_key": LASTFM_API_KEY,
            "artist": artist,
            "track": track,
            "format": "json"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Check if track info exists
        if "track" not in data:
            print(f"No track info found for artist: {artist}, track: {track}")
            return None
        
        # Extract album and images
        track_data = data["track"]
        if "album" not in track_data:
            print(f"No album info found for track: {track} by {artist}")
            return None
        
        album_data = track_data["album"]
        if "image" not in album_data or len(album_data["image"]) == 0:
            print(f"No album cover found for track: {track} by {artist}")
            return None
        
        # Find the extralarge image
        for img in album_data["image"]:
            if img["size"] == "extralarge":
                image_url = img["#text"]
                if image_url:
                    print(f"Found album cover for {artist} - {track}")
                    return image_url
        
        print(f"No extralarge image found for track: {track} by {artist}")
        return None
        
    except Exception as e:
        print(f"Error fetching album cover: {e}")
        return None
