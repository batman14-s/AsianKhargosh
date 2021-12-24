# pip install tensorflow
from pyfirmata import Arduino, OUTPUT
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cv2
# from tf.keras.models import load_model

facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
font=cv2.FONT_HERSHEY_COMPLEX
model = tf.keras.models.load_model('mask_model.h5')

port = '/dev/ttyACM0'
board = Arduino(port)

pin = 3
board.digital[pin].mode = OUTPUT

def preprocessing(img):
    img=img.astype("uint8")
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=cv2.equalizeHist(img)
    img = img/255
    return img


def get_className(classNo):
    if classNo==0:
        return "Mask"
    elif classNo==1:
        return "No Mask"

y = 100
x = 240
h = 200
w = 190

color = (0, 0, 0)
green = (0, 255, 0)
red = (50, 50, 255)

while True:
    sucess, imgOrignal=cap.read()

    crop_img=imgOrignal[y:y+h, x:x+h]
    cv2.imshow("Cropped image", crop_img)
    img=cv2.resize(crop_img, (64,64))
    img=img/255
    img = np.expand_dims(img, axis = 0)
    
    result=model.predict(img)
    probabilityValue=np.amax(result)
    predict = np.round(result[0][0])
    
    if predict == 0:
        color = green
        board.digital[pin].write(0)
    elif predict == 1:
        color = red
        board.digital[pin].write(1)
    cv2.rectangle(imgOrignal, (x, y), (x+w, y+h), color, 2)
    cv2.rectangle(imgOrignal, (x, y-40), (x+w, y), color, -2)
    cv2.putText(imgOrignal, str(get_className(predict)), (x, y-10), font, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Result",imgOrignal)
    
    k=cv2.waitKey(1)
    if k==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()














