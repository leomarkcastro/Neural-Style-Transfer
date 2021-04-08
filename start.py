from model_uploader import ModelManager
from artMaker import callProcess
import os


import secrets
import datetime

# read file
file_to_read = "tasks.xlsx"
mm = ModelManager()

if os.path.exists(file_to_read):
    
    data = mm.excel_Read(file_to_read)

    session_folder = f"outputset_{datetime.datetime.now().strftime('%m%d %H%M%S')}_{secrets.token_hex(4)}"

    # process files
    for i, entry in enumerate(data):
        print(f"\n\n\n------------------------\n\n")
        print(f"DOING PROCESS {i+1} OF {len(data)}")
        callProcess(entry, session_folder)
        print("\n\n\n")

    print("\n\n\nProcess DONE")
    print("Press Enter to EXIT\n\n\n\n")

else:

    print("\n\n\nNo 'tasks.xlsx' found. Created a new one instead. Rerun the app again to start the creation")
    mm.create_excelTemplate(file_to_read)
    print("Done creating the excel File\n\n\n")