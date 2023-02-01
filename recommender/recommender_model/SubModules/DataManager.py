import requests
import json
from zipfile import ZipFile
import os
import pandas as pd
import numpy as np
from Cleaner import music_cleaner_dataframe, sensor_cleaner_dataframe


def get_token(username='arvin', password='carrotparrot0'):
    #get token
    url = "http://31.7.74.196:1337/api/account/login/username/"
    payload = json.dumps({
    "username": str(username),
    "password": str(password)
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    token = 'Token ' + json.loads(response.text)['token']
    return token


def save_data(music_data, sensor_data):
    music_data.to_csv("music_data.csv")
    sensor_data.to_csv("sensor_data.csv")


def download_and_extract(first_index,last_index):
    last_index = last_index + 1
    token = get_token()

    for i in range(first_index,last_index):
        session_id = str(i)
        path = "./downloaded/3. fine/" + session_id + ".zip"

        if(os.path.exists(path)):
            print('skipped session: ' + session_id)
        else:
            url = "http://31.7.74.196:1337/api/state/session/" + session_id + "/get_data"

            payload = ""
            headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            open(path, "wb").write(response.content)

        if(os.path.exists(path)):
            if((os.stat(path).st_size) < 10240):
                os.remove(path)
                print("session " + session_id + " removed!")
            else:
                with ZipFile(path, 'r') as zObject:
                    zObject.extractall('./downloaded/3. fine/')


def concat(first_index, last_index, clean_flag, save_flag):
    music_data = pd.read_csv("./downloaded/3. fine/tmp/music_" + str(first_index) +".csv").set_index('id')
    sensor_data = pd.read_csv("./downloaded/3. fine/tmp/sensor_" + str(first_index) +".csv").set_index('id')

    for i in range(first_index + 1, last_index):
        session_id = str(i)

        if(os.path.exists("./downloaded/3. fine/tmp/sensor_" + session_id + ".csv")):
            sensor_appendable = pd.read_csv("./downloaded/3. fine/tmp/sensor_" + session_id + ".csv")
            
            if(clean_flag):
                sensor_appendable = sensor_cleaner_dataframe(sensor_appendable)
            
            sensor_appendable = sensor_appendable.reset_index().drop(columns=['index'])
            sensor_data = pd.concat([sensor_data, sensor_appendable])
            
        if(os.path.exists("./downloaded/3. fine/tmp/music_" + session_id + ".csv")):
            music_appendable = pd.read_csv("./downloaded/3. fine/tmp/music_" + session_id + ".csv")
            
            if(clean_flag):
                music_appendable = music_cleaner_dataframe(music_appendable)
            
            music_appendable = music_appendable.reset_index().drop(columns=['index'])
            music_data = pd.concat([music_data, music_appendable])
    
    if(save_flag):
        save_data(music_data, sensor_data)

    return (music_data, sensor_data)


