import os
import csv
from zipfile import ZipFile


class CSVConvertor:
    """
    Convert MusicState or SensorState tables' rows by given session id to CSV tables.
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.path = f'/tmp/{file_name}.csv'

    def convert(self, query_set):
        try:
            with open(self.path, 'w') as csv_file:
                if query_set:
                    self.writer = csv.writer(csv_file)
                    header = list(query_set[0].__dict__.keys())
                    header.pop(0)
                    self.writer.writerow(header)

                    for record in query_set:
                        row = list(record.__dict__.values())
                        row.pop(0)
                        self.writer.writerow(row)
        except:
            pass


class ZipConvertor:
    """
    Zip CSV reports by given session id.
    """

    def __init__(self, session_id):
        self.session_id = session_id
        self.path = f'/tmp/{self.session_id}.zip'
        self.music_csv_path = f'/tmp/music_{self.session_id}.csv'
        self.sensor_csv_path = f'/tmp/sensor_{self.session_id}.csv'

    def convert(self):
        try:
            zip_obj = ZipFile(self.path, 'w')
            
            if os.path.exists(self.sensor_csv_path):
                zip_obj.write(f'/tmp/sensor_{self.session_id}.csv')
              
            if os.path.exists(self.music_csv_path):    
                zip_obj.write(f'/tmp/music_{self.session_id}.csv')

            zip_obj.close()
        except:
            pass


class FileCleaner:
    """
    Delete ZIP & CSV files in '/tmp' directory by session id.
    """

    def __init__(self, session_id):
        self.session_id = session_id
        self.music_csv_path = f'/tmp/music_{self.session_id}.csv'
        self.sensor_csv_path = f'/tmp/sensor_{self.session_id}.csv'
        self.zip_path = f'/tmp/{self.session_id}.zip'

    def clean(self):
        try:
            if os.path.exists(self.zip_path):
                os.remove(self.zip_path)
                
            if os.path.exists(self.sensor_csv_path):    
                os.remove(self.sensor_csv_path)
                
            if os.path.exists(self.music_csv_path):
                os.remove(self.music_csv_path)
        except:
            pass
