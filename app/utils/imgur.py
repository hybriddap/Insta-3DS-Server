import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def upload_to_imgur(png_data):
    png_file = png_data.read()
    encoded_image = base64.b64encode(png_file)
    headers = {
        'Authorization': f'Client-ID {os.getenv("imgur_client_id")}'
    }
    data = {
        'image': encoded_image,
        'type': 'base64'
    }

    try:
        response = requests.post('https://api.imgur.com/3/image', headers=headers, data=data)
        response.raise_for_status()

        result = response.json()

        if result['success']:
            #print("Image uploaded successfully!")
            #print(f"Link: {result['data']['link']}")
            #print(f"Deletehash: {result['data']['deletehash']}")
            return result['data']['link']
        else:
            #print("Image upload failed.")
            #print(f"Error: {result['data']['error']}")
            return "Image upload failed."
    except:
        #print(f"An error occurred during the request.")
        return "An error occurred during the request."

