from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import os
import tempfile
import time
class salaryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x650+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(0,0)

        #Declaring print variable
        self.chk_print=0
        
        #  All Variables
        self.Hrs_wage = StringVar()
        self.Wrk_Hrs = StringVar()
        self.Payable = StringVar()
        self.Taxable = StringVar()
        self.NetPayable = StringVar()
        self.GrossPayable = StringVar()
        self.OverTimeBonus = StringVar()
        self.var_wid = StringVar()
        self.TimeOfOrder = StringVar()
        self.DateOfOrder = StringVar()
        self.DateOfOrder.set(time.strftime("%d/%m/%Y"))
        self.Date = StringVar()
        self.Date.set(time.strftime("%d/%m/%Y"))
        self.var_empid=StringVar()
        self.var_eid=StringVar()
        self.var_name=StringVar()
        self.empid_list=[]
        self.name_list=[]
        self.hrs_rate=[100]
        self.fetch_empid()


        #Title Frame
        Tops = Frame(self.root, width=1350, height=50, bd=8, bg="cornflower blue")
        Tops.pack(side=TOP)

#main frame
        f1 = Frame(self.root, width=700, height=600, bd=8, bg="white")
        f1.place(x=0,y=50,width=1000,height=410)

#label frame
        f2 = Frame(self.root, width=300, height=600, bd=8, bg="white")
        f2.place(x=1000,y=50,width=360,height=500)

