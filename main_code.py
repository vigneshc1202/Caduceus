# ************************IMPORTS*************************
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.imagelist import MDSmartTile
#from kivymd.uix.picker import MDThemePicker
#from kivy.uix.button import MDRaisedButton
from kivy.properties import NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.list import OneLineListItem
from kivy.properties import ListProperty
from kivymd.uix.datatables import MDDataTable
from kivy.properties import ObjectProperty
from kivy_garden.mapview import MapView
from kivy.app import App
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
import webbrowser
from kivy.core.clipboard import Clipboard
import app_func as APP
from plyer import filechooser
from kivymd.uix.pickers import MDDatePicker,MDTimePicker
import os
from time import *
import datetime
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarActionButton,MDSnackbarCloseButton
Window.clearcolor = (0, 0.6, 0.1, 1.0)
Window.size = (400, 625)
user_email = ''
doc_selected=''
#user_email=APP.load_current_acc()
class LoadingScreen(Screen):
    pass
class AppTourScreen(Screen):
    pass
class PAccountPage(Screen):
    def on_entr(self):
        DisplayDataCard.update(self,type='p')
    def get_home_screen_text_input(self):
        p_screen = self.manager.get_screen('p_screen')
        self.ids.p_name_.text = p_screen.ids.p_name.text
    def update(self):
        name= self.ids.name.text
        age= self.ids.age.text
        phn= self.ids.phn.text
        addr= self.ids.addr.text
class HomeScreen(Screen):
    pass
class AppoinShowCard(MDCard):
    def cancelapp(self,e,dt,s):
        date,time=dt.split('  ')
        if s=='processing':
            APP.cancel_appoin(e,date,time,s)
            print('Appoinment cancelled!!')
            toast('Appoinment cancelled!!')
        else:
            toast('Unable to cancel the appoinment!')
    def show_docdtls(self,e):
       # print(e)
        n,ph,age,addr,qlf,exp=APP.get_ddtls(e)
        Clipboard.copy(f'Name:{n},Ph no.:{ph},Age:{age},Addr:{addr},Qlf:{qlf}')
        toast("Doctor's details copied to the clipboard!" )
class AboutUsBox(MDBoxLayout):
    pass
class DSettingsBox(MDBoxLayout):
    def getvalues(self):
        user_email=APP.get_curr_user()
        f,about=APP.get_ddtls2(user_email)
        self.ids.fee_change.text=f
        self.ids.about_me.text=about
    def save_doc_dtls(self):
        fee=self.ids.fee_change.text
        about=self.ids.about_me.text
        if fee!='' or about!='':
            APP.load_ddtls2(user_email,fee,about,0)
            toast('Data saved!!')
        else:
            print('Enter all values!')
    def logout_user(self,n):
        MainApp.redt(self,screen='select')
        APP.reset_current_user()
        user_email=''
        toast('User logged out successfully!!')
class DisplayDataCard(MDCard):
    global edit_value
    edit = False
    edit_value=False
    def refresh(self,type):
        pass
    def change(self,tf):
        if tf==True:
            edit_value=True
    global user_email
    user_email=APP.load_current_acc()
    def getvalues(self,type):
        if type=='p':
            n,ph,age,addr=APP.get_pdtls(user_email)
            n=str(n)
            age=str(age)
            ph=str(ph)
            addr=str(addr)
            self.ids.name.text=n
            self.ids.age.text=age
            self.ids.phn.text=ph
            self.ids.addr.text=addr
        elif type=='d':
            n,ph,age,addr,qlf,exp=APP.get_ddtls(user_email)
            n=str(n)
            age=str(age)
            ph=str(ph)
            addr=str(addr)
            qlf=str(qlf)
            exp=str(exp)
            self.ids.name.text=n
            self.ids.age.text=age
            self.ids.phn.text=ph
            self.ids.addr.text=addr
            self.ids.qlf.text=qlf
            self.ids.exp.text=exp
        else:
            print('ERROR')
    def update(self,type):
        if type=='p':
            n=self.ids.name.text
            age=self.ids.age.text
            ph=self.ids.phn.text
            addr=self.ids.addr.text
            email=APP.load_current_acc()
            APP.load_pdtls(email,n,ph,age,addr)
        else:
            n=self.ids.name.text
            age=self.ids.age.text
            ph=self.ids.phn.text
            addr=self.ids.addr.text
            qlf=self.ids.qlf.text
            exp=self.ids.exp.text
            email=APP.load_current_acc()  
            APP.load_ddtls(email,n,ph,age,addr,qlf,exp)
    def check(self):
        if edit_value==True:
            return 1
        else:
            return 0
    def editt(self,type):
        edit_value=True
    def edit_pressed(self,type):
        if type=='p':
            MainApp.redt(self,screen='p_screen')
        else:
            MainApp.redt(self,screen='d_screen')

