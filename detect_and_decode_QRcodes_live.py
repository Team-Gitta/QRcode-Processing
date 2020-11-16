import cv2
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

            if data:
                print("[+] QR Code detected, data:", data)
        # display the result
        cv2.imshow("img", img)    
        if cv2.waitKey(1) == ord("q"):
            break
    except Exception as e:
        print("err:", str(e))
cap.release()
cv2.destroyAllWindows()