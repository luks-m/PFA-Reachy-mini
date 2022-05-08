import os
import time
import cv2

# A simple bubble sort
def increase_date_sort(paths):
    flag = True
    while flag:
        flag = False
        for i in range(len(paths) - 1):
            date1, date2 = os.path.getmtime(paths[i]), os.path.getmtime(paths[i+1])
            if date1 > date2 :
                paths[i], paths[i+1] = paths[i+1], paths[i]
    return paths

# Be careful, deletion of png here !
def delete_png_in(path, n_if_over, m_to_delete):
    paths = []
    for file in os.listdir(path):
        if os.path.isfile(path + '/' + file) and file.endswith(".png"):
            paths.append(path + '/' + file)
    if len(paths) < n_if_over:
        print(n_if_over)
        print("Nothing to remove")
        return
    paths = increase_date_sort(paths)
    paths = paths[:m_to_delete]
    for path in paths:
        os.remove(path)
        print(f"Removed : {path}")

# Return None if no png in path
def give_youngest_png_path(path):
    paths = []
    for file in os.listdir(path):
        if os.path.isfile(path + '/' + file) and file.endswith(".png"):
            paths.append(path + '/' + file)
    paths = increase_date_sort(paths)
    if len(paths) > 0:
        return paths[-1]
    else:
        print(f"No png in the directory : {path}")
        return None

def show_youngest_png(path):
    youngest_png = give_youngest_png_path(path)
    print(youngest_png)
    img = cv2.imread(youngest_png)
    cv2.namedWindow("Your picture", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Your picture', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Your picture", img)