raw_data = pd.read_csv('test_data_multi_houses.csv')

#Divide the raw data into different groups by house_id
grouped_df = raw_data.groupby(raw_data.columns[0])

#Array to store the transformed data
dataX=None
non_time_data=None
house_id_column=None
time_column=None
#Iterate all groups
for key, item in grouped_df:
    #Get the data
    single_house_raw_data = grouped_df.get_group(key)
    #Sliding window transform
    single_house_dataX = create_dataset(single_house_raw_data\
                                        .iloc[:,2].as_matrix(),window_size)
    #Stack the transformed data onto the ready-to-request array
    if dataX is None:
        dataX = single_house_dataX
    else:
        dataX = np.vstack([dataX,single_house_dataX])
    
    #Extract non-time info
    single_house_non_time = non_time_data_extraction(single_house_raw_data)
    #Stack the non-time data
    if non_time_data  is None:
        non_time_data  = single_house_non_time
    else:
        non_time_data  = np.vstack([non_time_data ,single_house_non_time])
        
    house_id = single_house_raw_data.iloc[window_size-1:,0]\
        .values.reshape([-1,1])
    if house_id_column  is None:
        house_id_column  = house_id
    else:
        house_id_column  = np.vstack([house_id_column ,house_id])
    
    time_stamp = single_house_raw_data.iloc[window_size-1:,1]\
        .values.reshape([-1,1])
    if time_column  is None:
        time_column  = time_stamp
    else:
        time_column  = np.vstack([time_column ,time_stamp])
