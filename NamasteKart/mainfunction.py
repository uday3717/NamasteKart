
import shutil
import datetime as dt
from datetime import date
import os
import smtplib
from mailservice import sendemail
from validations import checkproduct_id,future_date,move_to_rejected,calci,check_city,check_nullfield


r=0
c=os.listdir('incoming_files\\20240418')
for z in range(0,len(c)):
    with open('incoming_files\\20240418\\'+c[z],'r') as f1,open('incoming_files\\product_master.csv','r') as f2:
        if not os.path.exists('rejected_files/' + dt.datetime.today().strftime('%Y%m%d')):
            os.mkdir('rejected_files/' + dt.datetime.today().strftime('%Y%m%d'))
        product_id = []
        price=[]
        k=0
        product_id1 = []
        status=0
        a = f1.readlines()
        header = a[0]
        rows = a[1:]
        b = f2.readlines()
        rows1 = b[1:]
        prices={}
        dst = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\' + c[z]
        dst1 = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\error_orders_1.csv'
        for m in range(0,len(rows1)):
            prices[rows1[m].split(',')[0]] = int(rows1[m].split(',')[2])
        for i in range(0, len(rows1)):
            product_id1.append(rows1[i].split(',')[0])
        for i in range(0, len(rows)):
            str=rows[i]
            str1=c[z]
            if checkproduct_id(rows[i].split(',')[2],product_id1):
                pass
            else:
                error_reason='product_id not found in masters table\n'
                print(f'Rejecting file {c[z]} due to {error_reason}')
                move_to_rejected(dst, dst1,error_reason,header,str,str1)
                status=1
                r+=1
                break
            ##Validation2
            if calci(int(rows[i].split(',')[3]),prices[rows[i].split(',')[2]],int(rows[i].split(',')[4])):
                pass
            else:
                error_reason=',total sales amount not equal to quantity*price\n'
                print(f'Rejecting file {c[z]} due to {error_reason}')
                print('quantity*price!=total sum')
                move_to_rejected(dst, dst1, error_reason,header,str,str1)
                status = 1
                r+=1
                break
            ##Validaton3
            yr = '20' + rows[i][8:10]
            dt1 = date(int(yr), int(rows[i][5:7]), int(rows[i][2:4]))
            if future_date(dt1):
                pass
            else:
                error_reason=',order date is future\n'
                print(f'Rejecting file {c[z]} due to {error_reason}')
                print('order date is future...')
                move_to_rejected(dst, dst1, error_reason,header,str,str1)
                status = 1
                r+=1
                break
            ##Validation4
            s = rows[i].split(',')
            if check_nullfield(s):
                pass
            else:
                error_reason=',' +' field is null\n'
                print(f'Rejecting file {c[z]} due to {error_reason}')
                move_to_rejected(dst, dst1, error_reason,header,str,str1)
                status = 1
                r+=1
                break
            ##Validation5
            if check_city(rows[i].split(',')[5].strip()):
                print(f'{c[z]} row {i+1} has passed all validations')
            else:
                error_reason=',City is different\n'
                print(f'Rejecting file {c[z]} due to {error_reason}')
                print('city is {}'.format(rows[i].split(',')[5]))
                move_to_rejected(dst, dst1, error_reason,header,str,str1)
                status = 1
                r+=1
                break
        if(status==1):
            continue
        print('all rows of {} has passed all the validations'.format(c[z]))
        if not os.path.exists('success_files/' + dt.datetime.today().strftime('%Y%m%d')):
            os.mkdir('success_files/' + dt.datetime.today().strftime('%Y%m%d'))
        dest='success_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\'+c[z]
        shutil.copyfile('incoming_files\\20240418\\'+c[z], dest)
        continue

#getting the final count of files in the Input folder, Rejected and Success folder
Files_received=len(os.listdir('incoming_files\\20240418'))
files_rejected=len(os.listdir('rejected_files\\'+dt.datetime.today().strftime('%Y%m%d')))-1
files_accepted=len(os.listdir('success_files\\'+dt.datetime.today().strftime('%Y%m%d')))
##print(f'The total Number of files received is {Files_received} out of which {r} are rejected and {files_accepted} are accepted')
print(f'The total Number of files received is {Files_received} out of which {files_rejected} are rejected and {files_accepted} are accepted')

body=f'The total Number of files received is {Files_received} out of which {files_rejected} are rejected and {files_accepted} are accepted'

#sending an email
sendemail('From Namaste Kart Solutions',body)








