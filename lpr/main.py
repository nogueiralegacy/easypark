from os import walk
import cv2
from ocr import process_plate

def main():
    cam = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cam.read()
        
        placa = process_plate(frame)
        print(placa)
    
        if cv2.waitKey(1) == ord('q'):
            break
        
main()