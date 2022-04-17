import os
import time
import cv2

# A simple bubble sort
def decrease_date_sort(paths):
    flag = True
    while flag:
        flag = False
        for i in range(len(paths) - 1):
            date1, date2 = os.path.getmtime(paths[i]), os.path.getmtime(paths[i+1])
            if date1 < date2 :
                paths[i], paths[i+1] = paths[i+1], paths[i]
    return paths

# Be careful, deletion of png here !
def delete_png_in(path, n_to_delete, m_if_over):
    paths = []
    for file in os.lisdir(path):
        if os.path.isfile(path + '/' + file) and file.endswith(".png"):
            paths.append(path + '/' + file)
    if len(paths) >= m_if_over:
        paths = decrease_date_sort(paths)
    paths = paths[:n]
    for path in paths:
        os.remove(path)
        print(f"Removed : {path}")

# Return None if no png in path
def give_elder_png_path(path):
    paths = []
    for file in os.lisdir(path):
        if os.path.isfile(path + '/' + file) and file.endswith(".png"):
            paths.append(path + '/' + file)
    if len(paths) > 0:
        return paths[0]
    else:
        print(f"No png in the directory : {paht}")
        return None

def apply_png_deletion_policy(path, time_gap):
    number_to_delete = 2
    number_to_trigger_deletion = 5
    delete_png_in(path, number_to_delete, number_to_trigger_deletion)
    time.sleep(time_gap)

def show_elder_png(path):
    elder_png = give_elder_png_path(path)
    cv2.imread(elder_png)