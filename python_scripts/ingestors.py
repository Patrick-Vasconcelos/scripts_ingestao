from python_scripts.credentials import username, password
from abc import abstractmethod,ABC
from datetime import datetime
from python_scripts.apis import GetAgendamento, GetToken

from python_scripts.writers import DataWriter


class DataIngestor(ABC):
    def __init__(self, writer, **kwargs) -> None:
        self.writer = writer
        pass

    @abstractmethod
    def ingest(self) -> None:
        pass

        
class AgendamentoIngestor(DataIngestor):
    def __init__(self, writer: DataWriter, startDate: datetime.date = None , endDate: datetime.date = None, codEmpresa: str = 10177, page:str = 1, codProfissionais: str = None, **kwargs) -> None:
        super().__init__(writer, **kwargs)
        self.startDate = startDate
        self.endDate = endDate
        self.codEmpresa = codEmpresa
        self.page = page
        self.codProfissionais = codProfissionais
        self.writer = writer
    

    def ingest(self) -> None:
        token = GetToken().get_token(username=username, password=password)

        while True:
            self.page,pages,api = GetAgendamento().get_data(token=token, startDate=self.startDate, endDate=self.endDate, page=self.page, codProfissionais=self.codProfissionais)
            self.writer(api='Agendamentos').write(api)

            if self.page >= pages:
                break
            self.page += 1