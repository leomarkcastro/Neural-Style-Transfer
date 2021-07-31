from artMaker import callProcess
import os
import copy

import json

import sys

import secrets
import datetime

import random

# read file
template = {

    "style_image": "",
    "content_image": "",

    "output_size": "512",

    "iterations": "200",
    "create_iter": "100",
    
    "model": "accurate",
    "cpu": "gpu_modified",

    "style_scale": "1.0",
    "content_weight": "5",
    "style_weight": "100",
    
    "original_color": "No",

}

content_folder = "content/"

save_file = "save.json"
save_progress : list = []

def save(data) -> None:
    with open(save_file, "w+") as fp:
        json.dump(data, fp)

def jobTask(jobQueue, content, style, booster_style=None):

    global save_progress

    if not os.path.exists(save_file):
        save([])

    with open(save_file) as fp:
        save_progress = json.load(fp)


    if os.path.exists(content_folder):

        file_to_do = os.listdir(f"{content}/")

        [random.shuffle(file_to_do) for _ in range(5)]

        session_folder = f"outputset_{datetime.datetime.now().strftime('%m%d %H%M%S')}_{secrets.token_hex(4)}"
        
        for ix, image in enumerate(file_to_do):

            if image in save_progress:
                continue

            save_progress.append(image)

            for iy, job in enumerate(jobQueue):
                print(f"\n\n\n------------------------\n\n")
                print(f"DOING PROCESS [{ix+1}][{iy+1}/{len(jobQueue)}] OF {len(file_to_do)}")
                task = copy.deepcopy(job)
                task["content_image"] = f"{content}/{image}"
                callProcess(task, session_folder, style, booster_style)
            
                save(save_progress)
        
        print("\n\n\nProcess DONE")
        print("Press Enter to EXIT\n\n\n\n")

    else:

        print("\n\n\nContent folder does not exist")
        #print("Done creating the excel File\n\n\n")

if __name__ == "__main__":
    args = sys.argv
    read = ""
    with open(args[1]) as fp:
        read = json.load(fp)

    jobTask(read, args[2], args[3])