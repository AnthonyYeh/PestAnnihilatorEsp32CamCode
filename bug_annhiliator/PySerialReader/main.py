import re
import traceback

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

    start_loc = buf.find(SOI)
    if start_loc != -1:
        end_loc = start_loc + buf[start_loc:].find(EOI)
        if end_loc != -1:
            out_img_bytes = buf[start_loc: end_loc + len(EOI)]
            
            buf = buf[end_loc + len(EOI):]

            nparr = np.fromstring(out_img_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            try:
                cv2.imshow('frame', img_np)
                if cv2.waitKey(1) == ord('q'):
                    break
            except cv2.error:
                traceback.print_exception()
                pass

cv2.destroyAllWindows()
