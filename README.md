# Top 2000 Frame Art - Home Assistant Addon

Display NPO Radio 2 now playing artwork on your Samsung Frame TV as a Home Assistant addon.

## Features

- Monitors NPO Radio 2 for currently playing tracks
- Fetches album artwork from Last.fm
- Generates beautiful composite images with station branding
- Automatically uploads to Samsung Frame TV
- Configurable check interval, last.fm API key and Frame TV IP Address

### Step 1: Add this repository as add-on repository in Home Assistant

1. Open Home Assistant web interface
2. Navigate to **Settings** → **Add-ons** → **Add-on Store**
3. Click the menu (three dots) in the top right → **Repositories**
4. Add https://github.com/harmjanr/top2000-frame-art as repository

### Step 2: Install the Addon

The repository should now visible on the add-ons page. Select the add-on and press install

### Step 3: Configure the Addon

Before starting the addon, configure it:

1. Go to the **Configuration** tab
2. Set your options:
   - `tv_ip`: IP address of your Samsung Frame TV (e.g., "192.168.1.123")
   - `check_interval`: How often to check for new tracks in seconds (default: 10)

### Step 4: Start the Addon

1. Go to the **Info** tab
2. Enable **Start on boot** if you want it to start automatically
3. Click **START**

### Step 5: View Logs

- Click on the **Log** tab to see the addon's output
- You should see messages about tracks being detected and uploaded

## Requirements

- Home Assistant OS or Supervised installation
- Samsung Frame TV on the same network
- Samsung Frame TV in Art Mode

## Troubleshooting

### Addon won't start
- Check the logs for error messages
- Verify your TV IP address is correct
- Ensure your TV is powered on and in Art Mode

### Images not uploading to TV
- Confirm TV is on the same network as Home Assistant
- Check that the TV is in Art Mode
- Verify the TV IP address in the configuration

### No track information found
- Check the logs to see if the API is responding
- Verify the channel name is correct
- Ensure you have internet connectivity

## Project Structure

```
top2000-frame-art/
├── config.json           # Home Assistant addon configuration
├── Dockerfile            # Container image definition
├── run.sh               # Addon entry point script
├── app.py               # Main application loop
├── now_playing.py       # NPO Radio API integration
├── track_cover.py       # Last.fm cover art fetching
├── image_generator.py   # Composite image creation
├── samsung_frame_upload.py  # Samsung Frame TV integration
├── requirements.txt     # Python dependencies
└── resources/           # Logo images and assets
```

## License

This project monitors NPO Radio and uses the Last.fm API for album artwork.

