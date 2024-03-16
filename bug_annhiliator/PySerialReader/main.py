import re

import serial
import cv2
import numpy as np

# SOI and EOI must not be b""
SOI = b"\xff\xd8"  # start of image bytes sequence
EOI = b"\xff\xd9"  # end of image bytes sequence

ser = serial.Serial("COM3", 2000000)

buf = b""


while True:
    cc = ser.read_all()
    buf += cc

    first_strip = buf.find(SOI)
    if first_strip != -1:
        end_strip = first_strip + buf[first_strip:].find(EOI)
        if end_strip != -1:
            out_img_bytes = buf[first_strip: end_strip + len(EOI)]
            
            buf = buf[end_strip + len(EOI):]

            nparr = np.fromstring(out_img_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            try:
                cv2.imshow('frame', img_np)
                if cv2.waitKey(1) == ord('q'):
                    break
            except cv2.error:
                pass

cv2.destroyAllWindows()
