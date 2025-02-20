import requests
import json

def get_parsed_screen_elements(image_path):
    url = 'http://localhost:58082/process_image'
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        parsed_content = response.json().get('parsed_content')
        elements = []

        # Split parsed content into lines and process each line
        for line in parsed_content.splitlines():
            parts = line.split(": ", 1)  # Split at the first ": " only
            if len(parts) == 2:
                key, value = parts
                if key.startswith("Text Box ID"):
                    id_num = int(key.split()[-1])  # Get the last part as the ID
                    elements.append({
                        "Type": "TextBox",
                        "ID": id_num,
                        "Text": value.strip(),
                        "Context": "General Text"
                    })
                elif key.startswith("Icon Box ID"):
                    id_num = int(key.split()[-1])  # Get the last part as the ID
                    elements.append({
                        "Type": "IconBox",
                        "ID": id_num,
                        "Description": value.strip(),
                        "Context": "UI Icon"
                    })
            else:
                print(f"Skipping unrecognized line format: {line}")

        # Create structured JSON
        output_json = {
            "Screen Elements": elements
        }

        # Print the JSON output
        print(json.dumps(output_json, indent=4))

        # Optional: Save to a JSON file
        with open('ocr_output.json', 'w') as json_file:
            json.dump(output_json, json_file, indent=4)
        print("JSON output saved as 'ocr_output.json'")
    else:
        print(f"Error: {response.status_code}")

# Example usage
image_path = '/workspace/imgs/google_page.png'
get_parsed_screen_elements(image_path)
