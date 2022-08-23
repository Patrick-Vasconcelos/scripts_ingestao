from datetime import date,timedelta
import json
import os
import pandas as pd


class DataWriter:
    def __init__(self, api: str) -> None:
        self.filename = f"{api}/{date.today() - timedelta(days=1)}.json"
    
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)
    
    def write(self, data) -> None:
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, list):
            for element in data:
                self.write(element)
        else:
            pass
    
    def write_excel(self, data: dict) -> None:
        if isinstance(data, dict):
            df = pd.json_normalize(data=data)
            df.to_excel(f'{self.filename}.xlsx', index=False)
        
        elif isinstance(data, list):
            df = pd.DataFrame()
            for element in data:
                df_ = pd.json_normalize(data=element)
                df = pd.concat([df_, df], ignore_index=True)
            df.to_excel(f'{self.filename}.xlsx', index=False)
        
        else:
            pass