import shutil
import datetime as dt
from datetime import date
import os
import smtplib
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
        print(rows1)
        prices={}
        for m in range(0,len(rows1)):
            prices[rows1[m].split(',')[0]] = int(rows1[m].split(',')[2])
        print(prices)
        for i in range(0, len(rows1)):
            product_id1.append(rows1[i].split(',')[0])
        for i in range(0, len(rows)):
            if rows[i].split(',')[2] in product_id1 or rows[i].split(',')[2]=='':
                pass
            else:
                print('product_id is not present in product_master table')
                dst = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\'+c[z]
                dst1 = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\error_orders_1.csv'
                if not os.path.exists(dst1):
                    with open(dst1, 'a') as f3:
                        header = header.strip() + ',reason\n'
                        f3.write(header)
                with open(dst1, 'a') as f3:
                    f3.write(rows[i].strip() + ',product_id not found in masters table\n')
                shutil.copyfile('incoming_files\\20240418\\'+c[z], dst)
                status=1
                r+=1
                break
            ##Validation2
            print(int(rows[i].split(',')[3]),prices[rows[i].split(',')[2]],int(rows[i].split(',')[4]))
            if int(rows[i].split(',')[3])*prices[rows[i].split(',')[2]]==int(rows[i].split(',')[4]):
                pass
            else:
                print('quantity*price!=total sum')
                dst = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\' + c[z]
                dst1 = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\error_orders_1.csv'
                if not os.path.exists(dst1):
                    with open(dst1, 'a') as f3:
                        header = header.strip() + ',reason\n'
                        f3.write(header)
                with open(dst1, 'a') as f3:
                    f3.write(rows[i].strip() + ',total sales amount not equal to quantity*price\n')
                shutil.copyfile('incoming_files\\20240418\\'+c[z], dst)
                status = 1
                r+=1
                break
            ##Validaton3
            yr = '20' + rows[i][8:10]
            dt1 = date(int(yr), int(rows[i][5:7]), int(rows[i][2:4]))
            if (dt1 < dt.datetime.today().date()):
                pass
            else:
                print('order date is future...')
                dst = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\' + c[z]
                dst1 = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\error_orders_1.csv'
                if not os.path.exists(dst1):
                    with open(dst1, 'a') as f3:
                        header = header.strip() + ',reason\n'
                        print(header)
                        f3.write(header)
                with open(dst1, 'a') as f3:
                    f3.write(rows[i].strip() + ',order date is future\n')
                shutil.copyfile('incoming_files\\20240418\\'+c[z], dst)
                status = 1
                r+=1
                break
            ##Validation4
            s = rows[i].split(',')
            for j in range(0, len(s)):
                if s[j].strip()!= '':
                    continue
                else:
                    d = a[0].split(',')[j].strip()
                    print('{} is null'.format(a[0].split(',')[j].strip()))
                    dst = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\' + c[z]
                    dst1 = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\error_orders_1.csv'
                    if not os.path.exists(dst1):
                        with open(dst1, 'a') as f3:
                            header = header.strip() + ',reason\n'
                            print(header)
                            f3.write(header)
                    with open(dst1, 'a') as f3:
                        f3.write(rows[i].strip() + ',' + d + ' field is null\n')
                    shutil.copyfile('incoming_files\\20240418\\'+c[z], dst)
                    status = 1
                    r+=1
                    break
            ##Validation5
            if rows[i].split(',')[5].strip() == 'Bangalore' or rows[i].split(',')[5].strip() == 'Mumbai' or rows[i].split(',')[5].strip() == '':
                print('{} has passed all validations'.format(i + 1))
            else:
                print('city is {}'.format(rows[i].split(',')[5]))
                dst = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\' + c[z]
                dst1 = 'rejected_files\\' + dt.datetime.today().strftime('%Y%m%d') + '\\error_orders_1.csv'
                if not os.path.exists(dst1):
                    with open(dst1, 'a') as f3:
                        header = header.strip() + ',reason\n'
                        print(header)
                        f3.write(header)
                with open(dst1, 'a') as f3:
                    f3.write(rows[i].strip() + ',City is different\n')
                shutil.copyfile('incoming_files\\20240418\\'+c[z], dst)
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


Files_received=len(os.listdir('incoming_files\\20240418'))
files_rejected=len(os.listdir('rejected_files\\'+dt.datetime.today().strftime('%Y%m%d')))-1
files_accepted=len(os.listdir('success_files\\'+dt.datetime.today().strftime('%Y%m%d')))
##print(f'The total Number of files received is {Files_received} out of which {r} are rejected and {files_accepted} are accepted')
print(f'The total Number of files received is {Files_received} out of which {files_rejected} are rejected and {files_accepted} are accepted')


##Sending an email
s = smtplib.SMTP('smtp.gmail.com', 587)

s.starttls()
# Authentication
s.login("bujjy3717@gmail.com", "Prakash@21")
# message to be sent

message = 'The total Number of files received is' + str(Files_received) +' out of which ' + str(files_rejected)+' are rejected and '+ str(files_accepted)+ ' are accepted'
# sending the mail
s.sendmail("bujjy3717@gmail.com", "udayp43343@gmail.com", message)
# terminating the session
s.quit()




