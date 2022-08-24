from abc import ABC
from cgitb import text
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from abc import abstractmethod
from credentials import username, password



class Crawler(ABC):

    s = Service('C:/Users/Qorpo/.wdm/drivers/chromedriver/win32/chromedriver.exe')
    

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.url = 'https://clinicweb.vitta.me/clinicweb/login.jsp'
    
    def clicarXpath(self, xpath: str) -> None:
        self.driver.find_element(By.XPATH, xpath).click()
        print(f"Clicando no botão: {self.driver.find_element(By.XPATH, xpath).text}\n")
        time.sleep(3)
        

    def _sendCredentials(self) -> None:
        self.driver.find_element(By.NAME, 'login').send_keys(username)
        self.driver.find_element(By.NAME, 'senha').send_keys(password)
        self.clicarXpath('//*[@id="frmlogin"]/div/div/div[1]/div[3]/button')


    @abstractmethod
    def scrape(self, **kwargs) -> None:
        pass
        

class CrawlerConsulta(Crawler):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def scrape(self, **kwargs) -> None:
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.maximize_window()
        self.driver.get(self.url)
        self._sendCredentials()

        self.clicarXpath('//*[@id="tab_top"]/li[4]/a') # clicando em financeiro
        self.clicarXpath('//*[@id="tab_top"]/li[4]/ul/li[2]/a') # clicando em relatorio
        self.clicarXpath('//*[@id="tab_top"]/li[4]/ul/li[2]/ul/li[10]/a') # clicando em financeiro