import cv2
from ocr import process_plate
from message import send_message
import time


def main():
    cam = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cam.read()
        
        placa = process_plate(frame)
        
        if placa is not None:
            print('PLACA ENVIADA: ', placa)
            send_and_halt(plate=placa)

        if cv2.waitKey(1) == ord('q'):
            break


def send_and_halt(plate):
    send_message(plate=plate)
    time.sleep(10)


main()
