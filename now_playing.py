import requests


class NowPlaying:
    """Represents a currently playing track on NPO Radio."""
    
    def __init__(self, id, song, artist, from_time, until, cover_url=None):
        self.id = id
        self.song = song
        self.artist = artist
        self.from_time = from_time
        self.until = until
        self.cover_url = cover_url
    
    def __repr__(self):
        return f"NowPlaying(id='{self.id}', song='{self.song}', artist='{self.artist}', from='{self.from_time}', until='{self.until}')"
    
    def __str__(self):
        return f"{self.artist} - {self.song} ({self.from_time} to {self.until})"


def get_now_playing(channel="npo-radio-2"):
    """
    Fetches the currently playing track from NPO Radio API.
    
    Args:
        channel (str): The radio channel to query (default: "npo-radio-2")
    
    Returns:
        NowPlaying: Object containing the now playing information
    """
    import time
    
    # Add timestamp to prevent caching
    timestamp = int(time.time() * 1000)
    url = f"https://ios-luister.api.nporadio.nl/graphql?_={timestamp}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    body = {
        "extensions": {
            "clientLibrary": {
                "name": "apollo-ios",
                "version": "1.23.0"
            }
        },
        "operationName": "GetNowPlaying",
        "query": "query GetNowPlaying($channel: String!) { result: radio_track_plays( channel: $channel order_by: \"from\" order_direction: \"desc\" limit: 1 ) { __typename playingTrack: data { __typename id from until song artist track: radio_tracks { __typename cover_url(size: MEDIUM) } } } }",
        "variables": {
            "channel": channel
        }
    }
    
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    
    data = response.json()
    
    # Extract the track data from the nested JSON structure
    track_data = data['data']['result']['playingTrack'][0]
    
    # Extract cover_url if available
    cover_url = None
    if track_data.get('track') and track_data['track'].get('cover_url'):
        cover_url = track_data['track']['cover_url']
        # Remove width and height parameters from URL
        cover_url = cover_url.replace('&width=250&height=250', '')
    
    return NowPlaying(
        id=track_data['id'],
        song=track_data['song'],
        artist=track_data['artist'],
        from_time=track_data['from'],
        until=track_data['until'],
        cover_url=cover_url
    )

