import pandas as pd
import os
import re
#from datetime import datetime

path = "C:\\Users\\python_account\\Documents\\project_data"

full_names = []
file_times = []

for filename in os.listdir(path):
    full_name = os.path.join(path,filename)
    if filename.endswith(".csv") and "picturedata" in filename and os.path.isfile(full_name):
        ts_list = re.findall(r'\d+',filename)
        ts = ts_list[0] + "." + ts_list[1]
        file_time = float(ts)
        full_names.append(full_name)
        file_times.append(file_time)

current_file = full_names[file_times.index(max(file_times))]

current_df = pd.read_csv(current_file,index_col=0)

print(current_df)

lat1 = 40.858654
long1 = -111.938995

a = []
b = []
for i in range(current_df.shape[0]):
    new_dist = pow((pow(abs(current_df.loc[i,"Latitude"] - lat1),2)+ pow(abs(current_df.loc[i,"Longitude"] - long1),2)),.5)
    a.append(new_dist)
print(current_df)
current_df.drop(a.index(min(a)),inplace = True)
current_df.reset_index(drop = True,inplace=True)
print(current_df)



