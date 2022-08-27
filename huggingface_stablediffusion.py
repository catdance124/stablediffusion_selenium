from time import sleep
import base64
# selenium modules
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from subprocess import CREATE_NO_WINDOW


class StableDiffusion():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
    
    def quit(self):
        self.driver.quit()
    
    def _search_attribute(self, attribute, condition, timeout, poll_frequency):
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            expected_conditions.presence_of_element_located((attribute, condition))
        )
    
    def search_xpath(self, xpath, timeout=15, poll_frequency=1):
        return self._search_attribute(By.XPATH, xpath, timeout, poll_frequency)

    def search_name(self, name, timeout=15, poll_frequency=1):
        return self._search_attribute(By.NAME, name, timeout, poll_frequency)
    
    def search_class(self, class_name, timeout=15, poll_frequency=1):
        return self._search_attribute(By.CLASS_NAME, class_name, timeout, poll_frequency)
    
    def search_id(self, id, timeout=15, poll_frequency=1):
        return self._search_attribute(By.ID, id, timeout, poll_frequency)

    def generate_images(self, query):
        RETRY_LIMIT = 5
        for i in range(RETRY_LIMIT):
            url = "https://huggingface.co/spaces/stabilityai/stable-diffusion"
            self.driver.get(url)
            # Switch: gradio application iframe
            iframe = self.search_id("iFrameResizer0")
            self.driver.switch_to.frame(iframe)
            # Execute: send query
            elem = self.search_xpath('//input[@placeholder="Enter your prompt"]')
            elem.clear()
            elem.send_keys(query)
            elem.send_keys(Keys.ENTER)
            # Retry: when "This application is too busy! Try again soon."
            sleep(10)
            elems = self.driver.find_elements(By.XPATH, '//*[@id="gallery"]/*/span[contains(@class,"error")]')
            if len(elems) == 0:
                break
            else:
                print(f"error detection, retry...{i+1}")
        # Wait: until processing completes
        _ = self.search_xpath('//*[@id="gallery"]/div[contains(@class,"opacity-0")]', timeout=300, poll_frequency=10)
        # Get: generated images
        elems = self.driver.find_elements(By.XPATH, '//*[@id="gallery"]//*/img')
        binary_imgs = []
        for elem in elems:
            base64_img = elem.get_attribute("src")
            binary_img = base64.b64decode(base64_img.replace('data:image/png;base64,', ''))
            binary_imgs.append(binary_img)
        return binary_imgs