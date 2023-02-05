import pandas as pd
import numpy as np

class Adder():

    def add_music(self, id, artist_id, album_id, genre, energy, valence, year):
        music_df = pd.read_csv('DataFrames/music_df.csv').sort_values(by='id')

        record = { "id" : id, "artist_id": artist_id, "album_id" : album_id, "genre" : genre, "energy" : energy, "valence": valence, "year" : year, "rate" : 0 }

        record['rate'] = self.energy_valence_to_rate(record['energy'] ,record['valence'])

        music_df = music_df.append(record,ignore_index=True)
        
        music_df = music_df.set_index('id')
 
        music_df.to_csv('DataFrames/music_df.csv')

        similarity_df = self.create_similarity_matrix(music_df)

        #update rate_df by adding new song column to it
        rate_df = pd.read_csv('DataFrames/rate_df.csv').set_index('id')

        column = np.zeros((rate_df.shape[0],1))
        for i in range(column.shape[0]):
            column[i,0] = record['rate']
        df_column = pd.DataFrame(column, columns=[record['id']], index= rate_df.index)
        rate_df = rate_df.join(df_column)
        rate_df.to_csv('DataFrames/rate_df.csv')

        return (music_df,similarity_df,rate_df)

    def add_user(self, id, username, email):

        record = {'id': id, 'username' : username, 'email' : email}

        user_df = pd.read_csv('DataFrames/user_df.csv')
        user_df = user_df.append(record,ignore_index=True)
        
        music_df = pd.read_csv('DataFrames/music_df.csv').sort_values(by='id')

        #update rate_df by adding new user row to it
        rate_df = pd.read_csv('DataFrames/rate_df.csv').set_index('id')

        row = np.zeros((1,rate_df.shape[1]))
        for i in range(row.shape[1]):
            row[0,i] = music_df['rate'].iloc[i]
        df_row = pd.DataFrame(row, columns=rate_df.columns, index=[27])

        rate_df = rate_df.append(df_row)
        rate_df.to_csv('DataFrames/rate_df.csv')

        user_df = user_df.set_index('id').sort_values(by='id')
        user_df.to_csv('DataFrames/user_df.csv')