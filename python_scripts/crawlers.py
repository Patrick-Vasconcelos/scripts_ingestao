from abc import ABC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from abc import abstractmethod
from credentials import username, password



class Crawler(ABC):

    s = Service('C:/Users/Qorpo/.wdm/drivers/chromedriver/win32/chromedriver.exe')
    options = Options()
    options.add_argument('window-size=400,800')

    def __init__(self, url) -> None:
        super().__init__()
        self.url = url
        

    def _sendCredentials(self) -> None:
        self.driver.find_element(By.NAME, 'login').send_keys(username)
        self.driver.find_element(By.NAME, 'senha').send_keys(password)

    @abstractmethod
    def get_data(self, **kwargs):
        self.driver = webdriver.Chrome(service=self.s,options=self.options)
        self.driver.get(self.url)
        self._sendCredentials
        pass

