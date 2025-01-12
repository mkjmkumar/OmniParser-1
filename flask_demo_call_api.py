import requests

# Function to call the OmniParser API
def get_parsed_screen_elements(image_path):
    url = 'http://localhost:58090/process_image'
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Parsed Screen Elements:")
        print(response.json().get('parsed_content'))
    else:
        print(f"Error: {response.status_code}")

# Example usage with the correct path to the image
image_path = '/workspace/imgs/google_page.png'
get_parsed_screen_elements(image_path)
