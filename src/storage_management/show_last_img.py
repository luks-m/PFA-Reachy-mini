import png_treatment as tr
import time
import cv2

if __name__ == "__main__":
    while True:
        print("Your picture :")
        tr.show_youngest_png('../../tmp/img')
        cv2.waitKey(0)
        cv2.destroyAllWindows()