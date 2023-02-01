import pandas as pd
import numpy as np
import datetime

###########################################################
###########################################################
###########################################################

def music_imputer(start, end, dist):
    
    dist = int(dist)
    
    return_list = []

    # generate template rows
    for i in range(dist):
        return_list.append(start.copy()) 

    # set splitting point
    split_point = int(np.ceil(dist/2))
    
    # find position difference
    pos_dif = (end['position'] - start['position']) / dist

    # main impute iteration
    for i in range(0,dist):

        # set numeric values (incrementals) 
        # date_time
        return_list[i]['date_time'] = start['date_time'] + (i * pd.Timedelta(500, 'milli'))
        # position
        pos = (start['position'] + (i * pos_dif))
        res = str(pos.hour) + ":" + str(pos.minute) + ":" + str(pos.second) + "." + str(pos.microsecond)
        return_list[i]['position'] = res

        # set non-numeric values
        if i > split_point:
            return_list[i]['muted'] = end['muted']
            return_list[i]['state'] = end['state']
            return_list[i]['volume'] = end['volume']
            return_list[i]['playlist_count'] = end['playlist_count']
            return_list[i]['repeat_mode'] = end['repeat_mode']
            return_list[i]['shuffle_mode'] = end['shuffle_mode']
            return_list[i]['music_id'] = end['music_id']
            return_list[i]['album'] = end['album']
            return_list[i]['duration'] = end['duration']
            return_list[i]['artist'] = end['artist']
            return_list[i]['genre'] = end['genre']
            return_list[i]['energy'] = end['energy']
            return_list[i]['valence'] = end['valence']
            return_list[i]['title'] = end['title']
            return_list[i]['year'] = end['year']

    return return_list


def sensor_imputer(start, end, dist, df):
    dist = int(dist)
    return_list = []

    # if(start['location_latitude'] == 0 and start['location_longitude'] == 0):

    #     first_correct_lat = df[df['location_latitude'] > 0]
        
    #     if(first_correct_lat.shape[0] > 0):
    #         start['location_latitude'] = first_correct_lat['location_latitude'].iloc[0]
        
    #     first_correct_lon = df[df['location_longitude'] > 0]
        
    #     if(first_correct_lon.shape[0] > 0):
    #         start['location_longitude'] = first_correct_lon['location_longitude'].iloc[0]

    #generate template rows
    for i in range(dist):
        return_list.append(start.copy()) 

    #set splitting point
    split_point = int(np.ceil(dist/2))
    
    # find location_update_time difference
    pos_dif = (end['location_update_time'] - start['location_update_time']) / dist

    # find differences of float values
    # select float columns
    columns = list(df.columns)
    for excluded_column in ['date_time', 'location_update_time', 'location_is_from_mock_provider', 'location_altitude_reference_system', 'orientation_is_identity']:
        columns.remove(excluded_column)

    # create difference dictionary for float columns 
    dict_difference = {}
    for column in columns:
        dict_difference[column] = (end[column] - start[column]) / dist

    for i in range(0,dist):

        # set numeric values (incrementals) 
        # date_time
        return_list[i]['date_time'] = start['date_time'] + (i * pd.Timedelta(500, 'milli'))
        
        # location_update_time
        pos = (start['location_update_time'] + (i * pos_dif))
        res = str(pos.hour) + ":" + str(pos.minute) + ":" + str(pos.second) + "." + str(pos.microsecond)
        return_list[i]['location_update_time'] = res
        
        # float values
        for column in columns:
            return_list[i][column] = start[column] + (i * dict_difference[column])


        # set non-numeric values
        if i > split_point:
            return_list[i]['location_is_from_mock_provider'] = end['location_is_from_mock_provider']
            return_list[i]['location_altitude_reference_system'] = end['location_altitude_reference_system']
            return_list[i]['orientation_is_identity'] = end['orientation_is_identity']
    
    return return_list

###########################################################
###########################################################
###########################################################

def music_cleaner_dataframe(music_df):
    pd.options.mode.chained_assignment = None 
    df = music_df
    
    # sort values by id and remove unnecessary columns
    df = df.sort_values(by=['id'])

    #fix timestamps
    for i in range(df.shape[0]):
        if(str(df['position'][i]) == "_"):
            df['position'][i] = "00:00"
            df['state'][i] = "Stopped"
            df['volume'][i] = 50

        df['position'][i] = str(df['position'][i]).split(".")[0]

    df['position'] = pd.to_datetime(df['position'],format='%M:%S')
    df['date_time'] = pd.to_datetime(df['date_time'],format='%Y-%m-%d %H:%M:%S:%f')
    df = df.convert_dtypes()

    # interpolation for lost values using music_imputer
    fixed = []

    start_row = df.iloc[0]

    for k in range(1,df.shape[0]):
        end_row = df.iloc[k]
        distance = pd.Timedelta(end_row['date_time'] - start_row['date_time']) / pd.Timedelta(500, 'milli')
        if(distance > 0):
            fixed.extend(music_imputer(start_row, end_row, distance))
            
        #fixed.append(end_row)

        start_row = df.iloc[k]

    # save fixed values as new dataframe
    fixed_df = pd.DataFrame(fixed, columns= df.columns)
    fixed_df = fixed_df.drop_duplicates(subset=['date_time'], keep='last')
    return fixed_df


###########################################################
###########################################################
###########################################################

def sensor_cleaner_dataframe(sensor_df):
    pd.options.mode.chained_assignment = None
    df = sensor_df

    # sort values by id and remove unnecessary columns
    df = df.sort_values(by=['id'])
    df = df.drop(columns=['id'])
    
    #fix timestamps
    for i in range(df.shape[0]):
        df['location_update_time'][i] = str(df['location_update_time'][i]).split("+")[0].split("T")[1].split(".")[0]

    df['location_update_time'] = pd.to_datetime(df['location_update_time'],format='%H:%M:%S')
    df['date_time'] = pd.to_datetime(df['date_time'],format='%Y-%m-%d %H:%M:%S:%f')
    df = df.convert_dtypes()

    # interpolation for lost values using music_imputer
    fixed = []

    start_row = df.iloc[0]

    for k in range(1,df.shape[0]):
        end_row = df.iloc[k]
        distance = pd.Timedelta(end_row['date_time'] - start_row['date_time']) / pd.Timedelta(500, 'milli')
        
        if(distance > 0):
            fixed.extend(sensor_imputer(start_row, end_row, distance,df))
            
        #fixed.append(end_row)

        start_row = df.iloc[k]

    # save fixed values as new dataframe
    fixed_df = pd.DataFrame(fixed, columns= df.columns)
    fixed_df = fixed_df.drop_duplicates(subset=['date_time'], keep='last')
    return fixed_df
