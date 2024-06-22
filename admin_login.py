from tkinter import*
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
from PIL import Image,ImageTk
class Login_System:

    def __init__(self,root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1520x780+0+0")
        self.root.config(bg="#856ff8")

        #Declaring otp variable
        self.otp=''

        #Background image for login window
        self.bg1= ImageTk.PhotoImage(file="images/bg1.jpg")
        bg1 = Label(self.root, image=self.bg1).place(x=0, y=0, relwidth=1, relheight=1)
        
        #Small icon for login window
        self.icon_title=PhotoImage(file="Images/user3.png")
        self.icon_title2=PhotoImage(file="Images/user2.png")

         #===Time,Date & Heading====
        self.lbl_clock=Label(self.root,text="Welcome Back!\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",image=self.icon_title2,compound=LEFT,font=("times new roman",15,"bold"),bg="#add1f4")
        self.lbl_clock.place(x=0,y=0,relwidth=1,height=30)

        #Login Frame
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="#add1f4")
        login_frame.place(x=500,y=170,width=350,height=460)

        #Declaring variable
        self.admin_id=StringVar()
        self.password=StringVar()
        
        #Title of login frame
        title=Label(login_frame,text="Login System",image=self.icon_title,compound=LEFT,font=("Elephant",30,"bold"),bg="#add1f4").place(x=0,y=30,relwidth=1)
        
        #content of login frame
        lbl_employee_id=Label(login_frame,text="Admin ID",font=("Andalus",15,"bold"),bg="#add1f4").place(x=50,y=100)
        txt_employee_id=Entry(login_frame,textvariable=self.admin_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250,height=30)

        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15,"bold"),bg="#add1f4").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show='*',font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250,height=30)
        
        #Login button
        btn_login=Button(login_frame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="#0F52BA",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)
        
        #horizontal line
        hr=Label(login_frame,bg="black").place(x=50,y=370,width=250,height=2) 
        or_=Label(login_frame,text="OR",bg="white",font=("times new roman",15,"bold")).place(x=150,y=355)  

        #Forget password button    
        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",14,"bold"),bg="#add1f4",fg="black",bd=0,activebackground="white",activeforeground="#00759E",cursor="hand2").place(x=100,y=390)
        
        #Call the update date & time function
        self.update_date_time()

    #Login button function 
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.admin_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.admin_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid USERNAME/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        messagebox.showinfo("Success","Login Successful",parent=self.root)
                        self.root.destroy()
                        os.system("python admin_dashboard.py")
                    else:
                        messagebox.showerror("Error","Please Check Your Credentials",parent=self.root)  
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 

    #Forget Password Button Function
    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.admin_id.get()=="":
                messagebox.showerror("Error","Employee Id Must Be Required",parent=self.root) 
            else:
                cur.execute("select email from employee where eid=? ",(self.admin_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID,Try Again",parent=self.root) 
                else:
                    #Forget Window
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send_email_function() 
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error,Try Again",parent=self.root)
                    else:
                        #Forget Window
                        self.forget_win=Toplevel(self.root) 
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')  
                        self.forget_win.focus_force()
                        
                        #Title of forget password window
                        title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg='#3f51b5',fg="white").pack(side=TOP,fill=X)    
                        lbl_reset=Label(self.forget_win,text="Enter OTP Sent On Registered Email",font=("times new roman",15)).place(x=20,y=60)                      
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        #Reset password or OTP submit button
                        self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)                      
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)                      
                        txt_c_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)
                        
                        #Update password button
                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Update Password Button Function
    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password Is Required",parent=self.forget_win) 
        elif self.var_new_pass.get()!=  self.var_conf_pass.get():
             messagebox.showerror("Error","New Password & Confirm Password Should Be Same",parent=self.forget_win) 
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.admin_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password Updated Successfully",parent=self.forget_win)
                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
    
       
    #Reset button function
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP,Try Again",parent=self.forget_win)    

    #Forget window function for otp 
    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_
        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f' 

    #update Time & date function
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome Back!\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

if __name__=="__main__":
    root=Tk()
    obj=Login_System(root)
    root.mainloop()   

        
