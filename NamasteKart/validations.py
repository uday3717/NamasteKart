import datetime as dt
from datetime import date
import shutil
import os


def checkproduct_id(a,b):
    if(a in b):
        return True
    else:
        return False

def calci(a,b,c):
    return a*b==c


def future_date(dt1):
    if (dt1 < dt.datetime.today().date()):
        return True
    return False

def check_nullfield(s):
    for j in range(0, len(s)):
        if s[j].strip() != '':
            continue
        else:
            return False
    return True

def check_city(a):
    if a in ['Bangalore','Mumbai']:
        return True
    else:
        return False

def move_to_rejected(dst,dst1,error_reason,header,str,str1):
    if not os.path.exists(dst1):
        with open(dst1, 'a') as f3:
            header = header.strip() + ',reason\n'
            f3.write(header)
    with open(dst1, 'a') as f3:
        f3.write(str.strip()+error_reason)
    shutil.copyfile('incoming_files\\20240418\\' + str1, dst)

