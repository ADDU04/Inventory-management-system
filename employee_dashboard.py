from tkinter import *
import razorpay
from tkinter import messagebox
from Bill import BillClass
import os
import time
import webbrowser
from PIL import ImageTk,Image
class pay:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x780+0+0")
        self.root.title("Billing Management System")
        self.root.config(bg="white")
        #Background image of employee dashboard
        self.bg1= ImageTk.PhotoImage(file="images/bg5.jpg")
        bg1 = Label(self.root, image=self.bg1).place(x=0, y=0, relwidth=1, relheight=1)
        #Title of dashboard window
        title=Label(self.root,text="Customer Bill Management System",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        self.lbl_clock=Label(self.root,text="Welcome Back!\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15,"bold"),bg="#add1f4")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #Buttons
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",18,"bold"),bg="yellow",cursor="hand2").place(x=1190,y=10,height=50,width=150)
        btn_exit=Button(self.root,text="Exit",command=self.exit,font=("times new roman",18,"bold"),bg="yellow",cursor="hand2").place(x=1350,y=10,height=50,width=150)
        btn_bill=Button(self.root,text="Generate Bill",command=self.billing,font=("times new roman",20,"bold"),bg="#0F52BA",fg="white",cursor="hand2",anchor="w").place(x=700,y=150)
        btn_order=Button(self.root,text="Online Payment",command=self.pay,font=("times new roman",20,"bold"),bg="#097969",fg="white",cursor="hand2",anchor="w").place(x=1200,y=150)
        btn_attendance=Button(self.root,text="Attendance",command=self.attendance,font=("times new roman",20,"bold"),bg="#f44336",fg="white",cursor="hand2",anchor="w").place(x=170,y=150)
        #Images
        self.im=Image.open("Images/razor.jpg")
        self.im=self.im.resize((340,340),Image.ANTIALIAS)
        self.im=ImageTk.PhotoImage(self.im)
        self.lbl_im=Label(self.root,image=self.im,bd=3,relief=RAISED)
        self.lbl_im.place(x=1150,y=225)
        self.im2=Image.open("Images/face.jpg")
        self.im2=self.im2.resize((340,340),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=3,relief=RAISED)
        self.lbl_im2.place(x=100,y=225)
        self.im3=Image.open("Images/receipt.jpg")
        self.im3=self.im3.resize((340,340),Image.ANTIALIAS)
        self.im3=ImageTk.PhotoImage(self.im3)
        self.lbl_im3=Label(self.root,image=self.im3,bd=3,relief=RAISED)
        self.lbl_im3.place(x=620,y=225)
        #Footer
        lbl_footer=Label(self.root,text="IMS-Inventory Management System\nFor Any Technical Issue Contact:8551080719",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        #Calling update date & time function
        self.update_date_time()    
    #Bill window
    def billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=BillClass(self.new_win)  
    #Online payment window
    def pay(self):
        f=open('online_payment.html','r')
        webbrowser.open_new_tab('online_payment.html')
    def attendance(self):
       os.system('python main.py')    
    #Update date & time function
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome Back!\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)  
    #Logout function
    def logout(self):
        wayOut =messagebox.askyesno("Logout", "Do you want to logout from the system",parent=self.root)
        if wayOut > 0:
            self.root.destroy()
            os.system("python employee_login.py")   
    #Exit function
    def exit(self):
        wayOut =messagebox.askyesno("Exit", "Do you want to exit the system",parent=self.root)
        if wayOut > 0:
            self.root.destroy()
if __name__=="__main__":
    root=Tk()
    obj=pay(root)
    root.mainloop()        
