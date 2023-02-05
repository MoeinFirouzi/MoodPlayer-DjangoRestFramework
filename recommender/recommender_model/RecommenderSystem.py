import random as rd
import pandas as pd
import numpy as np
from time import sleep
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.preprocessing import MinMaxScaler
from recommender.recommender_model.SubModules.Cleaner import music_cleaner_dataframe, sensor_cleaner_dataframe
from recommender.recommender_model.SubModules.CustomDrivingEvaluation import Evaluator


class MemoryBased():
    
    def first_recommend(self, user_id, session_id):
        user_id = int(user_id)
        session_id = int(session_id)

        user_df = pd.read_csv('recommender/recommender_model/DataFrames/user_df.csv', index_col=0)
        neutral_state = user_df['score'].loc[user_id]
        current_state = neutral_state

        target_state = neutral_state + \
            (neutral_state - current_state) + rd.uniform(-0.1, 0.1)

        rate_df = pd.read_csv('recommender/recommender_model/DataFrames/rate_df.csv', index_col=0)
        recommended_musics = (rate_df.loc[user_id][(
            target_state - rate_df.loc[user_id]).abs().argsort().values])
        recommended_music = recommended_musics.head(1)

        Log_MemoryBased_Recommend = pd.read_csv(
            "recommender/recommender_model/DataFrames/Logs/Log_MemoryBased_Recommend.csv", index_col=0)
        input_log_df = pd.DataFrame(np.array([[session_id, user_id, recommended_music.index[0], recommended_music.values[0],
                                    current_state, neutral_state, target_state]]), columns=Log_MemoryBased_Recommend.columns)
        Log_MemoryBased_Recommend = pd.concat(
            (Log_MemoryBased_Recommend, input_log_df))
        Log_MemoryBased_Recommend.to_csv(
            "recommender/recommender_model/DataFrames/Logs/Log_MemoryBased_Recommend.csv")

        return int(recommended_music.index[0])

    def recommend(self, user_id, session_id):
        try:
            user_id = int(user_id)
            session_id = int(session_id)

            log_df = pd.read_csv(
                "recommender/recommender_model/DataFrames/Logs/Log_Updater_Score.csv", index_col=0)
            print(log_df)
            current_state = log_df.groupby('session_id').get_group(
                session_id).tail(1)['new_value'].values[0]

            user_df = pd.read_csv(
                'recommender/recommender_model/DataFrames/user_df.csv', index_col=0)
            neutral_state = user_df['score'].loc[user_id]

            target_state = neutral_state + (neutral_state - current_state)

            rate_df = pd.read_csv(
                'recommender/recommender_model/DataFrames/rate_df.csv', index_col=0)
            recommended_musics = (rate_df.loc[user_id][(
                target_state - rate_df.loc[user_id]).abs().argsort().values])
            recommended_music = recommended_musics.head(1)

            Log_MemoryBased_Recommend = pd.read_csv(
                "recommender/recommender_model/DataFrames/Logs/Log_MemoryBased_Recommend.csv", index_col=0)
            input_log_df = pd.DataFrame(np.array([[session_id, user_id, recommended_music.index[0], recommended_music.values[0],
                                        current_state, neutral_state, target_state]]), columns=Log_MemoryBased_Recommend.columns)
            Log_MemoryBased_Recommend = pd.concat(
                (Log_MemoryBased_Recommend, input_log_df))
            Log_MemoryBased_Recommend.to_csv(
                "recommender/recommender_model/DataFrames/Logs/Log_MemoryBased_Recommend.csv")

            return int(recommended_music.index[0])
        except Exception as e:
            print(e)


class CollaborativeFiltering():
    def recommend(user_id, music_id, session_id):
        rate_df = pd.read_csv("./DataFrames/rate_df.csv").set_index('id')
        similarity_users = 1 - euclidean_distances(rate_df.values)
        similarity_users = pd.DataFrame(
            similarity_users, columns=rate_df.index, index=rate_df.index)
        similar_user = similarity_users.iloc[user_id].sort_values(
            ascending=False).drop(index=user_id).head(1)

        similar_user_id = similar_user.index[0]
        similar_user_similarity = similar_user.values[0]
        similar_user_rate = rate_df.iloc[similar_user_id, music_id]

        Log_CollaborativeFiltering_Recommend = pd.read_csv(
            "./DataFrames/Logs/Log_CollaborativeFiltering_Recommend.csv", index_col=0)
        input_log_df = pd.DataFrame(np.array([[session_id, user_id, music_id, similar_user_id,
                                    similar_user_similarity, similar_user_rate]]),
                                    columns=Log_CollaborativeFiltering_Recommend.columns)
        Log_CollaborativeFiltering_Recommend = pd.concat(
            (Log_CollaborativeFiltering_Recommend, input_log_df))
        Log_CollaborativeFiltering_Recommend.to_csv(
            "./DataFrames/Logs/Log_CollaborativeFiltering_Recommend.csv")

        return similar_user_rate


