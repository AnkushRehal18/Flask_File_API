import os
import time
folder_Path = r"D:\Document convertor\flask-file-api\uploads"

def clearUploadFolder(delay_seconds = 10):
    time.sleep(delay_seconds)
    for fileName in os.listdir(folder_Path):
        filePath = os.path.join(folder_Path, fileName)
        try:
            if os.path.isfile(filePath):
                os.remove(filePath)
                print(fileName, "is removed")
        except PermissionError:
            print(f"Could not delete {fileName} - still in use")