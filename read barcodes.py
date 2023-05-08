from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
im = cv2.imread(r'C:\Users\python_account\Pictures\Barcodes\new tree.jpg', cv2.IMREAD_GRAYSCALE)
blur = cv2.GaussianBlur(im, (5, 5), 0)
ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
decode(bw_im, symbols=[ZBarSymbol.CODE128])