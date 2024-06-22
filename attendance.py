from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time
class attendanceClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Attendance System")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(0,0)
        
        #Declaring Time variable
        self.TimeOfAttend = StringVar()

        #Value set for time variable
        self.TimeOfAttend.set(time.strftime("%I:%M:%S"))

        #Declaring Date variable
        self.DateOfAttend = StringVar()

        #Value set for date variable
        self.DateOfAttend.set(time.strftime("%d/%m/%Y"))
        
        #Declaring variables
        self.var_aid=StringVar()
        self.var_empid=StringVar()
        self.var_name=StringVar()
        self.var_status=StringVar()
        self.empid_list=[]
        self.name_list=[]

        #calling function for fetch empid
        self.fetch_empid()
        
        #===Time & heading====
        self.lbl_clock=Label(self.root,text="Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15,"bold"),bg="#add1f4")
        self.lbl_clock.place(x=0,y=0,relwidth=1,height=30)

        #Attendance frame
        attendance_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        attendance_Frame.place(x=10,y=35,width=400,height=300)

        #Title of attendance frame
        title=Label(attendance_Frame,text="Manage Attendance Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        
        #Content of attendance frame
        lbl_empId=Label(attendance_Frame,text="Emp Id",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_empname=Label(attendance_Frame,text="Emp Name",font=("goudy old style",18),bg="white").place(x=30,y=140)
        lbl_status=Label(attendance_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=185)
        cmb_eid=ttk.Combobox(attendance_Frame,textvariable=self.var_empid,values=self.empid_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_eid.place(x=150,y=60,width=200)
        cmb_eid.current(0)
         
        #Fetch name button
        btn_fetchname=Button(attendance_Frame,text="Show employee name",command=self.fetch_name,font=("goudy old style",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=150,y=100,width=200,height=28)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=160,y=180,width=200)
        cmb_status=ttk.Combobox(attendance_Frame,textvariable=self.var_status,values=("Select","Present","Absent"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=185,width=200)
        cmb_status.current(0)
        
        #Buttons
        btn_add=Button(attendance_Frame,text="Take attendance",command=self.add,font=("goudy old style",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=5,y=260,width=200,height=28)
        btn_clear=Button(attendance_Frame,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="grey",fg="white",cursor="hand2").place(x=295,y=260,width=80,height=28)
        btn_delete=Button(attendance_Frame,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#f44336",fg="white",cursor="hand2").place(x=210,y=260,width=80,height=28)

        #Calling update date & time function
        self.update_date_time()

        #Attendance table frame
        a_frame=Frame(self.root,bd=3,relief=RIDGE)
        a_frame.place(x=460,y=35,width=520,height=300)
        
        #Title of Attendance table frame
        ATitle=Label(a_frame,text="Attendance Details",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        
        #Content of attendance table frame
        scrolly=Scrollbar(a_frame,orient=VERTICAL)
        scrollx=Scrollbar(a_frame,orient=HORIZONTAL)
 
        #Attendance table
        self.attendance_table=ttk.Treeview(a_frame,columns=("aid","empid","empname","status","time","date"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.attendance_table.xview)
        scrolly.config(command=self.attendance_table.yview)

        self.attendance_table.heading("aid",text="Attend. ID")
        self.attendance_table.heading("empid",text="Emp Id")
        self.attendance_table.heading("empname",text="Emp Name")
        self.attendance_table.heading("status",text="Status")
        self.attendance_table.heading("time",text="time")
        self.attendance_table.heading("date",text="Date")
        self.attendance_table["show"]="headings"

        self.attendance_table.column("aid",width=90)
        self.attendance_table.column("empid",width=100)
        self.attendance_table.column("empname",width=100)
        self.attendance_table.column("status",width=100)
        self.attendance_table.column("time",width=100)
        self.attendance_table.column("date",width=100)
        self.attendance_table.pack(fill=BOTH,expand=1)
        self.attendance_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    #Function of fetch employee id 
    def fetch_empid(self):
        self.empid_list.append("Empty")
        self.name_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select eid from employee")
            emid=cur.fetchall()
            
            if len(emid)>0:
                del self.empid_list[:]
                self.empid_list.append("Select")
                for i in emid:
                    self.empid_list.append(i[0])
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
            
    #Function of fetch employee id 
    def fetch_name(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="Select":
                messagebox.showerror("Error","Select Emp ID",parent=self.root)
            else:
                cur.execute("select name from employee where eid LIKE '%"+self.var_empid.get()+"%' ")
                row=cur.fetchone()
                self.var_name.set(row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 

    #Function of Add attendance or take attendance 
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="" or self.var_name.get()=="" or self.var_status.get()=="Select" :
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            else:
                    cur.execute("Insert into attendance(empid,empname,status,time,date) values(?,?,?,?,?)",(
                        self.var_empid.get(),
                        self.var_name.get(),
                        self.var_status.get(),
                        self.TimeOfAttend.get(),
                        self.DateOfAttend.get(),       
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Record Added Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Function of delete attendance  
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_aid.get()=="" :
                messagebox.showerror("Error","Select data From table",parent=self.root)
            else:
                cur.execute("Select * from attendance where aid=?",(self.var_aid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from attendance where aid=?",(self.var_aid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Record Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
    
    #Function of show attendance details
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from attendance")
            rows=cur.fetchall()
            self.attendance_table.delete(*self.attendance_table.get_children())
            for row in rows:
                self.attendance_table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Function of get attendance details in table
    def get_data(self,ev):
        f=self.attendance_table.focus()
        content=(self.attendance_table.item(f))
        row=content['values']
        self.var_aid.set(row[0])
        self.var_empid.set(row[1])
        self.var_name.set(row[2])
        self.var_status.set(row[3])
        self.TimeOfAttend.set(row[4])
        self.DateOfAttend.set(row[5])

    #Function of update date & time
    def update_date_time(self):
        self.time_=time.strftime("%I:%M:%S")
        self.date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Date:{str(self.date_)}\t\t Time: {str(self.time_)}")
        self.lbl_clock.after(200,self.update_date_time)
    
    #Function of clear
    def clear(self):
        self.var_aid.set("")
        self.var_empid.set("Select")
        self.var_name.set("")
        self.var_status.set("Select")
        self.show()

if __name__=="__main__":
    root=Tk()
    obj=attendanceClass(root)
    root.mainloop()