class GetDataCard(MDCard):
    def check(self,type):
        email=APP.load_current_acc()
        name= self.ids.name.text
        age= self.ids.age.text
        phn= self.ids.phn.text
        addr= self.ids.addr.text
        if type=='p':
            if name!='' and age!='' and phn!='' and addr!='':
                APP.load_pdtls(email,name,phn,age,addr)
                MainApp.redt(self,screen='main.py')
            else:
                toast('Please enter all details!')
        else:
            qlf=self.ids.qlf.text
            exp=self.ids.exp.text
            if name!='' and age!='' and phn!='' and addr!='' and qlf!='' and exp!='':
                APP.load_ddtls(email,name,phn,age,addr,qlf,exp)
                MainApp.redt(self,screen='d_screen2')
            else:
                toast('Please enter all details!')
class DMainScreen(Screen):
    def on_enter(self):
        self.active_appoin()
        self.past_appoin()
        self.rejected_appoin()
    def on_leave(self):
        self.clear_before_leaving()
    def reload_all(self):
        self.getname_email()
        self.on_leave()
        self.on_enter()
        toast('Page refreshed!')
    def getname_email(self):
        email=APP.get_curr_user()
        n,age,phn,addr,qlf,exp=APP.get_ddtls(email)
        self.ids.getname.text='Welcome, '+n
        self.ids.getemail.text='Hello, '+email
    def clear_before_leaving(self):
        alldoc = self.ids.active_listt
        alldoc.clear_widgets()
        pdoc = self.ids.past_listt
        pdoc.clear_widgets()
        rdoc = self.ids.rejected_listt
        rdoc.clear_widgets()
    def active_appoin(self):
        card = self.ids.active_listt
        for i in APP.get_all_active_appoin2():
            if APP.get_all_active_appoin2()==[]:
                continue
            else:
                email,date,time,status=i[0],i[1],i[2],i[3]
               # print(status)
                n,ph,age,addr=APP.get_pdtls(email)
                card_widget =AppoinCheckCard()
                card_widget.ids.pname.text = 'Name: '+n
                card_widget.ids.app_datetime2.text = f'{date}  {time}'
                card_widget.ids.statuss.text = i[3]
                card_widget.ids.emaill.text =email
                card.add_widget(card_widget)
    def past_appoin(self):
        card = self.ids.past_listt
        for i in APP.get_all_past_appoin2():
            if APP.get_all_past_appoin2()==[]:
                continue
            else:
                print(i,'past')
                email,date,time,status=i[0],i[1],i[2],i[3]
                n,ph,age,addr=APP.get_pdtls(email)
                card_widget =AppoinCheckCard()
                card_widget.ids.pname.text = 'Name: '+n
                card_widget.ids.app_datetime2.text = f'{date}  {time}'
                card_widget.ids.statuss.text = status
                card_widget.ids.emaill.text =email
                card.add_widget(card_widget)
    def rejected_appoin(self):
        card = self.ids.rejected_listt
        for i in APP.get_all_rejected_appoin2():
            if APP.get_all_rejected_appoin2()==[]:
                continue
            else:
                email,date,time,status=i[0],i[1],i[2],i[3]
                n,ph,age,addr=APP.get_pdtls(email)
                card_widget =AppoinCheckCard()
                card_widget.ids.pname.text = 'Name: '+n
                card_widget.ids.app_datetime2.text = f'{date}  {time}'
                card_widget.ids.statuss.text = status
                card_widget.ids.emaill.text =email
                card.add_widget(card_widget)
