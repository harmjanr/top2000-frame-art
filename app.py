import time
import os
from datetime import datetime
from now_playing import get_now_playing
from track_cover import get_track_cover
from image_generator import create_now_playing_image
from samsung_frame_upload import upload_to_samsung_frame, check_artmode

# Configuration - read from environment variables (set by Home Assistant addon)
TV_IP = os.getenv("TV_IP")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))
CHANNEL = "npo-radio-2"  # Fixed to NPO Radio 2

if __name__ == "__main__":
    last_playing_id = None
    
    print(f"Starting now playing monitor for {CHANNEL}... (Press Ctrl+C to stop)")
    print(f"TV IP: {TV_IP}, Check interval: {CHECK_INTERVAL}s")
    
    while True:
        try:
            result = get_now_playing(channel=CHANNEL)
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {result}")
            
            # Only process if it's a new track
            if result.id != last_playing_id:
                # Check if TV is in art mode before processing
                if not check_artmode(TV_IP):
                    print("TV is not in art mode - skipping update")
                    last_playing_id = result.id
                    continue
                
                cover_url = get_track_cover(result.artist, result.song)
                if cover_url:                   
                    # Generate the composite image
                    output_path = create_now_playing_image(result.artist, result.song, cover_url)
                    
                    # Upload to Samsung Frame TV
                    content_id = upload_to_samsung_frame(TV_IP, output_path)
                else:
                    print("Track cover not found")
                last_playing_id = result.id
        except KeyboardInterrupt:
            print("\n\nStopping monitor...")
            break
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(CHECK_INTERVAL)