class Updater():

    def fit(self, music_dataframe, sensor_dataframe):
        music_dataframe = music_dataframe.reset_index()
        sensor_dataframe = sensor_dataframe.reset_index()

        scores_df = self.get_scores(music_dataframe, sensor_dataframe)

        for i in scores_df.iloc:
            self.update_rate_df(
                i['session_id'], i['user_id'], i['music_id'], i['score'])
            self.update_neutral_state(
                i['session_id'], i['user_id'], i['music_id'], i['score'])

    def update_neutral_state(self, session_id, user_id, music_id, value):
        user_id = int(user_id)
        music_id = str(int(music_id))

        user_df = pd.read_csv(
            'recommender/recommender_model/DataFrames/user_df.csv', index_col=0)
        previous_value = user_df['score'].loc[user_id]

        updated_value = (previous_value + value) / 2
        user_df['score'].loc[user_id] = updated_value
        user_df.to_csv('recommender/recommender_model/DataFrames/user_df.csv')

        Log_Updater_Score = pd.read_csv(
            "recommender/recommender_model/DataFrames/Logs/Log_Updater_Score.csv", index_col=0)
        input_log_df = pd.DataFrame(np.array(
            [[session_id, user_id, music_id, previous_value, value, updated_value]]),
                                    columns=Log_Updater_Score.columns)
        Log_Updater_Score = pd.concat((Log_Updater_Score, input_log_df))
        Log_Updater_Score.to_csv(
            "recommender/recommender_model/DataFrames/Logs/Log_Updater_Score.csv")

    def update_rate_df(self, session_id, user_id, music_id, value):
        user_id = int(user_id)
        music_id = str(int(music_id))

        rate_df = pd.read_csv(
            'recommender/recommender_model/DataFrames/rate_df.csv', index_col=0)
        previous_value = rate_df[music_id].loc[user_id]
        updated_value = (previous_value + value) / 2
        rate_df[music_id].loc[user_id] = updated_value
        rate_df.to_csv('recommender/recommender_model/DataFrames/rate_df.csv')

        Log_Updater_Update = pd.read_csv(
            "recommender/recommender_model/DataFrames/Logs/Log_Updater_Update.csv", index_col=0)
        input_log_df = pd.DataFrame(np.array(
            [[session_id, user_id, music_id, previous_value, value, updated_value]]), columns=Log_Updater_Update.columns)
        Log_Updater_Update = pd.concat((Log_Updater_Update, input_log_df))
        Log_Updater_Update.to_csv(
            "recommender/recommender_model/DataFrames/Logs/Log_Updater_Update.csv")

        return rate_df

    def get_scores(self, music_dataframe, sensor_dataframe):

        cleaned_music_df = music_cleaner_dataframe(music_dataframe)

        cleaned_sensor_df = sensor_cleaner_dataframe(sensor_dataframe)

        cleaned_music_df = cleaned_music_df.reset_index()
        cleaned_sensor_df = cleaned_sensor_df.reset_index()

        # remove lost/unsent data rows from both frames

        for i in cleaned_sensor_df['date_time'].values:
            if i not in cleaned_music_df['date_time'].values:
                cleaned_sensor_df = cleaned_sensor_df[cleaned_sensor_df.date_time != i]

        for i in cleaned_music_df['date_time'].values:
            if i not in cleaned_sensor_df['date_time'].values:
                cleaned_music_df = cleaned_music_df[cleaned_music_df.date_time != i]

        group = cleaned_music_df.groupby('music_id')
        musics = list(group.groups.keys())

        df_list_music = []
        df_list_sensor = []
        driving_scores = []

        for i in musics:
            try:
                music_chunk = cleaned_music_df.iloc[list(
                    group.groups[i])].set_index('date_time')
                sensor_chunk = cleaned_sensor_df.iloc[list(
                    group.groups[i])].set_index('date_time')

                if (music_chunk.shape[0] > 120 and sensor_chunk.shape[0] > 120):
                    df_list_music.append(music_chunk)
                    df_list_sensor.append(sensor_chunk)
                    driving_score = Evaluator.evaluate(sensor_chunk)
                    driving_scores.append(
                        (i, cleaned_music_df.loc[0].user_id, cleaned_music_df.loc[0].session_id, driving_score))
            except:
                print('error occured at: ' + str(i))
        df_score = pd.DataFrame(driving_scores, columns=[
                                'music_id', 'user_id', 'session_id', 'score'])
        return df_score
