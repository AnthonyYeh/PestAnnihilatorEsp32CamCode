import re

import serial
import cv2
import numpy as np

ser = serial.Serial("COM3", 2000000)

buf = b""


while True:
    cc = ser.read_all()
    buf += cc

    first_strip = buf.find(b"Start New One")
    if first_strip != -1:
        end_strip = buf[first_strip + len(b"Start New One"):].find(b"Start New One")
        if end_strip != -1:
            out_img_bytes = buf[first_strip + len(b"Start New One"): end_strip]
            
            buf = buf[end_strip + len(b"Start New One"):]

            nparr = np.fromstring(out_img_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            try:
                cv2.imshow('frame', img_np)
                if cv2.waitKey(1) == ord('q'):
                    break
            except cv2.error:
                pass

cv2.destroyAllWindows()
