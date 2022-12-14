from abc import ABC
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from abc import abstractmethod
from credentials import username, password



class Crawler(ABC):

    s = Service('C:/Users/Qorpo/.wdm/drivers/chromedriver/win32/chromedriver.exe')
    

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.url = 'https://clinicweb.vitta.me/clinicweb/login.jsp'
    
    def timer(self) -> None:
        time.sleep(5)
    
    
    def clicarXpath(self, xpath: str, msg : str = None) -> None:

        if msg is None:
            print(f"Clicando no botão: {self.driver.find_element(By.XPATH, xpath).text}")
        else: 
            print(msg)
        self.driver.find_element(By.XPATH, xpath).click()
        self.timer()
        

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

    def sendDates(self,startDate : datetime.date, endDate: datetime.date) -> None:

        self.startDate = startDate.strftime('%d/%m/%Y')
        self.endDate = startDate.strftime('%d/%m/%Y')
        print(f"Consultando relatorio de consultas de {startDate} ate {endDate}")

        start_date = self.driver.find_element(By.NAME, 'de')
        start_date.clear()
        start_date.send_keys(self.startDate)

        end_date = self.driver.find_element(By.NAME, 'ate')
        end_date.clear()
        end_date.send_keys(self.endDate)


    
    def scrape(self, startDate : datetime.date, endDate : datetime.date, **kwargs) -> None:
        self.option = Options()
        self.option.add_argument("--headless")
        self.driver = webdriver.Chrome(service=self.s, chrome_options=self.option)
        self.driver.maximize_window()
        self.driver.get(self.url)
        self._sendCredentials()

        self.timer()
        
        self.clicarXpath('//*[@id="tab_top"]/li[4]/a') # clicando em financeiro
        self.clicarXpath('//*[@id="tab_top"]/li[4]/ul/li[2]/a') # clicando em relatorio
        self.clicarXpath('//*[@id="tab_top"]/li[4]/ul/li[2]/ul/li[10]/a') # clicando em financeiro
        self.sendDates(startDate=startDate,endDate=endDate) # atribuindo data de inicio e de fim
        self.clicarXpath(xpath='//*[@id="frmcadastrar"]/div[1]/div[26]/div[2]/label', msg='Retirando a opção SADT')
        self.clicarXpath(xpath='//*[@id="frmcadastrar"]/div[1]/div[27]/div/div[2]/label', msg='Selecionando para não separar guias')
        self.clicarXpath(xpath='//*[@id="containerFooter"]/div/div/a/span', msg='Clicando em gerar relatório')
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        print("Buscando dados da tabela")
        df = pd.read_html(self.driver.page_source)[0]

        df.columns = df.iloc[1]
        df.drop([1], inplace=True)
        df.reset_index(drop = True)
        df = df[df.Empresa == 'CLÍNICA QORPO - SAÚDE EM MOVIMENTO']
        df.dropna(axis='columns', inplace=True)
        df['Valor(R$)'] = df['Valor(R$)'].apply(lambda x: x[:-2] + '.' + x[-2:])
        df['Valor(R$)'] = pd.to_numeric(df['Valor(R$)'])

        print("salvando dados da tabela.")
        df.to_excel(f'docs/consultas {startDate}.xlsx', index = False)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.timer()
        self.driver.close()
        self.driver.quit()
        
