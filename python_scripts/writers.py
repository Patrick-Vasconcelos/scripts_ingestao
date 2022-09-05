import datetime
from datetime import date,timedelta
import json
import os
from tempfile import NamedTemporaryFile
import pandas as pd
from os import getenv
from dotenv import load_dotenv
import boto3
from botocore import exceptions
from botocore.exceptions import ClientError

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:

    def __init__(self, api: str) -> None:
        self.api = api
        self.filename = f"{api}/{date.today() - timedelta(days=1)}.json"
    
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)
    
    def _write_to_file(self, data):
        if isinstance(data, dict):
            print("DEBUG: entrou como dict")
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, list):
            print("DEBUG: entrou como lista")
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)


    def write(self, data):
        self._write_to_file(data=data)
       
    
    def write_excel(self, data: dict) -> None:
        if isinstance(data, dict):
            df = pd.json_normalize(data=data)
            df.to_excel(f'agendamentos.xlsx', index=False)
        
        elif isinstance(data, list):
            df = pd.DataFrame()
            for element in data:
                df_ = pd.json_normalize(data=element)
                df = pd.concat([df_, df], ignore_index=True)
            df.to_excel(f'agendamentos.xlsx', index=False)
        
        else:
            pass
    
class S3Writer(DataWriter):
    def __init__(self, api:str) -> None:
        super().__init__(api)
        self.env = load_dotenv(r'C:\Users\Qorpo\.env')
        self.tempfile = NamedTemporaryFile(delete=False)
        
        self.s3 =  boto3.client(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY')
        )
    def _write_row(self, row:str) -> None:
        with open(self.tempfile.name, "a") as f:
            f.write(row)

    def write(self, data):
        self.count = 1
        self.key = f"clinic_web/{self.api}/extracted_at={datetime.datetime.now().date()}/{datetime.datetime.now()}/{self.api}-{self.count}.json"
        self._write_to_file(data=data)
        self._write_file_to_s3()

    def _write_to_file(self, data):
        if isinstance(data, dict):
            print("DEBUG: entrou como dict")
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, list):
            print("DEBUG: entrou como lista")
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)

    def _write_file_to_s3(self):
        self.s3.put_object(
            Body=self.tempfile,
            Bucket="qorpo-data-lake-raw",
            Key=self.key
        )
