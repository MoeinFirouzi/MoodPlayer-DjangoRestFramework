import pandas as pd
import numpy as np

class Adder():
    def add_user(self, id, username, email):
        try:
            user_df = pd.read_csv('recommender/recommender_model/DataFrames/user_df.csv')

            user_df = pd.read_csv('recommender/recommender_model/DataFrames/user_df.csv')
            input_df = pd.DataFrame(np.array([[id,email, username, 0.5]]), columns=user_df.columns)
            user_df = pd.concat((user_df, input_df))
            user_df = user_df.set_index('id')
            user_df.to_csv('recommender/recommender_model/DataFrames/user_df.csv')

            
            #update rate_df by adding new user row to it       
            music_df = pd.read_csv('recommender/recommender_model/DataFrames/music_df.csv').sort_values(by='id')

            rate_df = pd.read_csv('recommender/recommender_model/DataFrames/rate_df.csv', index_col=0)

            row = np.zeros((1,rate_df.shape[1]))
            for i in range(row.shape[1]-1):
                row[0,i] = music_df['rate'].values[i]
            df_row = pd.DataFrame(row, columns=rate_df.columns, index=[id])

            rate_df = pd.concat((rate_df, df_row))
            rate_df = rate_df
            rate_df.to_csv('recommender/recommender_model/DataFrames/rate_df.csv')
        except:
            pass