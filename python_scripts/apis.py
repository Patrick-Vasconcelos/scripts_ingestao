from datetime import datetime
import requests
from abc import abstractmethod, ABC
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ClinicWebApi(ABC):
    """
    Classe de consumo api clinic web 

    Métodos:
        _get_endpoint -> metodo abstrato para classes herdeiras
        get_data -> metodo para fazer requisicoes na API do clinicWeb
    Returns:
        _get_endpoint (None) -> None
        get_data (json) -> retorna arquivo json com as requisicoes
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_endpoint = "https://prod-apicw.vitta.me"
    

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str: 
        pass

    def get_data(self,token : str,  **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        headers = {
        "Content-Type": "application/json",
        "Authorization": token
        }
        response = requests.request("GET", endpoint, headers=headers)
        return response.json()


class GetToken(ClinicWebApi):
    """
    Classe para Obter Token de acesso, que herda do ClinicWebApi

    Métodos:
        _writer_token -> escrever um arquivo txt, com o token de acesso
        get_token -> Faz uma requisição a API do clinicweb, para receber token de acesso
        _get_endpoint -> metodo abstrato herdado de ClinicWebApi para obter endpoint
    
    Returns:
        _writer_token (None) -> None
        get_token (str) -> token de acesso 
        _get_endpoint (str) -> endpoint
    """

    def _write_token(self, token : str) -> None:
        with open('token.txt', 'w') as file:
            file.write('JWT '+token)
    
    def get_token(self,username : str, password: str, **kwargs) -> str:
        headers = {
        "Content-Type": "application/json"
        }  

        user_data = {
        "username" : username,
        "password" : password
        }

        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting access token from endpoint: {endpoint}")
        response = requests.request("POST", endpoint, json=user_data, headers=headers)
        logger.info(f"Request status: {response.status_code}")
        response_data = response.json()
        token = response_data['token']

        self._write_token(token=token)
        
        return 'JWT '+token

    def _get_endpoint(self) -> str:
        return f"{self.base_endpoint}/auth/login"

class GetPaciente(ClinicWebApi):
    """
    Classe para buscar paciente, a partir do idPaciente, nome, cpf, ou data nascimento

    Métodos:
        _get_endpoint -> metodo abstrato herdado de ClinicWebApi para obter endpoint
    Returns:
        _get_endpoint (str) -> endpoint
    """

    def _get_endpoint(self, query: str, codEmpresa : int = 10177) -> str:
        return f"{self.base_endpoint}/pacientes/?codEmpresa={codEmpresa}&query={query}"
    

class GetProfissional(ClinicWebApi):
    """
    Classe para buscar profissional, a partir do nome do profissional

    Métodos:
        _get_endpoint -> metodo abstrato herdado de clinicwebapi para obter endpoint
    Returns:
        _get_endpoint (str) -> endpoint 
    """

    def _get_endpoint(self, term : str = None, codEmpresa: str = 10177) -> str:
        if term == None:
            return f"{self.base_endpoint}/profissionais/?codEmpresa={codEmpresa}"
        else:
            return f"{self.base_endpoint}/profissionais/?term={term}&codEmpresa={codEmpresa}"

class GetAgendamento(ClinicWebApi):
    """
    Classe para buscar lista de agendamentos, a partir de uma data de inicio, data final, pagina, lista de profissionais

    Métodos:
        _get_endpoint -> metodo abstrato herdade de clinicwebapi para obert endpoint
        _get_pages -> metodo para buscar quantidade de paginas presentes na consulta
        get_data -> sobrescrita do metodo get_data da classe mae
    Returns:
        _get_endpoint (str) -> endpoint
        _get_pages (int) (int) (str) -> pagina atual, quantidade de paginas, dados da consulta

    """
    
    def _get_endpoint(self, startDate: datetime.date = None , endDate: datetime.date = None, codEmpresa: str = 10177, page:str = 1, codProfissionais: str = None) -> str:
        if endDate == None  and codProfissionais == None:
            return f"{self.base_endpoint}/agendamentos?codEmpresa={codEmpresa}&startDate={startDate}&$page={page}"
        elif codProfissionais == None:
            return f"{self.base_endpoint}/agendamentos?codEmpresa={codEmpresa}&startDate={startDate}&endDate={endDate}&$page={page}"
        else:
            return f"{self.base_endpoint}/agendamentos?codEmpresa={codEmpresa}&startDate={startDate}&endDate={endDate}&$page={page}&codProfissionais={codProfissionais}"


    def _get_pages(self,response : dict, **kwargs):
        data = response
        return data['page'], data['pages'], data['data']


    def get_data(self, token: str, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        
        headers = {
        "Content-Type": "application/json",
        "Authorization": token
        }

        response = requests.request("GET", endpoint, headers=headers)
        response = response.json()
        page, pages, data = self._get_pages(response)
        return page, pages, data

