from datetime import timedelta,date
import datetime
from ingestors import AgendamentoIngestor
from writers import DataWriter




agendamento_ingestor = AgendamentoIngestor(writer=DataWriter,startDate=datetime.date(2022,8,17), endDate=datetime.date(2022,8,17))
agendamento_ingestor.ingest()
