import png_treatment as tr
import time
import sys

if __name__ == "__main__":
    while True :
        tr.delete_png_in('../../tmp/img', 1, sys.argv[1])
        time.sleep(10)
