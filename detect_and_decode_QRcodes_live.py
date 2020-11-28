import cv2
import math
import serial
import time

ser = serial.Serial('/dev/ttyAMA0',115200)
ser.timeout = 100
def dist(point1, point2): 
    return math.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point2[1],2))   

def detect_qrcode():
    pos = ['right','bottom','left','top']
    bottom =0
    left=0
    right=0
    top = 0
    ratio =0
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        #try:
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
                     print(pos[i] , ": " , dist(point1,point2))
                     print(point1,point2)
                     if(i==0):
                         right= dist(point1,point2)
                         
                     if(i==1):
                         bottom = dist(point1,point2)
                     if(i==2):
                         left = dist(point1,point2)
                                                  
                     if(i==3):
                         top = dist(point1,point2)
                         
                         ratio=left/right # left : 1.1 right : 0.0
                         print("ratio :",ratio)
            
            if data:
                print("[+] QR Code detected, data:", data)
                if bottom >= 260:
                    if data == 'seo':
                            print("start")
                            #height, water = bring_info(username,id)
                            #serial_communication(ratio,height,water)
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
                                if pump_stop_time > detected_time+20:
                                    key = '6'
                                    ser.write(key)
                                    break
                            while 1:
                                return_time = time.time()
                                if return_time > detected_time + 13:
                                    key = '5'
                                    ser.write(key)
                                    break
                    
                    
        #display the result
            img = cv2.resize(img,(300,300))
            cv2.imshow("img", img)    
            if cv2.waitKey(1) == ord("q"):
                break
        #except Exception as e:
           # print("err:", e)
    # cap.release()
     #   cv2.destroyAllWindows()

detect_qrcode()
