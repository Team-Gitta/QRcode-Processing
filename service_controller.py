import cv2
import math
import serial
import time
import pymysql
ser = serial.Serial('/dev/ttyAMA0',115200)
ser.timeout = 100
def dist(point1, point2): 
    return math.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point2[1],2))

def bring_info(username, id): #return height and water from db gitta using username and id
    db=pymysql.connect(host = 'localhost',user='root',port=3306,passwd='ilovegitta',db='gitta',charset='utf8')
    cursor = db.cursor()
    sql = "select * from %s where id = '%s'" % (username, id)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = result[0]
    height = result[2]
    water = result[6]
    return height,water

#height, water  = bring_info('seohyun218','seohyun218_123')



def serial_communication(ratio, height, water):
    detected_time = time.time()

        

def detect_qrcode(username ,id):
    pos = ['right','bottom','left','top']
    bottom =0
    left=0
    right=0
    top = 0
    ratio=0
    top_point=0
    cap = cv2.VideoCapture(0)
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
                     if(i==0):
                         right = dist(point1,point2)
                         right_point = point1[0]
                     if(i==1):
                         bottom = dist(point1,point2)
                     if(i==2):
                         left= dist(point1,point2)
                         left_point = point1[0]
                     if(i==3):
                         top = dist(point1,point2)
                         top_point = point1[1]
                         ratio=left/right
                         print("top Point : ",top_point)
                         print("left Point : ", left_point)
                         print("right Point  : ", right_point)
            if data:
                print("[+] QR Code detected, data:", data)
                if (bottom >= 150 and left >= 150):
                    if data == id:
                            #height, water = bring_info(username,id)
                            #serial_communication(ratio,height,water)
                            detected_time = time.time()
                            if(top_point >600):
                                key = '4'
                                ser.write(key)
                            else:
                                key = '8'
                                ser.write(key)
                            if(right_point > 1500):
                                key = '1'
                                ser.write(key)    
                            elif(right_point > 900):
                                key = '2'
                                ser.write(key)
                            while 1:
                                pump_time = time.time()
                                if pump_time > detected_time+4:
                                    key = '7'
                                    ser.write(key)
                                    #pump_operation_time = water*3
                                    pump_operation_time = 4
                                    break
                            while 1:                                    
                                pump_stop_time = time.time()
                                if pump_stop_time > detected_time+4+pump_operation_time:
                                    key = '6'
                                    ser.write(key)
                                    break
                            while 1:
                                return_time = time.time()
                                if return_time > detected_time + pump_operation_time+3:
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
detect_qrcode('seohyun','seoo')
