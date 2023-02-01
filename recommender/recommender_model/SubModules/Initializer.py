import json
import requests
import pandas as pd
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class Initializer():

    token = ""

    def __init__(self):
        self.get_token()

    def get_token(self, username='arvin', password='carrotparrot0'):
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
        self.token = 'Token ' + json.loads(response.text)['token']
        return self.token

    def create_similarity_matrix(self, music_df):
        #create similarity matrix for musics
        similarity = euclidean_distances(pd.get_dummies(music_df))

        scaler = MinMaxScaler().fit(similarity)
        similarity = scaler.transform(similarity)
        similarity = 1 - similarity

        similarity_df = pd.DataFrame(similarity, columns=music_df.index, index = music_df.index)
        similarity_df.to_csv('./DataFrames/similarity_df.csv')
        return similarity_df

    def energy_valence_to_rate(self,energy,valence):
        #change 2 dimensional categorical scores to 1 dimentinal numerical score
        dict_cat_to_num_energy = {'Too Negative': 0, 'Negative' : 0.25, 'Neutral' : 0.5, 'Positive' : 0.75, 'Too Positive' : 1}
        dict_cat_to_num_valence = {'Too Negative': 1, 'Negative' : 0.5, 'Neutral' : 0, 'Positive' : 0.5, 'Too Positive' : 1}
        return (dict_cat_to_num_energy[energy] + dict_cat_to_num_valence[valence]) / 2

    def create_music_list(self):

        #get music list
        url = "http://31.7.74.196:1337/api/player/music/"
        payload = ""
        headers = {
        'Authorization': self.token,
        'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        music_list = json.loads(response.text)['data']

        #generate music dataframe
        music_df = pd.DataFrame(music_list)
        music_df['album_id'] = music_df['album_id'].astype(str)
        music_df['artist_id'] = music_df['artist_id'].astype(str)
        music_df = music_df.drop(columns=['artist_absolute_url','album_absolute_url','absolute_url','address','song_image', 'album','album_url','artist','artist_url','title'])
        music_df = music_df.set_index('id').sort_values(by='id')


        rate_list = []
        for index in music_df.iterrows():
            row = music_df.loc[index[0]]
            
            rate_list.append(self.energy_valence_to_rate(row['energy'] ,row['valence']))
        rate_series = pd.Series(rate_list, name='rate', index=music_df.index)

        music_df = music_df.join(rate_series, how='right')

        music_df.to_csv('./DataFrames/music_df.csv')

        similarity_df = self.create_similarity_matrix(music_df)
        return (music_df,similarity_df)

    def create_user_list(self):
        #get user list
        url = "http://31.7.74.196:1337/api/account/users/"
        payload = ""
        headers = {
        'Authorization': self.token,
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        user_list = json.loads(response.text)

        for i in user_list:
            i['score'] = 0
        #generate user df
        user_df = pd.DataFrame(user_list)
        user_df = user_df.convert_dtypes()
        user_df = user_df.set_index('id').sort_values(by='id')

        user_df.to_csv('./DataFrames/user_df.csv')
        return user_df


    def create_user_music_matrix(self):
        # read music list
        music_df = pd.read_csv('./DataFrames/music_df.csv')
        user_df = pd.read_csv('./DataFrames/user_df.csv')

        # generate initial rating matrix (cold-start solution)
        music_id_list = music_df['id']
        user_id_list = user_df['id']

        rate_matrix_initial = np.zeros((len(user_id_list), len(music_id_list)))

        for i in range(rate_matrix_initial.shape[1]):
            rate_matrix_initial[:,i] = music_df.values[i,-1]

        rate_df = pd.DataFrame(rate_matrix_initial, columns=music_id_list, index = user_id_list)
        rate_df.to_csv('./DataFrames/rate_df.csv')
        return rate_df


    def create_logs(self):
        Log_MemoryBased_Recommend = pd.DataFrame([], columns=['session_id', 'user_id', 'recommended_music_id', 'recommended_music_score', 'current_state', 'neutral_state', 'target_state'])
        Log_MemoryBased_Recommend.to_csv("./DataFrames/Logs/Log_MemoryBased_Recommend.csv")
        
        Log_CollaborativeFiltering_Recommend = pd.DataFrame([], columns=['session_id', 'user_id', 'music_id', 'similar_user_id', 'similar_user_similarity', 'similar_user_rate'])
        Log_CollaborativeFiltering_Recommend.to_csv("./DataFrames/Logs/Log_CollaborativeFiltering_Recommend.csv")
        
        Log_Updater_Update = pd.DataFrame([], columns=['session_id', 'user_id', 'music_id', 'previous_value', 'new_value', 'updated_value'])
        Log_Updater_Update.to_csv("./DataFrames/Logs/Log_Updater_Update.csv")

        Log_Updater_Score = pd.DataFrame([], columns=['session_id', 'user_id', 'music_id', 'previous_value', 'new_value', 'updated_value'])
        Log_Updater_Score.to_csv("./DataFrames/Logs/Log_Updater_Score.csv")




    def initialize(self):
        self.create_music_list()
        self.create_user_list()
        self.create_user_music_matrix()
        self.create_logs()