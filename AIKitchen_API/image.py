import os
import requests
import json
import base64
import logging

class Image:
    imagefx_url = "https://content-aisandbox-pa.googleapis.com/v1:runImageFx?alt=json"

    def get_image(self, input, generationCount, token):
        if not isinstance(generationCount, int):
            generationCount = 2
        generationCount = min(8, max(1, generationCount))

        headers = {
            "Referer": "https://aitestkitchen.withgoogle.com",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }

        payload = {
            "userInput": {
                "candidatesCount": generationCount,
                "prompts": [input]
            },
            "clientContext": {
                "sessionId": "93fe8ad1-776d-469a-b769-e713523926f8",
                "tool": "IMAGE_FX"
            },
            "aspectRatio": "IMAGE_ASPECT_RATIO_SQUARE"
        }

        try:
            response = requests.post(self.imagefx_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses
            if response.status_code == 200:
                # Check if the response content is not empty
                if response.text:
                    images = []
                    for image in response.json()["imagePanels"][0]["generatedImages"]:
                        images.append(image["encodedImage"])
                    return images
                else:
                    logging.error("Response content is empty.")
                    return 400
            else:
                logging.error(f"Unexpected status code: {response.status_code}")
                return response.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return 502

    
    def b64toImg(self, image_list, filename):
        count = 0
        new_filename = filename
        while os.path.exists(new_filename):
            count += 1
            new_filename = f"{filename} {count}"
        os.makedirs(new_filename)
        
        for i,image in enumerate(image_list):
            with open(f"{new_filename}/Image-{i+1}", "wb") as f:
                f.write(base64.b64decode(image))
        logging.info("Images successfully generated!")
        # Successful Request
        return 200