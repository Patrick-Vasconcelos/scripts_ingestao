
import pandas as pd
from datetime import timedelta,date
import datetime
from ingestors import AgendamentoIngestor
from crawlers import CrawlerConsulta
from writers import DataWriter
from crawlers import Crawler


# agendamento_ingestor = AgendamentoIngestor(writer=DataWriter,startDate=date.today() - timedelta(days=1), endDate=date.today() - timedelta(days=1))
# agendamento_ingestor.ingest()

# agendamento_ingestor = AgendamentoIngestor(writer=DataWriter,startDate=date.today() - timedelta(days=1), endDate=date.today())
# agendamento_ingestor.ingest()


crawler = CrawlerConsulta()
Date = datetime.date(2022, 8, 30)
# crawler.scrape(startDate=date.today() - timedelta(days=1),endDate=date.today() - timedelta(days=1))
crawler.scrape(startDate=Date,endDate=Date)
