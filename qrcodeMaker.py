import qrcode
# example data
data = "princess seohyun"
# output file name
filename = "qrcode.png"
# generate qr code
img = qrcode.make(data)
# save img to a file
img.save(filename)