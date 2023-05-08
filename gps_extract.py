import os
from exif import Image

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
            coords = (decimal_coords(img.gps_latitude, img.gps_latitude_ref), decimal_coords(img.gps_longitude, img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print('No EXIF')
    print(f"Image {src.name}, was taken: {img.datetime_original}, and has coordinates: {coords}")



root = 'C:\\Users\\python_account\\Pictures\\GPS'
image_list = os.listdir(root)
image_list = [root + '\\' + a  for a in image_list if a.endswith('JPG')]
print(image_list)

for a in image_list: 
    img_coords(a)