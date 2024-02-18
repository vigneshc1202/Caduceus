from json import *
from datetime import *
from csv import *
import sys
from pathlib import Path
import os

# Initial set-up options
def exist(email:str,passw,scr):
    try:
        # if user is new, creating an file
        with open(email+'.json','x') as f:
            with open(r'C:\Users\Caduceus\Music\codes\samp.json') as m:
                cont=load(m)
                dump(cont,f,indent=4)
        login(email,passw)
        utype(email,scr)
        save_current_acc(email)
        print('New user:',email)
        return 0
    except:
        return 1
def check_exist(email):
    try:
        with open(email+'.json','r') as f:
            return 1
    except:
        return 0
def login(email:str,passw:str):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['id']['email']=email
        cont['id']['passw']=passw
        dump(cont,f,indent=4)
def cuser_type(email,c='p'):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        if cont['id']['acc_type']=='patient':
            return 'main.py'
        elif cont['id']['acc_type']!='doctor':
            cont['id']['acc_type']='patient'
            dump(cont,f,indent=4)
        else:
            return 'doctor.py'
def store(email,acc,head,subhead,nv):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont[acc][head][subhead]=nv
        dump(cont,f,indent=4)
#Checking if credentials are correct or not
def clogin(email:str,passw:str):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        if cont['id']['email']==email and cont['id']['passw']==passw:
            save_current_acc(email)
            return 1
        else:
            return 0
# Login count function
def login_cnt_inc(email,n=0):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['login_count']+=1
        dump(cont,f,indent=4)

def login_cnt_check(email,n=0):
    try:
        with open(email+'.json','r+') as f:
            try:
                cont=load(f)
                f.seek(0)
                if cont['login_count']>50:
                    return 0
                else:
                    return 1
            except:
                print('User file deleted!!')
                reset_current_user()
    except:
        print('User file deleted!!')
        reset_current_user()
        sys.exit()
def reset_login_cnt(email):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['login_count']=10
        dump(cont,f,indent=4)
def utype(email,screen_name):
    if screen_name=='p_login_screen':
        with open(email+'.json','r+') as f:
            cont=load(f)
            f.seek(0)
            cont['id']['acc_type']='patient'
            f.seek(0)
            dump(cont,f,indent=4)
    else:
        with open(email+'.json','r+') as f:
            cont=load(f)
            f.seek(0)
            cont['id']['acc_type']='doctor'
            f.seek(0)
            dump(cont,f,indent=4)
def bp_check(sys,dia):
    try:
        sys,dia=int(sys),int(dia)
        if sys<=90 and dia<=60:
            bp_result=f'Low BP!! \nEat more salt content foods like Fish etc.'
        elif sys<130 and dia<100:
            bp_result=f'Normal BP \nNo need to worry!'
        elif sys<=160 and dia<=100:
            bp_result=f'Hypertension BP!!! \nDo not get angry!! Do meditation'
        elif sys<200 and dia<120:
            bp_result=f'High Hypertension BP!! \nWe suggest you to consult a doctor and get a fast checkup!'
        else:
            #print('Invalid numberss..')
            bp_result=f'Invalid values entered'
    except:
        bp_result='Invalid character!!'
    return bp_result

def bmi_check(h,w):
    bmi=0
    try:
        h,w=float(h),int(w)
        bmi = w//(h**2)
        #Checking the result and updating the answer
        if bmi<=18.5:
            bmi_result=f'You are underweight! \nConsult a nutritionalist'
        elif bmi<=25:
            bmi_result=f'Your weight is proper \nMaintain the same weight'
        elif bmi>40:
            bmi_result=f'You are overweight! \nDo exercise and bet fit'
        elif bmi<40:
            bmi_result=f'You are obese!! \nConsult a doctor as soon as possible'
        else:
            bmi_result=f'Invalid values entered'
    except:
        bmi_result=f'Invalid character!!'
    return bmi_result,bmi
def bmi_save(email,bmi,comment):
    email=load_current_acc()
    with open(email+'.json','r+') as f:
        cont=load(f)
        td=datetime.now()
        savedate=f"{td.strftime('%d')} {td.strftime('%b')} {td.strftime('%Y')}"
        old=cont['pacc_dtls']['tests']['BMI']
        saveas=[savedate,f'BMI:{bmi}',comment]
        f.seek(0)
        old.append(saveas)
        dump(cont,f,indent=4)
