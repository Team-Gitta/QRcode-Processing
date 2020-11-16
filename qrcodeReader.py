import cv2
import argparse

parser = argparse.ArgumentParser(description='image file name')
parser.add_argument('--filename',type=str, help='image file name')
args = parser.parse_args()
filename =args.filename
print(filename)
# read the QRCODE image
img = cv2.imread(filename)

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

# detect and decode
data, bbox, straight_qrcode = detector.detectAndDecode(img)

# if there is a QR code
if bbox is not None:
    print(f"QRCode data:\n{data}")
    # display the image with lines
    # length of bounding box
    for i in range(4):
        # draw all lines
        point1 = tuple(bbox[0][i])
        point2 = tuple(bbox[0][(i+1) % 4])
        cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)

# display the result
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()