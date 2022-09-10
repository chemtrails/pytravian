from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec


class Bot():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.headless = False
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )


    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

            
    def locate(self, by, element, t):
        located = WebDriverWait(self.driver, t).until(
            ec.presence_of_element_located((by, element))
        )
        return located 


    def login(self):
        start_url = f'https://{self.server}.travian.com'
        self.driver.get(start_url)
        name_input = self.locate(
            By.CSS_SELECTOR, 
            'input[type="text"]', 
            10
        )
        name_input.send_keys(self.username)
        password_input = self.locate(
            By.CSS_SELECTOR, 
            'input[type="password"]', 
            10
        )
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        self.locate(By.CLASS_NAME, 'map', 10)
        self.crawl(start_url)


    def crawl(self, start_url):
        for x_axis in range(-200, 201):
            for y_axis in range(-200, 201):
                url = f'{start_url}/karte.php?fullscreen=1&x={x_axis}&y={y_axis}'
                self.driver.get(url)
                map_container = self.locate(
                    By.ID, 
                    'mapContainer', 
                    10
                )
                map_container.click()
                title = self.locate(
                    By.XPATH, 
                    '//div[@id="tileDetails"]/h1', 
                    5
                )
                title_text = title.text
                print(title_text)


if __name__ == '__main__':
    bot = Bot('server', 'username', 'password')       #   server e.g. 'gos.x1.international'
    bot.login()