#Date Frame
        fla = Frame(f1, width=600, height=350, bd=8, bg="white")
        fla.pack(side=TOP)

        #Title
        lbl_information = Label(Tops, font=('arial', 20, 'bold'), text="Employee Salary System ", relief=GROOVE,  bd=1, bg="white", fg="Black")
        lbl_information.grid(row=0, column=0)

        payslip = Label(f2, textvariable=self.DateOfOrder, font=('arial', 21, 'bold'), fg="black", bg="white").grid(row=0,
                                                                                                           column=0)
        ATitle=Label(self.root,text="Payslip",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").place(x=1140,y=15)
           
        self.txtPaymentSlip = Text(f2, height=22, width=34, bd=16, font=('arial', 13, 'bold'), fg="black", bg="white")
        self.txtPaymentSlip.grid(row=1, column=0)
        
        
        # Label Widget

        labelFirstName = Label(fla, text="Emp Name", font=('goudy old style', 15,"bold"), bd=2, fg="black", bg="white").grid(row=0, column=2)

        labelEid = Label(fla, text="Emp Id", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=0,
                                                                                                               column=0)
        labelHoursWorked = Label(fla, text="Hours Worked", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=2, column=0)
        
        labelHourlyRate = Label(fla, text="Hourly Rate", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=2, column=2)

        labelTax = Label(fla, text="Tax", font=('goudy old style',15,"bold"), bd=2, anchor='w', fg="black", bg="white").grid(row=3,
                                                                                                                column=0)
        labelOverTime = Label(fla, text="OverTime", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=3,
                                                                                                              column=2)
        labelGrossPay = Label(fla, text="GrossPay", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=4,
                                                                                                              column=0)
        labelNetPay = Label(fla, text="Net Pay", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=4,
                                                                                                           column=2)
        labelwid = Label(fla, text="Week No.", font=('goudy old style',15,"bold"), bd=2, fg="black", bg="white").grid(row=5,
                                                                                                           column=1)

# Entry Widget

        txtname = Entry(fla, textvariable=self.var_name, font=('arial', 16, 'bold'),  width=22, justify='left',bg="lightyellow",fg="black")
        txtname.grid(row=0, column=3)
        cmb_eid=ttk.Combobox(fla,textvariable=self.var_empid,values=self.empid_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_eid.grid(row=0,column=1)
        cmb_eid.current(0)
        txtWrk_hrs = Entry(fla, textvariable=self.Wrk_Hrs, font=('arial', 16, 'bold'),  width=22, justify='left',bg="lightyellow",fg="black")
        txtWrk_hrs.grid(row=2, column=1)

        txtHrs_Wages = Entry(fla, textvariable=self.Hrs_wage,font=('arial', 16, 'bold'), width=22, justify='left',bg="lightyellow",fg="black")
        txtHrs_Wages.grid(row=2, column=3)

        
        txtGrossPayment = Entry(fla, textvariable=self.Payable, font=('arial', 16, 'bold'),  width=22, justify='left',bg="lightyellow",fg="black")
        txtGrossPayment.grid(row=4, column=1)

        txtNetPayable = Entry(fla, textvariable=self.NetPayable, font=('arial', 16, 'bold'),  width=22, justify='left',bg="lightyellow",fg="black")
        txtNetPayable.grid(row=4, column=3)

        txtTaxable = Entry(fla, textvariable=self.Taxable, font=('arial', 16, 'bold'),  width=22, justify='left',bg="lightyellow",fg="black")
        txtTaxable.grid(row=3, column=1)

        txtOverTimeBonus = Entry(fla, textvariable=self.OverTimeBonus, font=('arial', 16, 'bold'),  width=22, justify='left',bg="lightyellow",fg="black")
        txtOverTimeBonus.grid(row=3, column=3)

        cmb_status=ttk.Combobox(fla,textvariable=self.var_wid,values=("Select",
                                                    "Aug w1 8 21",
                                                    "Aug w2 8 21",
                                                    "Aug w3 8 21",
                                                    "Aug w4 8 21",
                                                    "sep w1 9 21",
                                                    "sep w2 9 21",
                                                    "sep w3 9 21",
                                                    "sep w4 9 21",
                                                    "Oct w1 10 21",
                                                    "Oct w2 10 21",
                                                    "Oct w3 10 21",
                                                    "Oct w4 10 21",
                                                    "Nov w1 11 21",
                                                    "Nov w2 11 21",
                                                    "Nov w3 11 21",
                                                    "Nov w4 11 21",
                                                    "Dec w1 12 21",
                                                    "Dec w2 12 21",
                                                    "Dec w3 12 21",
                                                    "Dec w4 12 21",
                                                    "Jan w1 1 22",
                                                    "Jan w2 1 22",
                                                    "Jan w3 1 22",
                                                    "Jan w4 1 22",
                                                    "Feb w1 2 22",
                                                    "Feb w2 2 22",
                                                    "Feb w3 2 22",
                                                    "Feb w4 2 22",
                                                    "Mar w1 3 22",
                                                    "Mar w2 3 22",
                                                    "Mar w3 3 22",
                                                    "Mar w4 3 22",
                                                    "Apr w1 1 22",
                                                    "Apr w2 1 22",
                                                    "Apr w3 1 22",
                                                    "Apr w4 1 22",
                                                    "May w1 5 22",
                                                    "May w2 5 22",
                                                    "May w3 5 22",
                                                    "May w4 5 22",
                                                    "Jun w1 6 22",
                                                    "Jun w2 6 22",
                                                    "Jun w3 6 22",
                                                    "Jun w4 6 22",
                                                    "Jan w1 7 22",
                                                    "Jul w2 7 22",
                                                    "Jul w3 7 22",
                                                    "Jul w4 7 22",
                                                    "Aug w1 8 22",
                                                    "Aug w2 8 22",
                                                    "Aug w3 8 22",
                                                    "Aug w4 8 22",
                                                    "sep w1 9 22",
                                                    "sep w2 9 22",
                                                    "sep w3 9 22",
                                                    "sep w4 9 22",
                                                    "Oct w2 10 22",
                                                    "Oct w2 10 22",
                                                    "Oct w3 10 22",
                                                    "Oct w4 10 22",
                                                    "Nov w1 11 22",
                                                    "Nov w2 11 22",
                                                    "Nov w3 11 22",
                                                    "Nov w4 11 22",
                                                    "Dec w1 12 22",
                                                    "Dec w2 12 22",
                                                    "Dec w3 12 22",
                                                    "Dec w4 12 22",
                                                    "Jan w1 1 23",
                                                    "Jan w2 1 23",
                                                    "Jan w3 1 23",
                                                    "Jan w4 1 23",
                                                    "Feb w1 2 23",
                                                    "Feb w2 2 23",
                                                    "Feb w3 2 23",
                                                    "Feb w4 2 23",
                                                    "Mar w1 3 23",
                                                    "Mar w2 3 23",
                                                    "Mar w3 3 23",
                                                    "Mar w4 3 23",
                                                    "Apr w1 1 23",
                                                    "Apr w2 1 23",
                                                    "Apr w3 1 23",
                                                    "Apr w4 1 23",
                                                    "May w1 5 23",
                                                    "May w2 5 23",
                                                    "May w3 5 23",
                                                    "May w4 5 23",
                                                    "Jun w1 6 23",
                                                    "Jun w2 6 23",
                                                    "Jun w3 6 23",
                                                    "Jun w4 6 23",
                                                    "Jan w1 7 23",
                                                    "Jul w2 7 23",
                                                    "Jul w3 7 23",
                                                    "Jul w4 7 23",
                                                    "Aug w1 8 23",
                                                    "Aug w2 8 23",
                                                    "Aug w3 8 23",
                                                    "Aug w4 8 23",
                                                    "sep w2 9 23",
                                                    "sep w2 9 23",
                                                    "sep w3 9 23",
                                                    "sep w4 9 23",
                                                    "Oct w2 10 23",
                                                    "Oct w2 10 23",
                                                    "Oct w3 10 23",
                                                    "Oct w4 10 23",
                                                    "Nov w1 11 23",
                                                    "Nov w2 11 23",
                                                    "Nov w3 11 23",
                                                    "Nov w4 11 23",
                                                    "Dec w1 12 23",
                                                    "Dec w2 12 23",
                                                    "Dec w3 12 23",
                                                    "Dec w4 12 23",
                                                    "Jan w1 1 24",
                                                    "Jan w2 1 24",
                                                    "Jan w3 1 24",
                                                    "Jan w4 1 24",
                                                    "Feb w1 2 24",
                                                    "Feb w2 2 24",
                                                    "Feb w3 2 24",
                                                    "Feb w4 2 24",
                                                    "Mar w1 3 24",
                                                    "Mar w2 3 24",
                                                    "Mar w3 3 24",
                                                    "Mar w4 3 24",
                                                    "Apr w1 1 24",
                                                    "Apr w2 1 24",
                                                    "Apr w3 1 24",
                                                    "Apr w4 1 24",
                                                    "May w1 5 24",
                                                    "May w2 5 24",
                                                    "May w3 5 24",
                                                    "May w4 5 24",
                                                    "Jun w1 6 24",
                                                    "Jun w2 6 24",
                                                    "Jun w3 6 24",
                                                    "Jun w4 6 24",
                                                    "Jan w1 7 24",
                                                    "Jul w2 7 24",
                                                    "Jul w3 7 24",
                                                    "Jul w4 7 24",
                                                    "Aug w1 8 24",
                                                    "Aug w2 8 24",
                                                    "Aug w3 8 24",
                                                    "Aug w4 8 24",
                                                    "sep w2 9 24",
                                                    "sep w2 9 24",
                                                    "sep w3 9 24",
                                                    "sep w4 9 24",
                                                    "Oct w2 10 24",
                                                    "Oct w2 10 24",
                                                    "Oct w3 10 24",
                                                    "Oct w4 10 24",
                                                    "Nov w1 11 24",
                                                    "Nov w2 11 24",
                                                    "Nov w3 11 24",
                                                    "Nov w4 11 24",
                                                    "Dec w1 12 24",
                                                    "Dec w2 12 24",
                                                    "Dec w3 12 24",
                                                    "Dec w4 12 24",
                                                    "Jan w1 1 25",
                                                    "Jan w2 1 25",
                                                    "Jan w3 1 25",
                                                    "Jan w4 1 25",
                                                    "Feb w1 2 25",
                                                    "Feb w2 2 25",
                                                    "Feb w3 2 25",
                                                    "Feb w4 2 25",
                                                    "Mar w1 3 25",
                                                    "Mar w2 3 25",
                                                    "Mar w3 3 25",
                                                    "Mar w4 3 25",
                                                    "Apr w1 1 25",
                                                    "Apr w2 1 25",
                                                    "Apr w3 1 25",
                                                    "Apr w4 1 25",
                                                    "May w1 5 25",
                                                    "May w2 5 25",
                                                    "May w3 5 25",
                                                    "May w4 5 25",
                                                    "Jun w1 6 25",
                                                    "Jun w2 6 25",
                                                    "Jun w3 6 25",
                                                    "Jun w4 6 25",
                                                    "Jan w1 7 25",
                                                    "Jul w2 7 25",
                                                    "Jul w3 7 25",
                                                    "Jul w4 7 25",
                                                    "Aug w1 8 25",
                                                    "Aug w2 8 25",
                                                    "Aug w3 8 25",
                                                    "Aug w4 8 25",
                                                    "sep w2 9 25",
                                                    "sep w2 9 25",
                                                    "sep w3 9 25",
                                                    "sep w4 9 25",
                                                    "Oct w2 10 25",
                                                    "Oct w2 10 25",
                                                    "Oct w3 10 25",
                                                    "Oct w4 10 25",
                                                    "Nov w1 11 25",
                                                    "Nov w2 11 25",
                                                    "Nov w3 11 25",
                                                    "Nov w4 11 25",
                                                    "Dec w1 12 25",
                                                    "Dec w2 12 25",
                                                    "Dec w3 12 25",
                                                    "Dec w4 12 25",),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_status.grid(row=5,column=2)
        cmb_status.current(0)
        
        # buttons
        ButtonSalary = Button(self.root, text='Weekly Salary', bd=2, font=('arial', 16, 'bold'), relief="groove", width=14, fg="black",
                   bg="lightgrey", command=self.WagesForWeekly,cursor="hand2").place(x=200,y=230)

        ButtonPaySlip = Button(self.root, text='View Payslip',bd=2, font=('arial', 16, 'bold'), relief="groove", width=14,
                    command=self.InformationEntry, fg="black", bg="lightgrey",cursor="hand2").place(x=400,y=230)

        ButtonName = Button(self.root, text='Show employee name',bd=2, font=('arial', 16, 'bold'), relief="groove", width=17,
                    command=self.add_name, fg="black", bg="lightgrey",cursor="hand2").place(x=600,y=230)
            

        ButtonPrint = Button(self.root, text='Print',bd=2, font=('arial', 16, 'bold'), relief="groove", width=14, command=self.print_slip,fg="white", bg="green",cursor="hand2").place(x=1130,y=560,width=120,height=50)
        
        
        ButtonAdd = Button(self.root, text='Add',bd=2, font=('arial', 16, 'bold'), relief="groove", width=14,
                 fg="black", bg="#2196f3",cursor="hand2",command=self.add).place(x=150,y=280)
        Buttonupdate = Button(self.root, text='Update',bd=2, font=('arial', 16, 'bold'), relief="groove", width=14,
                 fg="black", bg="#4caf50",cursor="hand2",command=self.update).place(x=350,y=280)
        ButtonDelete = Button(self.root, text='Delete', bd=2, font=('arial', 16, 'bold'), relief="groove", width=14,
                 fg="black", bg="#f44336",cursor="hand2",command=self.delete).place(x=550,y=280)
        ButtonClear = Button(self.root, text='Clear', bd=2, font=('arial', 16, 'bold'), relief="groove", width=14,
                 fg="black", bg="#607d8b",cursor="hand2",command=self.clear).place(x=750,y=280)      
    
        #Salary table frame
        emp_frame=Frame(self.root,bd=1,relief=RIDGE,bg="black")
        emp_frame.place(x=210,y=370,width=650,height=250)
        ATitle=Label(emp_frame,text="Salary Details",font=("goudy old style",20,"bold"),bg="cornflower blue",fg="white").pack(side=TOP,fill=X)
        

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        
        #Salary table
        self.salary_table=ttk.Treeview(emp_frame,columns=("eid","empid","empname","netpay","wid","date"),yscrollcommand=scrolly.set)
        

        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.salary_table.yview)

        self.salary_table.heading("eid",text="S ID")
        self.salary_table.heading("empid",text="Emp ID")
        self.salary_table.heading("empname",text="Emp Name")
        self.salary_table.heading("netpay",text="Netpay")
        self.salary_table.heading("wid",text="W No.")
        self.salary_table.heading("date",text="Date")
       
        self.salary_table["show"]="headings"
        
        self.salary_table.column("eid",width=90)
        self.salary_table.column("empid",width=100)
        self.salary_table.column("empname",width=100)
        self.salary_table.column("netpay",width=100)
        self.salary_table.column("wid",width=100)
        self.salary_table.column("date",width=100)
        self.salary_table.pack(fill=BOTH,expand=1)
        self.salary_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()

#Payment slip info entry
    def InformationEntry(self):
        self.txtPaymentSlip.delete("1.0", END)
        self.txtPaymentSlip.insert(END, "\t\tPay Slip\n\n")
        self.txtPaymentSlip.insert(END, "Emp Name :\t\t" + self.var_name.get() + "\n\n")
        self.txtPaymentSlip.insert(END, "Hours Worked :\t\t" + self.Wrk_Hrs.get() + "\n\n")
        self.txtPaymentSlip.insert(END, "Wages per hour :\t\t" + self.Hrs_wage.get() + "\n\n")
        self.txtPaymentSlip.insert(END, "Tax Paid :\t\t" + self.Taxable.get() + "\n\n")
        self.txtPaymentSlip.insert(END, "Payable :\t\t" + self.Payable.get() + "\n\n")
        self.txtPaymentSlip.insert(END, "Overtime Bonus :\t\t" +  self.OverTimeBonus.get() + "\n\n")
        self.txtPaymentSlip.insert(END, "Net Payable :\t\t" + self.NetPayable.get() + "\n\n")
        
        self.chk_print=1
    
    #function for weekly salary
    def WagesForWeekly(self):
        self.txtPaymentSlip.delete("1.0", END)
        hrs_wrk_per_wek = float(self.Wrk_Hrs.get())
        hrs_per_wgs = float(self.Hrs_wage.get())

        DuePayment = hrs_per_wgs * hrs_wrk_per_wek
        PaymentDue = "INR" + str('%.2f' % DuePayment)
        self.Payable.set(PaymentDue)

        tax = DuePayment * 0.12
        taxable = "INR" + str('%.2f' % tax)
        self.Taxable.set(taxable)

        PaymentNet = DuePayment - tax
        NetPayments = "INR" + str('%.2f' % PaymentNet)
        self.NetPayable.set(NetPayments)

        if hrs_wrk_per_wek > 40:  
            HoursTimeOver = (hrs_wrk_per_wek - 40) + hrs_per_wgs * 1.5
            OverTime = "INR" + str('%.2f' % HoursTimeOver)
            self.OverTimeBonus.set(OverTime)
        elif hrs_wrk_per_wek <= 40:
            PaymentOverTime = (hrs_wrk_per_wek - 40) + hrs_per_wgs * 1.5
            HoursOverTime = "INR" + str('%.2f' % PaymentOverTime)
            self.OverTimeBonus.set(HoursOverTime)
        return
    
    #Print slip function
    def print_slip(self):
        
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please Wait While Printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txtPaymentSlip.get('1.0',END))
            os.startfile(new_file,'print')
        else:
             messagebox.showerror('Print',"Please Generate paymentslip To Print The Receipt",parent=self.root)
        
    
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
    
    #Fetch employee name function
    def add_name(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="Select":
                messagebox.showerror("Error","Select emp id",parent=self.root)
            else:
                cur.execute("select name from employee where eid LIKE '%"+self.var_empid.get()+"%' ")
                row=cur.fetchone()
                self.var_name.set(row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 

    #Add record function
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="Select" or  self.var_name.get()=="Select" or self.var_wid.get()=="Select" :
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            else:
                cur.execute("Select * from salary where  empid=? AND empname=? AND wid=? ",(self.var_empid.get(),self.var_name.get(),self.var_wid.get(),))
                user=cur.fetchone()
                if user!=None:
                    messagebox.showerror("Error","Salary of this week already assigned to this employee",parent=self.root)
                else:
                    cur.execute("Insert into salary(empid,empname,netpay,wid,date) values(?,?,?,?,?)",(
                        self.var_empid.get(),
                        self.var_name.get(),
                        self.NetPayable.get(),
                        self.var_wid.get(),
                        self.Date.get()     
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Record Added Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
        
    #Show record function
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from salary")
            rows=cur.fetchall()
            self.salary_table.delete(*self.salary_table.get_children())
            for row in rows:
                self.salary_table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    
    
    #Get record function
    def get_data(self,ev):
        f=self.salary_table.focus()
        content=(self.salary_table.item(f))
        row=content['values']
        self.var_eid.set(row[0])
        self.var_empid.set(row[1])
        self.var_name.set(row[2])
        self.NetPayable.set(row[3])
        self.var_wid.set(row[4])
        self.Date.set(row[5])
       
    #Update record function  
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="Select" :
                messagebox.showerror("Error","Please Select record",parent=self.root)
            else:
                cur.execute("Select * from salary where eid=?",(self.var_eid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid ",parent=self.root)
                else:
                    cur.execute("Update salary set empid=?,empname=?,netpay=?,wid=?,date=? where eid=?",(
                        self.var_empid.get(),
                        self.var_name.get(),
                        self.NetPayable.get(),
                        self.var_wid.get(),
                        self.Date.get(),
                        self.var_eid.get()                 
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Record Updated Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Delete record function
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_eid.get()=="" :
                messagebox.showerror("Error","Please Select record",parent=self.root)
            else:
                cur.execute("Select * from salary where eid=?",(self.var_eid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from salary where eid=?",(self.var_eid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Record Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Clear function
    def clear(self):
        self.var_eid.set("")
        self.var_empid.set("Select")
        self.var_name.set("")
        self.NetPayable.set("")
        self.var_wid.set("Select")
        self.Wrk_Hrs.set("")
        self.Hrs_wage.set("")
        self.Payable.set("")
        self.Taxable.set("")
        self.GrossPayable.set("")
        self.OverTimeBonus.set("")
        self.txtPaymentSlip.delete("1.0", END)
        self.show()

if __name__=="__main__":
    root=Tk()
    obj=salaryClass(root)
    root.mainloop()
    