def bp_save(email,sys,dia,res):
    email=get_curr_user()
    with open(email+'.json','r+') as f:
        cont=load(f)
        td=datetime.now()
        savedate=f"{td.strftime('%d')} {td.strftime('%b')} {td.strftime('%Y')}"
        old=cont['pacc_dtls']['tests']['BP']
        saveas=[savedate,f'BP:{sys}/{dia}',res]
        f.seek(0)
        old.append(saveas)
        dump(cont,f,indent=4)
def load_pdtls(email,n,ph,age,addr):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['pacc_dtls']['dtls']['name']=n
        cont['pacc_dtls']['dtls']['ph_no']=ph
        cont['pacc_dtls']['dtls']['age']=age
        cont['pacc_dtls']['dtls']['addr']=addr
        dump(cont,f,indent=4)
def load_ddtls(email,n,ph,age,addr,qlf,exp):
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['dacc_dtls']['dtls']['name']=n
        cont['dacc_dtls']['dtls']['ph_no']=ph
        cont['dacc_dtls']['dtls']['age']=age
        cont['dacc_dtls']['dtls']['addr']=addr
        cont['dacc_dtls']['dtls']['qlf']=qlf
        cont['dacc_dtls']['dtls']['exp']=exp
        doc_add_dtls(email,n,qlf,exp)
        dump(cont,f,indent=4)
def load_ddtls2(email,fee,about_me,use):
    email=get_curr_user()
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['dacc_dtls']['dtls']['fee']=fee
        cont['dacc_dtls']['dtls']['about_me']=about_me
        if use==1:
            add_fee_doclist(email,fee)
        dump(cont,f,indent=4)
def get_pdtls(email):
    try:
        if email=='':
            email=load_current_acc()
            email=get_absolute_path(email)
        email=get_absolute_path(email)
        with open(email+'.json','r+') as f:
            cont=load(f)
            f.seek(0)
            n=cont['pacc_dtls']['dtls']['name']
            ph=cont['pacc_dtls']['dtls']['ph_no']
            age=cont['pacc_dtls']['dtls']['age']
            addr=cont['pacc_dtls']['dtls']['addr']
            return n,ph,age,addr
    except:
       # print('Error!!')
        return 'error',0,0,0
def get_ddtls(email):
    if email=='':
        email=load_current_acc()
        #email=get_absolute_path(email)
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        #f.seek(0)
        n=cont['dacc_dtls']['dtls']['name']
        ph=cont['dacc_dtls']['dtls']['ph_no']
        age=cont['dacc_dtls']['dtls']['age']
        addr=cont['dacc_dtls']['dtls']['addr']
        qlf=cont['dacc_dtls']['dtls']['qlf']
        exp=cont['dacc_dtls']['dtls']['exp']
        return n,ph,age,addr,qlf,exp
def get_ddtls2(email):
    if email=='':
        email=load_current_acc()
    try:
        with open(email+'.json','r+') as f:
            cont=load(f)
            f=cont['dacc_dtls']['dtls']['fee']
            about=cont['dacc_dtls']['dtls']['about_me']
            return f,about
    except:
        print('Doctor account deleted!')
        return '0',0
def get_total_records(email):
    if email=='':
        email=load_current_acc()
    fn=f'C:\\Users\\Caduceus\\Music\\codes\\{email+".json"}'
    with open(fn,'r+') as f:
        cont=load(f)
        f.seek(0)
        bmittl=len(cont['pacc_dtls']['tests']['BMI'])
        bpttl=len(cont['pacc_dtls']['tests']['BP'])
        return bmittl,bpttl
def get_bmi_records(itr,n): #6
    email=load_current_acc()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        bmi=cont['pacc_dtls']['tests']['BMI'] #2[[],[]]
        if bmi==[]:
            return 0
        else:
            return cont['pacc_dtls']['tests']['BMI'][itr][n]

def get_bp_records(itr,n): #6
    email=load_current_acc()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        bmi=cont['pacc_dtls']['tests']['BP'] #2[[],[]]
        if bmi==[]:
            return 0
        else:
            return cont['pacc_dtls']['tests']['BP'][itr][n]

def get_aboutdoc(email):
    with open(email+'.json','r+') as f:
        cont=load(f)
        #f.seek(0)
        about=cont['dacc_dtls']['dtls']['about_me']
        fee=cont['dacc_dtls']['dtls']['fee']
        return about,fee
