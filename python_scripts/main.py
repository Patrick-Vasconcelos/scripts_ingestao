from datetime import timedelta,date
import datetime
from python_scripts.ingestors import AgendamentoIngestor
from python_scripts.writers import DataWriter




agendamento_ingestor = AgendamentoIngestor(writer=DataWriter,startDate=datetime.date(2022,8,17), endDate=datetime.date(2022,8,17))
agendamento_ingestor.ingest()
