from abc import ABC
from datetime import date, timedelta
from operator import attrgetter
import pandas as pd
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as bs
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
        self.driver = webdriver.Chrome(service=self.s)
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
        
        df = pd.read_html(self.driver.page_source)

        df.head()
        
        
       
        """
        dados_consultas = []
        site = bs(self.page_content, 'html.parser')
        site = site.find('table')     
        consultas = site.find_all('tr')

        for consulta in consultas:
            rows = consulta.find_all('td')
            for row in rows:
                print(row.text)

        
        df = pd.DataFrame(columns= ['Empresa', 'Data de Registro' , 'Hora de Registro',
                            'Data', 'Hora', 'Paciente', 'Carteirinha', 'CPF do Paciente',
                            'Dmed gerado', 'Pagador', 'Executante', 'Solicitante', 'Qtde',
                            'Procedimento', 'Grupo de Procedimento', 'Especialidade', 'Convênio',
                            'Plano', 'Lote', 'Pagamento', 'N. Guia', 'Taxa do Cartão (R$(%))',
                            'Recebido Bruto(R$)', 'Imposto(R$)', 'Recebido Líquido(R$)',
                            'Tipo de Pagamento', 'Forma de Pagamento', 'Nota Fiscal', 'Valor(R$)',
                            'Observação (Faturamento)', 'Observação (Pagamento)'])
        for row in consulta.tbody.find_all('tr'):
            columns = row.find_all('td')
        """   