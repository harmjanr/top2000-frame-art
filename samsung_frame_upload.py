import asyncio
import logging
import os
import time
from samsungtvws.async_art import SamsungTVAsyncArt
from samsungtvws import exceptions

logging.basicConfig(level=logging.INFO)


async def check_artmode_async(tv_ip):
    """
    Checks if the Samsung Frame TV is currently in art mode.
    
    Args:
        tv_ip (str): IP address of the Samsung Frame TV
    
    Returns:
        bool: True if TV is in art mode, False otherwise
    """
    tv = None
    try:
        tv = SamsungTVAsyncArt(host=tv_ip, port=8002)
        await tv.start_listening()
        
        artmode_info = await tv.get_artmode()
        # The response can be either a string "on"/"off" or a dict {"value": "on"}
        if isinstance(artmode_info, dict):
            is_artmode = artmode_info.get('value') == 'on'
        else:
            is_artmode = str(artmode_info).lower() == 'on'
        
        logging.info(f'Art mode status: {"on" if is_artmode else "off"}')
        return is_artmode
        
    except Exception as e:
        logging.error(f'Error checking art mode: {e}')
        return False
    finally:
        if tv:
            try:
                await tv.close()
            except:
                pass


async def upload_to_samsung_frame_async(tv_ip, image_path, matte="none", matte_color="black"):
    """
    Uploads an image to a Samsung Frame TV asynchronously.
    
    Args:
        tv_ip (str): IP address of the Samsung Frame TV
        image_path (str): Path to the image file to upload
        matte (str): Matte style to apply (default: "none")
        matte_color (str): Matte color to apply (default: "black")
    
    Returns:
        str: Content ID of the uploaded image, or None if failed
    """
    # Set the matte variable
    if matte != 'none':
        matte_var = f"{matte}_{matte_color}"
    else:
        matte_var = matte
    
    tv = None
    
    try:
        tv = SamsungTVAsyncArt(host=tv_ip, port=8002)
        await tv.start_listening()
        
        # Check if TV is supported
        supported = await tv.supported()
        if not supported:
            logging.error('This TV is not supported')
            return None
        
        logging.info('TV is supported')
        
        # Get current artwork to delete later
        current_content_id = None
        try:
            current_info = await tv.get_current()
            current_content_id = current_info.get('content_id')
        except Exception as e:
            logging.warning(f'Could not get current artwork: {e}')
        
        # Upload the image
        with open(image_path, "rb") as f:
            file_data = f.read()
        
        file_type = os.path.splitext(image_path)[1][1:]  # Get extension without dot
        
        logging.info(f'Uploading {len(file_data)} bytes as {file_type}...')
        content_id = await tv.upload(file_data, file_type=file_type, matte=matte_var)
        logging.info(f'Uploaded {image_path} to TV as {content_id}')
        
        # Give TV time to process the upload
        await asyncio.sleep(2)
        
        # Select the uploaded image
        await tv.select_image(content_id, show=True)
        logging.info(f'Set artwork to {content_id}')
        
        # Delete the previous artwork
        if current_content_id:
            try:
                await asyncio.sleep(1)
                await tv.delete_list([current_content_id])
                logging.info(f'Deleted previous artwork: {current_content_id}')
            except Exception as e:
                logging.warning(f'Could not delete previous artwork: {e}')
        
        return content_id
        
    except exceptions.ResponseError as e:
        logging.error(f'Response error: {e}')
        return None
    except BrokenPipeError as e:
        logging.error(f'Connection lost to TV (broken pipe). Is the TV on and accessible?')
        return None
    except ConnectionError as e:
        logging.error(f'Connection error: {e}. Check TV IP address and network.')
        return None
    except Exception as e:
        logging.error(f'Error uploading to Samsung Frame: {e}')
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Clean up connection
        if tv:
            try:
                await tv.close()
            except:
                pass


def check_artmode(tv_ip):
    """
    Synchronous wrapper for checking art mode status.
    
    Args:
        tv_ip (str): IP address of the Samsung Frame TV
    
    Returns:
        bool: True if TV is in art mode, False otherwise
    """
    return asyncio.run(check_artmode_async(tv_ip))


def upload_to_samsung_frame(tv_ip, image_path, matte="none", matte_color="black"):
    """
    Synchronous wrapper for uploading to Samsung Frame TV.
    
    Args:
        tv_ip (str): IP address of the Samsung Frame TV
        image_path (str): Path to the image file to upload
        matte (str): Matte style to apply (default: "none")
        matte_color (str): Matte color to apply (default: "black")
    
    Returns:
        str: Content ID of the uploaded image, or None if failed
    """
    return asyncio.run(upload_to_samsung_frame_async(tv_ip, image_path, matte, matte_color))


if __name__ == "__main__":
    # Test upload
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python samsung_frame_upload.py <tv_ip> <image_path>")
        sys.exit(1)
    
    tv_ip = sys.argv[1]
    image_path = sys.argv[2]
    
    result = upload_to_samsung_frame(tv_ip, image_path)
    if result:
        print(f"Successfully uploaded image. Content ID: {result}")
    else:
        print("Failed to upload image")
