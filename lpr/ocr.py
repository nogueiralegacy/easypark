import pytesseract
import cv2
import re
import string

def process_plate(image):
    #PASSA A IMAGEM PARA UMA ESCALA DE CINZA
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #PASSA CADA PIXEL DA IMAGEM PARA UM THRESHOLD PRA FICAR PRETO OU BRANCO DEPENDENDO DA COR DO PIXEL BASEADO NA ESCALA DE CINZA ANTERIOR
    #O VALOR BASE USADO É 128, SENDO POSSÍVEL ALTERAR
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    #BORRA A IMAGEM PRA DEIXAR OS CARACTERES MAIS LEGÍVEIS CASO TENHA ALGUMA IMPERFEIÇÃO DENTRO DE CADA UM DELES (ex: TIVER LISTRAS BRANCAS/CINZAS DENTRO DA LETRA)
    #DÁ PRA USAR ESSE medianBlur (BORRA BASEADO EM UM VALOR, NESSE CASO 5) OU O GaussianBlur PASSANDO OUTROS PARÂMETROS
    img = cv2.medianBlur(img, 5)

    #BUSCA CONTORNOS TRAÇÁVEIS NA IMAGEM
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #INICIALIZANDO O RECORTE DA IMAGEM
    roi = None

    for c in contours:
        #DEFINE O PERÍMETRO DO CONTORNO
        perimeter = cv2.arcLength(c, True)
        if perimeter > 150:
            #FAZ UMA APROXIMAÇÃO DOS VÉRTICES DO CONTORNO PARA VER SE É UM RETÂNGULO
            aprox = cv2.approxPolyDP(c, 0.03 * perimeter, True)
            if len(aprox) == 4:
                #FAZ O TRAÇADO DO RETANGULO NAS CORDENADAS
                (x,y,w,h) = cv2.boundingRect(c)

                #VERIFICA SE A ALTURA * 2,5 É MENOR QUE O COMPRIMENTO, SENDO ASSIM SUSCETÍVEL A SER UMA PLACA
                if w > h * 2.5:
                    #DESENHA OS RETANGULOS NA IMAGEM SEM FILTRO
                    cv2.rectangle(image, (x,y), (x + w, y + h), (0,255,0), 2)

                    #DESENHA OS RETANGULOS NA IMAGEM COM FILTRO
                    cv2.rectangle(img, (x,y), (x + w, y + h), (0,255,0), 2)
                    
                    #RECORTA O CONTORNO DA IMAGEM
                    roi = img[y:y+h, x:x+w]

                    #PROCESSA O RECORTE
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
    
    #IMAGEM COM OS FILTROS E CONTORNOS APLICADOS
    cv2.imshow('camera com filtros', img)
    
    return None

def validate_plate(plate):
    if isinstance(plate, str) and len(plate) == 7 and plate[:3].isalpha() and plate[3].isdigit() and plate[2:].isdigit():
        return True
    return False