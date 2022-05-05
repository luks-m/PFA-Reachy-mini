import png_treatment as tr
import time

if __name__ == "__main__":
    while True :
        tr.delete_png_in('../../tmp/img', 1, 200)
        time.sleep(10)
