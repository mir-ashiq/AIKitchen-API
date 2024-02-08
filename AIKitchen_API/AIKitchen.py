import requests 
import os 
import dotenv
import datetime 
import json 
import base64 
import pickle
import logging 
from time import sleep
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class Login:
    def __init__(self, email=None, password=None):
        self.url = 'https://aitestkitchen.withgoogle.com/experiments/music-lm'
        self.email = email or os.environ.get("EMAIL")
        self.password = password or os.environ.get("PASSWORD")
        if os.environ.get("TOKEN") == "":
            self.token = self.get_token()
        elif self.token_refresh():
            self.token = self.get_token()
        else:
            self.token = os.environ.get("TOKEN")
    def save_cookies(self, driver, filename):
        pickle.dump(driver.get_cookies(), open(filename, 'wb'))
        print("Cookies saved successfully")

    def add_cookies(self, driver, filename):
        cookies = pickle.load(open(filename, 'rb'))
        
        # Enables network tracking so we may use Network.setCookie method
        driver.execute_cdp_cmd('Network.enable', {})

        # Iterate through pickle dict and add all the cookies
        for cookie in cookies:
            # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
            if 'expiry' in cookie:
                cookie['expires'] = cookie['expiry']
                del cookie['expiry']

            # Set the actual cookie
            driver.execute_cdp_cmd('Network.setCookie', cookie)

        # Disable network tracking
        driver.execute_cdp_cmd('Network.disable', {})
        
        print("Cookies added successfully")
        return True

    def get_token(self):
        driver = uc.Chrome(headless=True)
        try:
            driver.get(self.url)
            if os.path.exists("cookies.pkl"):
                self.add_cookies(driver,"cookies.pkl")
                print("Added Cookies successfully.")
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in with Google']"))).click()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in']"))).click()

                #driver.switch_to.window(driver.window_handles[1])
                logging.info('Logging in...')
                sleep(2)
                print(driver.current_url)
                if driver.current_url=="https://aitestkitchen.withgoogle.com/api/auth/signin?error=Callback":
                    print("Got error...")
                    driver.delete_all_cookies()
                    print("deleted all cookies!")
                    driver.get(self.url)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in with Google']"))).click()
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in']"))).click()
                    logging.info('Retrying login...')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{self.email}\n')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{self.password}\n')
                logging.info('Successfully logged in')

                #driver.switch_to.window(driver.window_handles[0])
                sleep(3) #20 seconds for two factor authentication 
            except Exception as e:
                logging.error("An error occurred while interacting with the webpage, details: " + str(e))
                raise Exception("Unable to fetch token due to Selenium interaction error")
            sleep(2)
            logging.info('Getting OAuth 2.0 token')
            cookies = driver.get_cookies()
            self.save_cookies(driver, "cookies.pkl")
            #print(cookies)
            driver.get("https://aitestkitchen.withgoogle.com/api/auth/session")
            jsondata = json.loads(driver.find_element(By.XPATH, "/html/body").text)
            
        except Exception as e:
            logging.error("An error occurred while fetching the token, details: " + str(e))
            raise Exception("Unable to fetch token due to browser error")

        finally:
            driver.quit()
            
        token = jsondata["access_token"]

        dotenv.set_key(dotenv_file, "TOKEN", str(token))
        os.environ["TOKEN"] = str(token)
        dotenv.set_key(dotenv_file, "EXPIRATION_TIMESTAMP", str(datetime.datetime.now() + datetime.timedelta(minutes=59)))
        os.environ["EXPIRATION_TIMESTAMP"] = str(datetime.datetime.now() + datetime.timedelta(minutes=59))

        logging.info('OAuth 2.0 token obtained')
        return token

    def token_refresh(self):
        current_timestamp = datetime.datetime.now().replace(microsecond=0)
        expiration_timestamp = datetime.datetime.strptime(os.environ['EXPIRATION_TIMESTAMP'],  '%Y-%m-%d %H:%M:%S.%f')

        difference = current_timestamp - expiration_timestamp
        if difference >= datetime.timedelta(minutes=0):
            return True
        else:
            return False

class Music:
    musiclm_url = "https://content-aisandbox-pa.googleapis.com/v1:soundDemo?alt=json"
    def get_tracks(self, input, generationCount, token):
        if not isinstance(generationCount, int):
            generationCount = 2
        generationCount = min(8, max(1, generationCount))

        payload = json.dumps({
        "generationCount": generationCount,
        "input": {
            "textInput": input
        },
        "soundLengthSeconds": 30  # this doesn't change anything 
        })

        headers = {
        'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.post(self.musiclm_url, headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            logging.error("Can't connect to the server.")
            # Bad Gateway
            return 502
        if response.status_code == 400:
                logging.error("Oops, can't generate audio for that.")
                # Bad Request
                return 400
        
        tracks = []
        for sound in response.json()['sounds']:
            tracks.append(sound["data"])

        return tracks

    def b64toMP3(self, tracks_list, filename):
        count = 0
        new_filename = filename
        while os.path.exists(new_filename):
            count += 1
            new_filename = f'{filename} ({count})'

        os.mkdir(new_filename)

        for i, track in enumerate(tracks_list):
            with open(f"{new_filename}/track{i+1}.mp3", "wb") as f:
                f.write(base64.b64decode(track))

        logging.info("Tracks successfully generated!")
        # Successful Request
        return 200

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