# App start functions ---------------------
def save_current_acc(email):
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r+') as f:
        f.truncate()
        f.seek(0)
        sv_type=email
        f.writelines(sv_type)
def load_current_acc():
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r') as f:
        #cnt=eval(f.read())
        cnt=f.read()
        #cnt[0]=cnt[0]
        email=cnt
        return email
def clear_current_acc():
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r+') as f:
        f.truncate()
def check_last_user():
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r+') as f:
        email=f.readlines()
        #print(email)
        if email==[]:
            return 0
        else:
            return 1
def guest_login_options():
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r+') as f:
        f.truncate()
        f.seek(0)
        f.write('guest')
def reset_current_user():
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r+') as f:
        f.truncate()
        print('Current user cleared...')
def get_curr_user():
    with open(r'C:\Users\Caduceus\Music\codes\curr_user.txt','r+') as f:
        n=f.read()
       # print('EMAIL:',n)
        return n
def doc_add_dtls(email,n,qlf,exp,fee=0):
    with open('doctors_list.csv','a+',newline='') as f:
        cnt=[email,n,qlf,exp,fee]
        #add_fee_doc_list(email,fee)
        try:
            w=writer(f)
            w.writerow(cnt)
        except:
            print('File read!!')
def get_doctor(n):
    file='C:\\Users\\Caduceus\\Music\\codes\\doctors_list.csv'
    with open(file,'r',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        try:
            r=reader(f)
            lst=list(r)
        except:
            print('File read!!')
        return lst[n]
def get_total_doc():
    fn='C:\\Users\\Caduceus\\Music\\codes\\doctors_list.csv'
    with open(fn,'r+',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        try:
            l=0
            r=reader(f)
            for i in r:
                l+=1
        except:
            print('File read!!')
        return l
def get_doc_name(email):
    try:
        with open(email+'.json','r+') as f:
            cont=load(f)
            f.seek(0)
            n=cont['dacc_dtls']['dtls']['name']
            return n
    except:
        return 'Account deleted'
def get_all_active_appoin():
    email=load_current_acc()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        ls=cont['pacc_dtls']['appoin']
        nl=[]
        for x in ls:
            if x[3]=='confirmed-booking' or x[3]=='processing':
                nl.append(x)
        return nl
def get_all_active_appoin2():
    email=load_current_acc()
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        ls=cont['dacc_dtls']['dtls']['appoin']
        nl=[]
        for x in ls:
            if x[3]=='confirmed-booking' or x[3]=='processing':
                nl.append(x)
        return nl
def get_all_past_appoin2():
    email=load_current_acc()
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        ls=cont['dacc_dtls']['dtls']['appoin']
        nl=[]
        for x in ls:
            if x[3]=='appoinment---done':
                nl.append(x)
        return nl
def get_all_past_appoin():
    email=load_current_acc()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        ls=cont['pacc_dtls']['appoin']
        nl=[]
        for x in ls:
            if x[3]=='appoinment---done'or x[3]=='rejected--booking' or x[3]=='cancelled-booking':
                nl.append(x)
        return nl
def get_all_rejected_appoin2():
    email=load_current_acc()
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        ls=cont['dacc_dtls']['dtls']['appoin']
        nl=[]
        for x in ls:
            if x[3]=='rejected--booking' or x[3]=='cancelled-booking':
                nl.append(x)
        return nl
def update_doc_list(email,nn,nqlf,nexp,nfee):
    with open('doctors_list.csv','r+',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        email=get_curr_user()
        r=reader(f)
        w=writer(f)
        cnt=[]
        for x in r:
            cnt.append(x)
        f.seek(0)
        for a in cnt:
            if a!=[]:
                if a[0]==email:
                    a[1]=nn
                    a[2]=nqlf
                    a[3]=nexp
                    a[4]=nfee
        f.seek(0)
        w.writerows(cnt)
def delete_doc_list(email):
    with open('doctors_list.csv','r+',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        email=get_curr_user()
       # print('user:   ',email)
        r=reader(f)
        w=writer(f)
        cnt=[]
        for x in r:
            cnt.append(x)
        f.seek(0)
        #print(cnt)
        for a in cnt:
            if a!=[]:
                if a[0]==email:
                    cnt.remove(a)
        f.seek(0)
        w.writerows(cnt)
def add_fee_doc_list(email,fee):
    with open('doctors_list.csv','r+',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        r=reader(f)
        w=writer(f)
        f.seek(0)
        for i in r:
            if i[0]==email:
                curr=f.tell()
                i[4]=fee
                #print(f.tell())
                f.seek(curr)
                w.writerow(i)
        lst=list(r)
def add_fee_doclist(email,fee):
    with open('doctors_list.csv','r+',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        email=get_curr_user()
        r=reader(f)
        w=writer(f)
        cnt=[]
        for x in r:
            cnt.append(x)
        f.seek(0)
        for a in cnt:
            if a!=[]:
                if a[0]==email:
                    a[4]=fee
        f.seek(0)
        w.writerows(cnt)
        def xyz():
            for i in r:
                if i[0]==email:
                    curr=f.tell()
                    i[4]=fee
                    #print(i)
                    #print(f.tell())
                    f.seek(curr)
                    w.writerow(i)
            lst=list(r)
def indent_doc_list():
    with open('doctors_list.csv','r+',newline='\r\n') as f:
        #cnt=[email,n,qlf,exp,fee]
        try:
            r=reader(f)
            w=writer(f)
            for i in r:
                if i==[]:
                    pos=f.tell()
                    f.seek(pos)
        except:
            print('Error')
def save_appoin(e,d,t):
    e=str(e)
    d=str(d)
    t=str(t)
    email=get_curr_user()
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['pacc_dtls']['appoin']
        old.append([e,d,t,'processing'])
        dump(cont,f,indent=4)
def add_doc_appoin(e,d,t):
    email=get_curr_user()
    d=str(d)
    t=str(t)
    with open(e+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['dacc_dtls']['dtls']['appoin']
        old.append([email,d,t,'processing'])
        dump(cont,f,indent=4)
def cancel_appoin(e,d,t,s):
    e=str(e)
    d=str(d)
    t=str(t)
    email=get_curr_user()
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['pacc_dtls']['appoin']
        for i in old:
            if i[0]==e:
                if i[1]==d:
                    if i[2]==t:
                        i[3]='cancelled-booking'
        dump(cont,f,indent=4)
    with open(e+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['dacc_dtls']['dtls']['appoin']
        for i in old:
            if i[0]==email:
                if i[1]==d:
                    if i[2]==t:
                        i[3]='cancelled-booking'
        dump(cont,f,indent=4)
def change_appoin_status(e,d,t,nstatus):
    e=str(e)
    d=str(d)
    t=str(t)
   # print('Going inside...',e,d,t,nstatus)
    email=get_curr_user()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['dacc_dtls']['dtls']['appoin']
        for i in old:
            if i[0]==e:
                if i[1]==d:
                    if i[2]==t:
                        #print(i)
                        i[3]=nstatus
        dump(cont,f,indent=4)
    with open(e+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['pacc_dtls']['appoin']
        for i in old:
            if i[0]==email:
                if i[1]==d:
                    if i[2]==t:
                       # print(i)
                        i[3]=nstatus
        dump(cont,f,indent=4)
def add_emergency_con(amb,doc,home):
    email=get_curr_user()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        cont['pacc_dtls']['emerg']['ambulance']=amb
        cont['pacc_dtls']['emerg']['doctor']=doc
        cont['pacc_dtls']['emerg']['home']=home
        dump(cont,f,indent=4)
def get_emergency_con(n):
    email=get_curr_user()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        amb=cont['pacc_dtls']['emerg']['ambulance']
        doc=cont['pacc_dtls']['emerg']['doctor']
        home=cont['pacc_dtls']['emerg']['home']
        l=[amb,home,doc]
        return l[n]
def get_all_documents(email):
    email=get_curr_user()
    email=get_absolute_path(email)
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        x=cont['pacc_dtls']['documents']
        return x
def store_documents(file):
    email=f"C:\\Users\\Caduceus\\Music\\codes\\{get_curr_user()}"
    with open(email+'.json','r+') as f:
        cont=load(f)
        f.seek(0)
        old=cont['pacc_dtls']['documents']
        old.append(file)
        dump(cont,f,indent=4)
def get_absolute_path(file):
    return f"C:\\Users\\Caduceus\\Music\\codes\\{file}"
def delete_document(file):
    email=f"C:\\Users\\Caduceus\\Music\\codes\\{get_curr_user()}"
    os.remove(file)
    print('File removed succ...')
