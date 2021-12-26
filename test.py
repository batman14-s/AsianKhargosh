from pyfirmata import Arduino, OUTPUT
import tensorflow as tf
import numpy as np
import cv2

url = "https://192.168.1.6:8080/video"
cv2.namedWindow('Phone Video', cv2.WINDOW_NORMAL)
phonecap = cv2.VideoCapture(url)

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
font=cv2.FONT_HERSHEY_COMPLEX
model = tf.keras.models.load_model('mask_model.h5')

port = '/dev/ttyACM0'
board = Arduino(port)

buzzor_pin = 3
motor_pin = 8
board.digital[buzzor_pin].mode = OUTPUT
board.digital[motor_pin].mode = OUTPUT


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
    camera, phoneframe = phonecap.read()

    crop_img=imgOrignal[y:y+h, x:x+h]
    img=cv2.resize(crop_img, (64,64))
    img=img/255
    img = np.expand_dims(img, axis = 0)
    
    result=model.predict(img)
    predict = np.round(result[0][0])
    
    if predict == 0:
        color = green
        board.digital[buzzor_pin].write(0)
        board.digital[motor_pin].write(1)
    elif predict == 1:
        color = red
        board.digital[buzzor_pin].write(1)
        board.digital[motor_pin].write(0)
    cv2.rectangle(imgOrignal, (x, y), (x+w, y+h), color, 2)
    cv2.rectangle(imgOrignal, (x, y-40), (x+w, y), color, -2)
    cv2.putText(imgOrignal, str(get_className(predict)), (x, y-10), font, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imshow("Result",imgOrignal)
    # cv2.imshow("Cropped image", crop_img)
    cv2.imshow("Phone Video", phoneframe)   
    cv2.resizeWindow('Phone Video', 740,480) 
    k=cv2.waitKey(1)
    if k==ord('q'):
        break

board.digital[motor_pin].write(0)
board.digital[buzzor_pin].write(0)
cap.release()
cv2.destroyAllWindows()