class MAINScreen(Screen):
    global iter
    iter=0
    def on_enter(self):
        self.values()
        self.load_table()
        self.active_appoin()
        self.past_cancel_appoin()
        self.getname_email()
        self.get_documents()
    def on_leave(self, *args):
        self.clear_before_leaving()
    def reload_all(self):
        self.getname_email()
        self.on_leave()
        self.on_enter()
        toast('Page refreshed!')
    def logout_user(self):
        app=MDApp.get_running_app()
        APP.clear_current_acc()
        global user_email
        user_email=''
        app.redt('select')
    def values(self):
        card = self.ids.doc_list
        for i in range(APP.get_total_doc()):
            if APP.get_doctor(i)==[]:
                continue
            else:
                email,n,qlf,exp,fee=APP.get_doctor(i)
                card_widget = DocShowCard()
                card_widget.ids.name.text = '  '+n
                card_widget.ids.qlf.text = qlf
                card_widget.ids.exp.text = exp+'years of exp.'
                card_widget.ids.fee.text = 'Rs. '+fee
                card_widget.ids.email.text = email
                card.add_widget(card_widget)
    def clear_before_leaving(self):
        alldoc = self.ids.doc_list
        alldoc.clear_widgets()
        active = self.ids.active_list
        active.clear_widgets()
        past=self.ids.past_cancel_list
        past.clear_widgets()
        records = self.ids.record_list
        records.clear_widgets()
        docs=self.ids.document_list
        docs.clear_widgets()
    def active_appoin(self):
        card = self.ids.active_list
        for i in APP.get_all_active_appoin():
            if APP.get_all_active_appoin()==[]:
                continue
            else:
                email,date,time,status=i[0],i[1],i[2],i[3]
                fee,ab=APP.get_ddtls2(email)
                card_widget =AppoinShowCard()
                card_widget.ids.dname.text = '  '+APP.get_doc_name(email)
                card_widget.ids.app_datetime.text = f'{date}  {time}'
                card_widget.ids.status.text = status
                card_widget.ids.fee.text ='FEE: Rs.'+fee
                card_widget.ids.emailid.text = email
                card.add_widget(card_widget)
    def past_cancel_appoin(self):
        card = self.ids.past_cancel_list
        for i in APP.get_all_past_appoin():
            if APP.get_all_past_appoin()==[]:
                continue
            else:
                email,date,time,status=i[0],i[1],i[2],i[3]
                fee,ab=APP.get_ddtls2(email)
                card_widget =AppoinShowCard()
                card_widget.ids.dname.text = '  '+APP.get_doc_name(email)
                card_widget.ids.app_datetime.text = f'ON: {date}  {time}'
                card_widget.ids.status.text = 'STATUS: '+status
                card_widget.ids.fee.text ='FEE: Rs.'+fee
                card_widget.ids.emailid.text = email
                card.add_widget(card_widget)
    def get_documents(self):
        card = self.ids.document_list
        for i in APP.get_all_documents(user_email):
            if APP.get_all_documents(user_email)==[]:
                continue
            else:
                if os.path.exists(i):
                    card_widget =TileView(icon=i,icon2='delete-empty')
                    if i:
                        card.add_widget(card_widget)
    def getname_email(self):
        email=APP.get_curr_user()
        n,age,phn,addr=APP.get_pdtls(email)
        self.ids.getname.text='Welcome, '+n
        self.ids.getemail.text='Hello, '+email
    def add_document(self):
        filters = ['*.jpg', '*.png']
        path= filechooser.open_file(filters=filters)
        for i in path:
            APP.store_documents(file=i)
            print('Document added successfully!!')
        toast('Image uploaded successfully!')
    def load_table(self):
        record_page = self.ids.record_list
        bmittl,bpttl=APP.get_total_records(user_email)
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.8, 0.1),
            size= [dp(100) ,dp(100)],
            use_pagination=True,
            column_data=[
                ("Date", dp(30)),
                ("Test Type", dp(30)),
                ("Result", dp(30)),
                ("Comment", dp(30))],
            row_data=[
                (APP.get_bmi_records(i,0),'Body Mass Index',APP.get_bmi_records(i,1),APP.get_bmi_records(i,2)) for i in range(bmittl)],
            sorted_order="DSC")
        #self.add_widget(self.data_tables)
        self.data_bp_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.8, 0.1),
            size= [dp(100) ,dp(100)],
            use_pagination=True,
            column_data=[
                ("Date", dp(30)),
                ("Test Type", dp(30)),
                ("Result", dp(30)),
                ("Comment", dp(30))],
            row_data=[
                (APP.get_bp_records(i,0),'Blood Pressure',APP.get_bp_records(i,1),APP.get_bp_records(i,2)) for i in range(bpttl)],
            sorted_order="DSC")
        record_page.add_widget(self.data_tables)
        record_page.add_widget(self.data_bp_tables)
class UserInfoScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class SelectionScreen(Screen):
    pass
class PatientScreen(Screen):
    def get_screen(self, screen):
        self.current = screen
class DoctorScreen(Screen):
    def get_screen(self, screen):
        self.current = screen
class HelpScreen(Screen):
    pass
class DAccountPage(Screen):
    pass
class Tab(MDFloatLayout,MDTabsBase):
    pass
class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
class DContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
class RootWidget(ScreenManager):
    pass
class GetDataCard2(MDCard):
    def check(self,type):
        email=APP.load_current_acc()
        if type=='d2':
            fee=self.ids.fee.text
            about_me=self.ids.about_me.text
            if fee!='' and about_me!='':
                APP.load_ddtls2(email,fee,about_me,1)
                MainApp.redt(self,screen='doctor.py')
            else:
                toast('Please enter all details!')

class DoctorScreen2(Screen):
    pass
class DocShowCard(MDCard):
    global doc_selected
    def __init__(self, **kwargs):
        super(DocShowCard, self).__init__(**kwargs)
        self.size_hint=None,None
        self.size_hint_y = None
    def runnn():
        t=AppoinBox.time_
        d=AppoinBox.date
        email=''
        print(email,t,d)
    def show_appoin(self,name):
        self.dialog=MDDialog(
            title='Book your Appoinment',
            type='custom',
            content_cls=AppoinBox(),
            radius=[20, 7, 20, 7]
            )
        self.dialog.open()
    def appoin(self,name,email):
        global doc_selected
        doc_selected=email
        self.show_appoin(name)
class MyDialog(MDDialog):
    pass
class TileView(MDSmartTile):
    def delete_file(self,path):
        APP.delete_document(path)
        toast('Image deleted successfully!')
class AppoinCheckCard(MDCard):
    def confirm_appoin(self,e,dt,status):
        n=dt.split('  ')
        d,t=n[0],n[1]
        APP.change_appoin_status(e,d,t,'confirmed-booking')
        toast('Status changed!!')
    def reject_appoin(self,e,dt,status):
        n=dt.split('  ')
        d,t=n[0],n[1]
        APP.change_appoin_status(e,d,t,'rejected--booking')
        toast('Appoinment rejected!!')
    def appoin_done(self,e,dt,status):
        n=dt.split('  ')
        d,t=n[0],n[1]
        if status=='confirmed-booking':
            APP.change_appoin_status(e,d,t,'appoinment---done')
            toast('Appoinment finished!!')
        else:
            toast('Error-Unable to change the status!!')
    def show_pdtls(self,email):
        n,ph,age,addr=APP.get_pdtls(email)
        Clipboard.copy(f'Name:{n},Phone no.:{ph},Address:{addr},Age:{age}')
        toast('Patient info copied to your clipboard!')
class SettingsBox(MDBoxLayout):
    def save_emergency(self):
        amb=self.ids.amb_no.text
        doc=self.ids.doc_no.text
        home=self.ids.home_no.text
        if amb!='' and doc!='' and home!='':
            APP.add_emergency_con(amb,doc,home)
        else:
            toast('Enter all values!!')
    def logout_user(self,n):
        MainApp.redt(self,screen='select')
        APP.reset_current_user()
        toast('User logged out successfully!!')
