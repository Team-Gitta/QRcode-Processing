import cv2
import math
import serial
import time
ser = serial.Serial('/dev/ttyAMA0',115200)
ser.timeout = 100
def dist(point1, point2):
	return math.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point2[1],2))

pos = ['bottom','left','top','right']
left=0
right=0
# initalize the cam
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
while True:
    try:
        _, img = cap.read()
        # detect and decode
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if bbox is not None:
            for i in range(4):
                # draw all lines
                point1 = tuple(bbox[0][i])
                point2 = tuple(bbox[0][(i+1) % 4])
                cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)
                print(pos[i],": ",dist(point1,point2))
                if(i==1):
                    left = dist(point1,point2)
                if(i==3):
                    right = dist(point1,point2)
                    print(left/right) # left : 1.1 right : 0.0
            if data:
                print("[+] QR Code detected, data:", data)
                if data == 'seoo':
                    detected_time = time.time()
                    key = '8'
                    ser.write(key)
                    while 1:
                        pump_time = time.time()
                        if pump_time > detected_time+4:
                            key = '7'
                            ser.write(key)
                            break
                    while 1:
                        pump_stop_time = time.time()
                        if pump_stop_time > detected_time+10:
                            key = '6'
                            ser.write(key)
                            break
                    while 1:
                        return_time = time.time()
                        if return_time > detected_time + 13:
                            key = '5'
                            ser.write(key)
                            break

                    break
        #display the result
        #cv2.imshow("img", img)    
        #if cv2.waitKey(1) == ord("q"):
            # break
    except Exception as e:
        print("err:", str(e))
cap.release()
cv2.destroyAllWindows()
