from datetime import timedelta,date
import datetime
from ingestors import AgendamentoIngestor
from writers import DataWriter




agendamento_ingestor = AgendamentoIngestor(writer=DataWriter,startDate=date.today() - timedelta(days=1), endDate=date.today() - timedelta(days=1))
agendamento_ingestor.ingest()
