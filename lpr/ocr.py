import pytesseract
import cv2
import re
import string

def process_plate(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    img = cv2.medianBlur(img, 5)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    roi = None

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        if perimeter > 150:
            aprox = cv2.approxPolyDP(c, 0.03 * perimeter, True)
            if len(aprox) == 4:
                (x,y,w,h) = cv2.boundingRect(c)
                if w > h * 2.5:
                    cv2.rectangle(image, (x,y), (x + w, y + h), (0,255,0), 2)

                    #DESENHAR OS RETANGULOS NA IMAGEM COM FILTRO
                    cv2.rectangle(img, (x,y), (x + w, y + h), (0,255,0), 2)
                    
                    roi = img[y:y+h, x:x+w]

                    if roi is not None:
                        custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6'
                        plate = (pytesseract.image_to_string(roi, config=custom_config))
                        pattern = re.compile('[\W_]+')
                        plate = pattern.sub('', plate)
                        print('LEITURA DO ALGORITMO: ', plate)
                        
                        if(validate_plate(plate)):
                            return plate

    #COMENTA A QUE NAO FOR USAR
    #cv2.imshow('camera normal', image)
    
    #IMAGEM
    cv2.imshow('camera com filtros', img)
    
    return None

def validate_plate(plate):
    if isinstance(plate, str) and len(plate) == 7 and plate[:3].isalpha() and plate[3].isdigit() and plate[2:].isdigit():
        return True
    return False