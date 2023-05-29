import os
from exif import Image
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import pandas as pd
from datetime import datetime
import tkinter as tk
import re

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

def read_barcode(picture_path):
    im = cv2.imread(picture_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(im, (5, 5), 0)
    ret, bw_im = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    barcode_info = decode(bw_im)#, symbols=[ZBarSymbol.CODE128])
    if barcode_info == []:
        return "error: no barcode found"
    elif len(barcode_info) > 1:
        return "error: multiple barcodes"
    else:
        return barcode_info[0].data.decode("utf-8")

def new_data():
    columns_upload = ['Picture File Path', 'Task Type', 'Latitude', 'Longitude', 'Date Picture Taken', 'Date Picture Processed']
    columns_errors = ['Picture File Path', 'Barcode', 'exif', 'exif_detail']
    picture_df = pd.DataFrame(columns = columns_upload)
    errors_df = pd.DataFrame(columns = columns_errors)
    root = r'C:\Users\python_account\Pictures\combination_test'
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

    folder = 'C:\\Users\\python_account\\Documents\\project_data\\'
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

def remove_closest_task(lat1,long1,current_df):

    a = []
    for i in range(current_df.shape[0]):
        new_dist = pow((pow(abs(current_df.loc[i,"Latitude"] - lat1),2)+ pow(abs(current_df.loc[i,"Longitude"] - long1),2)),.5)
        a.append(new_dist)
    print(current_df)
    current_df.drop(a.index(min(a)),inplace = True)
    current_df.reset_index(drop = True,inplace=True)
    return current_df
                 
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