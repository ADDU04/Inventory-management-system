from tkinter import *
from employee import employeeClass 
from supplier import supplierClass
from category import categoryClass
from Product import productClass
from salary import salaryClass
from sales import salesClass
from Return import ReturnClass
from attendance import attendanceClass
import sqlite3
from tkinter import messagebox
from PIL import Image,ImageTk
import os
import time
from pathlib import Path
class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x780+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        #Background image of dashboard
        self.bg1= ImageTk.PhotoImage(file="images/bg6.jpg")
        bg1 = Label(self.root, image=self.bg1).place(x=0, y=0, relwidth=1, relheight=1)
        #Small icon at top
        self.icon_title=PhotoImage(file="Images/icon2-modified.png")
        #=====title======
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",35),bg="#033054",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)  
        #===Button Logout====
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",18),bg="yellow",cursor="hand2").place(x=1400,y=15,height=40,width=100)        
        #===Time & heading 2====
        self.lbl_clock=Label(self.root,text="Welcome To Inventory Management System!\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #====Left Menu Frame===
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=100,width=295,height=680)  
        #Image of menu
        self.MenuLogo=Image.open("Images/logo.png")
        self.MenuLogo=self.MenuLogo.resize((135,135),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X) 
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20,"bold"),bg="gray25",fg="white").pack(side=TOP,fill=X)
        #Buttons 
        btn_employee=Button(LeftMenu,text="Employee Details",command=self.employee,font=("times New Roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier Details",command=self.supplier,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category Details",command=self.category,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product Details",command=self.product,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Bill Details",command=self.sales,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_salary=Button(LeftMenu,text="Salary",command=self.salary,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_attendance=Button(LeftMenu,text="Review To Attendance",command=self.attendance,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_return=Button(LeftMenu,text="Manage Return Products",command=self.return_product,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_order=Button(LeftMenu,text="Review To Total Sales",command=self.order,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",command=self.exit,font=("times new roman",18,"bold"),bg="royal blue",fg="white",cursor="hand2",anchor="w",bd=3,relief=RAISED).pack(side=TOP,fill=X)
        #===Content in main window===
        self.lbl_employee=Label(self.root,text="Total Employee \n [0]",bd=5,relief=RIDGE,bg="#1E90FF",fg="white",font=("goudy old style",20))
        self.lbl_employee.place(x=340,y=100,height=100,width=215)
        self.lbl_supplier=Label(self.root,text="Total Suppliers \n [0]",bd=5,relief=RIDGE,bg="#FF6700",fg="white",font=("goudy old style",20))
        self.lbl_supplier.place(x=790,y=100,height=100,width=215)
        self.lbl_category=Label(self.root,text="Total Category \n [0]",bd=5,relief=RIDGE,bg="#097969",fg="white",font=("goudy old style",20))
        self.lbl_category.place(x=565,y=100,height=100,width=215)
        self.lbl_product=Label(self.root,text="Total Products \n [0]",bd=5,relief=RIDGE,bg="#f5c71a",fg="white",font=("goudy old style",20))
        self.lbl_product.place(x=1015,y=100,height=100,width=215)
        self.lbl_sales=Label(self.root,text="Total Sales \n [0]",bd=5,relief=RIDGE,bg="#483D8B",fg="white",font=("goudy old style",20))
        self.lbl_sales.place(x=1240,y=100,height=100,width=215)
        #===Footer===
        lbl_footer=Label(self.root,text="IMS-Inventory Management System\nFor Any Technical Issue Contact:8551080719",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)        
        #Calling function for total employee,suppliers,category,product,sales
        self.update_content()    
    #Employee Window
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    #Supplier Window
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    #Category Window
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    #Product Window
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)    
    #Salary window
    def salary(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salaryClass(self.new_win)           
    #Sales Window
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win) 
    #Return product window
    def return_product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ReturnClass(self.new_win)
    #Attendance window
    def attendance(self):
       os.system('python rev_attendance.py')     
    #Total sales excel sheet
    def order(self):
        absolutePath = Path('C:/Users/Neha/Desktop/Project/Inventory/Order.xlsx').resolve()
        os.system(f'start excel.exe "{absolutePath}"')  
    #Exit function
    def exit(self):
        wayOut =messagebox.askyesno("Exit", "Do you want to exit from the system",parent=self.root)
        if wayOut > 0:
            self.root.destroy()
    #Function for update content in main window
    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Products \n [{str(len(product))}]')
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers \n [{str(len(supplier))}]')
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Category \n [{str(len(category))}]')
            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee \n [{str(len(employee))}]')      
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n [{str(bill)}]')       
            #time & date
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
    #Logout function
    def logout(self):
        wayOut =messagebox.askyesno("Logout", "Do you want to logout from the system",parent=self.root)
        if wayOut > 0:
            self.root.destroy()
            os.system("python employee_login.py")  
if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()