class AppoinBox(MDBoxLayout):
    time_=''
    date=''
    def reload(self):
        self.ids.time_choosed.text=str('Appoinment at '+str(self.time_))
        self.ids.date_choosed.text=str('Appoinment on '+str(self.date))
    def on_save(self, instance, value, date_range):
        self.date=value
    def get_time(self, instance, time):
        self.time_=time
        return time
    def calender(self):
        date_dialog = MDDatePicker(title='Select Date',
                                    min_date=datetime.date.today(),
                                    max_date=datetime.date(
                                        datetime.date.today().year+1,
                                        datetime.date.today().month,
                                        datetime.date.today().day ,))
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
    def on_cancel(self):
        self.date_dialog.close()
        toast('DATE/TIME Selected!')
    def time(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    def get_aboutdoc(self):
        email=doc_selected
        doc=APP.get_aboutdoc(email)
    def book_appoin(self):
        t=self.time_
        d=self.date
        e=doc_selected
        toast('Your appoinment has been booked!')
        APP.save_appoin(e,d,t)
        APP.add_doc_appoin(e,d,t)
class P_login_Screen(Screen):
    pass
class D_login_Screen(Screen):
    pass
class SampCard(MDCard):
    def redirect(self,screen):
        self.root.current= screen
    def close_dia(self):
        self.dialog_bmi.dismiss
    def show_dialog_bmi(self,bmi_result,bmi):
        self.dialog_bmi=MDDialog(
            title='Your Result',
            type='simple',
            text=f'BMI :{bmi}\n{bmi_result}',
            buttons=[MDFlatButton(text='Save')],
            radius=[20, 7, 20, 7]
            )
        self.dialog_bmi.open()
    def show_dialog_bp(self,bp_result):
        self.dialog_bp=MDDialog(
            title='Your Result',
            type='simple',
            text=f'{bp_result}',
            buttons=[MDFlatButton(text='Save')],
            radius=[20, 7, 20, 7]
            )
        self.dialog_bp.open()
        toast('Your report is saved!')
    def clear_value(self):
        self.ids.tb1.text=''
        self.ids.tb2.text=''
    def msg(self):
        toast('Your data is saved!!')
    def check(self,type):
        box1= self.ids.tb1.text
        box2= self.ids.tb2.text
        print(box1,box2)
        if box1!='' and box2!='':
            if type=='bmi':
                result,bmi=APP.bmi_check(box1,box2)
                SampCard.show_dialog_bmi(self,bmi_result=result,bmi=bmi)
                print(user_email)
                APP.bmi_save(user_email,bmi,result)
            if type=='bp':
                result=APP.bp_check(box1,box2)
                print(result)
                APP.bp_save(user_email,box1,box2,result)
                SampCard.show_dialog_bp(self,bp_result=result)

        else:
            toast('Please enter values!!')

class LoginCard(MDCard):
    app=MDApp.get_running_app()
    def redirect(scr):
        app=MDApp.get_running_app()
        app.root.current=scr 
    def process(self,screen_name):
        email= self.ids.emailid.text
        passw = self.ids.passwd.text
        print(email,passw)
        if email!='' and passw!='':
            if screen_name=='p_login_screen':
                output = APP.exist(email,passw,screen_name)
                print('output',output)
                if output==0:
                    LoginCard.redirect('p_screen')
                else:
                    toast('User already exist!! Signin now')
                    LoginCard.redirect('login_screen')
            elif screen_name=='d_login_screen':
                output = APP.exist(email,passw,screen_name)
                if output==0:
                    LoginCard.redirect('d_screen')
                else:
                    toast('User already exist!! Signin now')
                    LoginCard.redirect('login_screen')
            elif screen_name=='login_screen':
                #check = APP.exist(email,passw,screen_name)
                c= APP.check_exist(email)
                if c==0:
                    toast('User not found!!')
                    LoginCard.redirect('home_screen')
                elif c==1:
                    output = APP.clogin(email,passw)
                    if output==1:
                        LoginCard.redirect(APP.cuser_type(email))
                    else:
                        toast('Wrong email or password')

        else:
            toast('Please enter the details!') 
class MyCard(MDCard):
    def fechar(self):
        self.parent.remove_widget(self)
class ListWidget(OneLineAvatarIconListItem):
    pass
decimal = 2
class MainApp(MDApp):
    root_widget = RootWidget()
    def on_start(self):
        global user_email 
        if APP.check_last_user()==0:
            MainApp.redt(self,screen='select')
        else:
            user_email = APP.load_current_acc()
            print('Current user:',user_email)
            if APP.login_cnt_check(user_email)==0:
                toast('Login Expired!!')
                APP.reset_login_cnt(user_email)
                user_email=''
                MainApp.redt(self,screen='select')
            else:
                APP.login_cnt_inc(user_email)
                MainApp.redt(self,screen=APP.cuser_type(user_email))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #rv_data = ListProperty()

    #def update_data(self, rv_data_list):
       # self.rv_data = [{'text': item} for item in rv_data_list]
        #print(self.rv_data, 'update')
    dialog_bmi=None
    dialog_bp=None
    def build(self):
        #Clock.schedule_once(self.redirectt,4)
        self.root_widget = RootWidget()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "700"
        self.title = "Caduceus"
        self.icon='logo1.png'
        Builder.load_file('main_code.kv')
        self.data = {
            'Ambulance': [
                'ambulance',
                    "on_press", lambda x: webbrowser.open(f'tel:{APP.get_emergency_con(0)}'),
                    "on_release", lambda x :toast(f'Calling Ambulance:{APP.get_emergency_con(0)}')
                ],
            'Home': [
                'home',
                "on_press", lambda x: webbrowser.open(f'tel:{APP.get_emergency_con(1)}') ,
                "on_release", lambda x:toast(f'Calling Home:{APP.get_emergency_con(1)}')
            ],
            'Doctor': [
                'doctor',
                    "on_press", lambda x: webbrowser.open(f'tel:{APP.get_emergency_con(2)}'),
                    "on_release", lambda x:toast(f'Calling Doctor:{APP.get_emergency_con(2)}')
                ],
        }
        return RootWidget(transition=FadeTransition())
    def redirectt(self,*args):
        MainApp.redt(self,screen='select')
    def redt(self,screen):
        app=MDApp.get_running_app()
        app.root.current= screen
    def press(self):
        app=MDApp.get_running_app()
        screen = self.root.get_screen('p_screen').ids.p_name.text
        print(screen)
        #test()
        #MDApp.get_running_app().root.ids.paccount_screen.ids.p_name_.text = client_name
        self.root.get_screen('paccount_screen').ids.p_name_.text=screen
        #app.root.current=screen
    def get_screen(self, screen):
        self.current = screen
    def set_screen(self,screen1):
        MDApp.get_running_app().root.current = screen1
    def sh(self):
        print("Its working!!! ------------------------")
    def process(self,sname):
        sn=str(sname)
        print(sn)
        try:
            passwd=0
            emailid= self.root_widget.get_screen(sn).ids.emailid.text
            print("Email:", emailid)
            print("Password:", passwd)
            APP.exist(emailid,passwd)
        except Exception as e:
            print("Error:", str(e))
    def notify(self,msg):
        toast(msg)
    def logout_user(self,n):
        self.redt('select')
        APP.reset_current_user()
        toast('User logged out successfully!!')
    def delete_user(self,n):
        toast('Deleting account!')
        global user_email
        #APP.delete_doc_list(user_email)
        user_email=APP.get_curr_user()
        os.remove(user_email+'.json')
        MainApp.logout_user()
    def guest_logged(self):
        APP.save_current_acc('guest')
    def update_items(self):
        print('updated!!')
        MAINScreen.values(self)
    def change_theme(self):
        self.theme_cls.primary_palette = "Cyan" if  self.theme_cls.primary_palette == "Teal" else 'Teal'
    def logout_user():
        app=MDApp.get_running_app()
        APP.reset_current_user()
        APP.clear_current_acc()
        app.redt('select')
    def msg(self,m):
        toast(m)

if __name__ == "__main__":
    #try:
    MainApp().run()
    #except:
       # print('An error occured!!')
       ## sleep(2)
       # exit()
