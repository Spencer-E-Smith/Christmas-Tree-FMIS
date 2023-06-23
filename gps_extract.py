import os
from exif import Image
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import pandas as pd
from datetime import datetime
import tkinter as tk
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import plotly.express as px

aerial_photo_path = 'C:\\Users\\spenc\\OneDrive\\Pictures\\farm north.JPG'
data_save_location = 'C:\\Users\\spenc\\OneDrive\\Documents\\Project Data\\'
input_data_path = 'C:\\Users\spenc\\OneDrive\\Pictures\\final upload'


def display_data(data_list, subset):
    temp_list = []
    if len(subset) != 0:
        for i in data_list:
            if i[1] in subset:
                temp_list.append(i)
        data_list = temp_list

    fig, ax = plt.subplots()
    def mapping_data(atlas_data):
        x, y = [], []
        
        x.append(atlas_data[2])
        y.append(atlas_data[3])

        return x, y
    def add_scatter(x,y, color):
        ax.scatter(x, y, edgecolor='yellow', zorder=2,)
    def unique(list1):
    # initialize a null list
        unique_list = []
    # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        # print list
        return unique_list
    descriptions = []
    x = []
    y = []
    for i in data_list:
        x.append(i[3])
        y.append(i[2])
        descriptions.append(i[1])
    unique_descriptions = []
    for i in descriptions:
        if i not in unique_descriptions:
            unique_descriptions.append(i)
    
    colors = []
    for i in range(len(unique_descriptions)):
        colors.append(i/len(unique_descriptions))
    
    for i in range(len(colors)):
        current_x =[]
        current_y =[]
        current_color = []
        for j in range(len(descriptions)):
            if unique_descriptions[i] == descriptions[j]:
                current_x.append(x[j])
                current_y.append(y[j])
                current_color.append(colors[i])           
        add_scatter(current_x, current_y, current_color)
    #ax.scatter(x, y, c=colors, edgecolor = 'red', zorder=2,)
    ax.imshow(mpimg.imread(aerial_photo_path), extent=(-120.717566420228, -120.71407, 38.7385559849825, 38.74139), zorder=1)
    plt.legend(unique_descriptions)
    plt.savefig('C:\\Users\\spenc\\OneDrive\\Pictures\\6_18_map.png',dpi = 800)
    plt.show()

#create task class
class task:
    def __init__(self, file_path, task_type, latitude, longitude, date_picture_taken, date_picture_processed):
        self.file_path = file_path
        self.task_type = task_type
        self.latitude = latitude
        self.longitude = longitude
        self.date_picture_taken = date_picture_taken
        self.date_picture_processed = date_picture_processed
    
    def valid(self):
        #check for error message or NoneType
        e = 'error'
        if self.latitude is not None and self.task_type is not None:
            if e in str(self.latitude) or e in str(self.task_type):
                return False
            else:
                return True
        else:
            return False


#Convert to decimal coodinates
def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == 'S' or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees

#extracts and prints GPS coordinates
def img_coords(f_name):
    with open(f_name, 'rb') as src:
        img = Image(src)
        print(src.name, img)
    if img.has_exif:
        try:
            img.gps_longitude
            return [decimal_coords(img.gps_latitude, img.gps_latitude_ref), decimal_coords(img.gps_longitude, img.gps_longitude_ref), img.datetime_original]
        except Exception as e:
            return ['error during exif read', e, None]
    else:
        return ['error', 'no exif', None]
    #print(f"Image {src.name}, was taken: {img.datetime_original}, and has coordinates: {coords}")

def barcode_error_fixing(picture_path,error_code):
    if '(' in os.path.basename(picture_path):
        name = os.path.basename(picture_path)
        return name[name.find('(')+1:name.find(')')]
    else:
        return error_code

def read_barcode(picture_path):
    im = cv2.imread(picture_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(im, (5, 5), 0)
    ret, bw_im = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    barcode_info = decode(bw_im)#, symbols=[ZBarSymbol.CODE128])
    if barcode_info == []:
        return barcode_error_fixing(picture_path,"error: no barcode found")
    elif len(barcode_info) > 1:
        return barcode_error_fixing(picture_path,"error: multiple barcodes")
    else:
        return barcode_info[0].data.decode("utf-8")

def new_data():
    columns_upload = ['Picture File Path', 'Task Type', 'Latitude', 'Longitude', 'Date Picture Taken', 'Date Picture Processed']
    columns_errors = ['Picture File Path', 'Barcode', 'exif', 'exif_detail']
    picture_df = pd.DataFrame(columns = columns_upload)
    errors_df = pd.DataFrame(columns = columns_errors)
    root = input_data_path
    image_list = os.listdir(root)
    image_list = [root + '\\' + a  for a in image_list if a.upper().endswith('JPG')]
    #print(image_list)
    now = datetime.now().timestamp()
    for a in image_list:
        barcode_string = read_barcode(a)
        exif_list = img_coords(a)
        current_pic = task(a,barcode_string, exif_list[0], exif_list[1], exif_list[2], now)
        if current_pic.valid():
            picture_df.loc[picture_df.shape[0]] = [current_pic.file_path, current_pic.task_type, current_pic.latitude,\
                                            current_pic.longitude, current_pic.date_picture_taken, now]
        else:
            errors_df.loc[errors_df.shape[0]] = [current_pic.file_path, current_pic.task_type, current_pic.latitude,\
                current_pic.longitude]
        del current_pic

    folder = data_save_location
    picture_df.to_csv(folder + 'picturedata' + str(now) + '.csv' )           #   folder + r'\picture_data' + datetime_string + '.csv')
    errors_df.to_csv(folder + 'errors' + str(now) + '.csv')

def load_newest_file(path):
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
    return current_df

def remove_closest_task(lat1,long1,current_df):

    a = []
    for i in range(current_df.shape[0]):
        new_dist = pow((pow(abs(current_df.loc[i,"Latitude"] - lat1),2)+ pow(abs(current_df.loc[i,"Longitude"] - long1),2)),.5)
        a.append(new_dist)
    print(current_df)
    current_df.drop(a.index(min(a)),inplace = True)
    current_df.reset_index(drop = True,inplace=True)
    return current_df

#new_data()
df = load_newest_file(data_save_location)
display_data(df.values.tolist(),[])

fig = px.bar(df.groupby('Task Type').count().reset_index(level = 0), x= 'Task Type', y = 'Latitude')
fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
fig.show()


'''
input_list = [['a',
  38.74080556,-120.7152111
],
 ['b',
  38.74122778,-120.715225
]
,
 ['c',
  38.73989444,-120.714875
]
,
 ['d',
  38.73910278,-120.7173778
]
,
 ['e',
  38.74096389,-120.7169417
]
]
#input_list = [['a',38.74080556,-120.7152111],['b',38.74122778,-120.715225]['c',38.73989444,-120.714875]['d',38.73910278,-120.7173778]['e',38.74096389,-120.7169417]]

display_data(input_list)

              
root = tk.Tk()

root.title("FMIS")

path_label = tk.Label(root,text = "Enter Path for Data Storage")

default_path = "C:\\Users\\python_account\\Documents\\project_data"
file_path = tk.StringVar()
file_path.set(default_path)

path_entry = tk.Entry(root, textvariable= file_path, width= 100)

submit1 = tk.Button(root, text = "Submit", command = root.destroy)

path_label.grid(row=0,column=0)
path_entry.grid(row=0,column=1)
submit1.grid(row=0,column=2)

root.mainloop()
'''