import requests
import shutil

def download_image(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        print('Image downloaded successfully!')
    else:
        print('Unable to download the image.')

# Example usage
image_url = 'https://example.com/image.jpg'
save_path = '/path/to/save/image.jpg'

download_image(image_url, save_path)