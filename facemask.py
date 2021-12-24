from pyfirmata import Arduino, SERVO
port='COM5'
board=Arduino(port)
pin=10
board.digital[pin].mode=SERVO
def rotateServo(pin,angle):
    board.digital[pin].write(angle)
def doorAuto(val):
    if val==0:
        rotateServo(pin,180)
    elif val==1:
        rotateServo(pin,40)

