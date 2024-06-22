from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
from pathlib import Path
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x780+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        
        #Declaring variable for list
        self.cart_list=[]

        #Declaring variable for print 
        self.chk_print=0

        #Declaring variable for date
        self.Date = StringVar()

        #Value set for date variable
        self.Date.set(time.strftime("%d/%m/%Y"))
        
        #=====Main title======
        
        title=Label(self.root,text="Inventory Management System",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        
        #Logout button
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",18,"bold"),bg="yellow",cursor="hand2").place(x=1330,y=10,height=50,width=150)

        #===Time, date & heading====
        self.lbl_clock=Label(self.root,text="Welcome To Inventory Management System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #Product Frame
        self.var_date=StringVar()
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        #Product Frame title
        pTitle=Label(ProductFrame1,text="All Product",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        #product search frame
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        #Declaring variable for search
        self.var_search=StringVar()
        
        #Content of product search frame
        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Serach",command=self.search,font=("goudy old style",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)
        
        #Product table Frame
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        
        #Product table
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","warranty","exp","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Qty")
        self.product_Table.heading("warranty",text="Warranty")
        self.product_Table.heading("exp",text="Exp Date")
        self.product_Table.heading("status",text="Status")
        
        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("warranty",width=100)
        self.product_Table.column("exp",width=90)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity To Remove Product From Cart'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)
        Warn_label=Label(self.root,text="Please Check The Expiry Date Of Product Before Sale",font=("times new roman",15),bg="white",fg="red",bd=1,cursor="hand2").place(x=10,y=700)

        #Customer Details Frame     
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=700,height=70)

        #Declaring variable for customer details
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        self.var_deliver=StringVar()

        #Customer details frame title
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
 
        #Content of customer details frame 
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=60,y=35,width=160)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=220,y=35)

        #Function of contact for limitsize
        def limitSize(*args):
            value =self.var_contact.get()
            if len(value) > 2: self.var_contact.set(value[:10])
        self.var_contact.trace('w', limitSize)
        validate_contact=self.root.register(self.checkcontact)

        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow",validate='key',validatecommand=(validate_contact,"%P")).place(x=320,y=35,width=140)
        lbl_status=Label(CustomerFrame,text="Delivery status",font=("goudy old style",15),bg="white").place(x=460,y=35)
       
        cmb_status=ttk.Combobox(CustomerFrame,textvariable=self.var_deliver,values=("Select","Free delivery","Delivery charges","None"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=580,y=35,width=115)
        cmb_status.current(0)

        #Cart, order table & cart widgets frame
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=700,height=360)
        
        #Cart Table Frame
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=5,y=8,width=300,height=342)

        #title of Cart Table Frame
        self.cartTitle=Label(Cart_Frame,text="Cart \t Total Product:[0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)
        
        #Cart table
        self.Cart_Table=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Cart_Table.xview)
        scrolly.config(command=self.Cart_Table.yview)

        self.Cart_Table.heading("pid",text="PID")
        self.Cart_Table.heading("name",text="Name")
        self.Cart_Table.heading("price",text="Price")
        self.Cart_Table.heading("qty",text="Qty")
       
        self.Cart_Table["show"]="headings"

        self.Cart_Table.column("pid",width=40)
        self.Cart_Table.column("name",width=90)
        self.Cart_Table.column("price",width=90)
        self.Cart_Table.column("qty",width=40)
        self.Cart_Table.pack(fill=BOTH,expand=1)
        self.Cart_Table.bind("<ButtonRelease-1>",self.get_data_cart)

        #Menus frame=ADD cart 
        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=550,width=700,height=110)

        #Declaring variables for add to cart
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_exp=StringVar()
        self.var_stock=StringVar()
        self.var_war=StringVar()

        #Content of add cart frame
        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=175,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=195,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=195,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=360,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=360,y=35,width=100,height=22)
        
        #Order button
        btn_order=Button(Add_CartWidgetsFrame,text="Add to order",font=("times new roman",17,"bold"),bg="red",fg="white",cursor="hand2",command=self.add_order).place(x=480,y=15,width=180,height=40)
    
        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)
        
        #Clear cart button
        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)

        #Add update cart button
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)
        
        #Order Table Frame
        order_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        order_Frame.place(x=310,y=8,width=390,height=342)
         
        #Order Table Frame title
        self.orderTitle=Label(order_Frame,text="Order",font=("goudy old style",15),bg="lightgray")
        self.orderTitle.pack(side=TOP,fill=X)
        scrolly=Scrollbar(order_Frame,orient=VERTICAL)
        scrollx=Scrollbar(order_Frame,orient=HORIZONTAL)
  
        #Order Table
        self.order_Table=ttk.Treeview(order_Frame,columns=("oid","custname","contact","pname","qty","price","date"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.order_Table.xview)
        scrolly.config(command=self.order_Table.yview)

        #Declaring variable
        self.var_oid=StringVar()

        self.order_Table.heading("oid",text="OID")
        self.order_Table.heading("custname",text="CustName")
        self.order_Table.heading("contact",text="Contact")
        self.order_Table.heading("pname",text="ProdName")
        self.order_Table.heading("qty",text="Qty")
        self.order_Table.heading("price",text="Price")
        self.order_Table.heading("date",text="Date") 
        self.order_Table["show"]="headings"

        self.order_Table.column("oid",width=40)
        self.order_Table.column("custname",width=90)
        self.order_Table.column("contact",width=90)
        self.order_Table.column("pname",width=90)
        self.order_Table.column("qty",width=40)
        self.order_Table.column("price",width=90)
        self.order_Table.column("date",width=90)
        self.order_Table.pack(fill=BOTH,expand=1)
        self.order_Table.bind("<ButtonRelease-1>",self.get_order_data)

        #Billing Area frame
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=1120,y=110,width=410,height=410)
 
        ##Billing Area frame Title
        BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        #Bill receipt area
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        
          
        #Billing Buttons frame(Menus)
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=1120,y=520,width=410,height=190)
        
        #row1
        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_gst=Label(billMenuFrame,text="GST\n[18%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_gst.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)
        
        #row2
        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)
        
        btn_generate=Button(billMenuFrame,text="Generate/Save Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)

        btn_update=Button(billMenuFrame,text="Update Sale\nIn Excel",command=self.add,font=("goudy old style",15,"bold"),bg="#4caf50",fg="white",cursor="hand2")
        btn_update.place(x=145,y=135,width=120,height=50)
        
        #Footer
        footer=Label(self.root,text="IMS-Inventory Management System | For Any Technical Issue Contact:987xxxx01",font=("times new roman",11),bg="#4d636d",fg="white",bd=0,cursor="hand2").pack(side=BOTTOM,fill=X)

        #Calling functions
        self.show()
        self.update_date_time()
        
        

        #ALL FUNCTIONS====

    #Show product table function
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,warranty,exp,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)  

    #Search function for product table
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search Input Required",parent=self.root)

            else:
                cur.execute("select pid,name,price,qty,warranty,exp,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)        
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)            
    
    #Get product table details function
    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_exp.set(row[4])
        self.var_war.set(row[4])
        self.var_qty.set('1')
        
        
    #Get product table details to cart table function
    def get_data_cart(self,ev):
        f=self.Cart_Table.focus()
        content=(self.Cart_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3]) 
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
          

    #Add update product function
    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Error","Please Select Product",parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error","Quantity Is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)    
        else:
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
    
            #Update Cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno("Confirm","Product Already Present\nDo You Want To Update| Remove From The Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)    

            self.show_cart()
            self.bill_updates()

    #Bill amount , netpay is getting updated for every new product
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.gst=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.gst=(self.bill_amnt*18)/100 
        self.net_pay=self.bill_amnt+self.gst
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    #Show details in cart table
    def show_cart(self):
        try:
            self.Cart_Table.delete(*self.Cart_Table.get_children())
            for row in self.cart_list:
                self.Cart_Table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    #Generate bill function
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='' or self.var_deliver.get()=='':
            messagebox.showerror("Error",f"Customer Details Are Required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product To The Cart",parent=self.root)
        else:
            #Bill Top
            self.bill_top()
            #Bill Middle
            self.bill_middle()
            #Bill Bottom
            self.bill_bottom()
            #Bill Last
            self.bill_last()

            fp=open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill Has Been Generated/Saved In Backend",parent=self.root)

            self.chk_print=1

           
    #Top bil area function
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tElectronic Sales-Inventory
\t Phone No. 8551080719 , Mumbai-400029
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph No. :{self.var_contact.get()}
 Invoice No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))} 
{str("="*47)}
 Product Name\t\t\tQty\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    #Middle bill area function
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:  
            for row in self.cart_list:
                
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"    
    
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #update quantity in product table  
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))  
                con.commit()
            con.close()
            self.show()    
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        

    #Bottom bill area function
    def bill_bottom(self):
        bill_bottom_temp=f'''   
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 GST\t\t\t\tRs.{self.gst}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        ''' 
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_last(self):
        bill_last_temp=f'''
 Delivery status:{self.var_deliver.get()}     
 *Goods once sold will not be taken back
 *1 Year warranty from invoice date
 *Terms & Conditions applied
{str("="*47)}\n      
        '''   
        self.txt_bill_area.insert(END,bill_last_temp)

    #Clear cart table function
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('') 
        self.lbl_inStock.config(text=f"In Stock ")
        self.var_stock.set('')

    #Clear all winow function
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_deliver.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
    
    #Update date & time function
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    #Print bill function
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please Wait While Printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please Generate Bill To Print The Receipt",parent=self.root)
  
    #Logout function
    def logout(self):
        self.root.destroy()
        os.system("python login.py")        
    
    #TOtal sales update excel sheet
    def add(self):
        absolutePath = Path('C:/Users/Neha/Desktop/Project/Inventory/Order.xlsx').resolve()
        os.system(f'start excel.exe "{absolutePath}"')   

    #Add order function
    def add_order(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cname.get()=="" or self.var_contact.get()=="" or self.var_pname.get()=="Select" or self.var_qty.get()=="" or self.var_price.get()=="" :
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            
            else:
                    cur.execute("Insert into cart(custname,contact,pname,qty,price,date) values(?,?,?,?,?,?)",(
                        self.var_cname.get(),
                        self.var_contact.get(),
                        self.var_pname.get(),
                        self.var_qty.get(),
                        self.var_price.get(),
                        self.Date.get(),
                                 
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Order Added Successfully",parent=self.root)  
                    self.show_order()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Show order details in table
    def show_order(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from cart")
            rows=cur.fetchall()
            self.order_Table.delete(*self.order_Table.get_children())
            for row in rows:
                self.order_Table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    

     #Get order details in order table
    def get_order_data(self,ev):
        f=self.order_Table.focus()
        content=(self.order_Table.item(f))
        row=content['values']
        self.var_oid.set(row[0])
        self.var_cname.set(row[1])
        self.var_contact.set(row[2])
        self.var_pname.set(row[3])
        self.var_qty.set(row[4])
        self.var_price.set(row[5])
        self.Date.set(row[6])

    #Check contact field function
    def checkcontact(self,contact):
        if contact.isdigit():
            return True
        if len(str(contact))==0:
            return True
        else:
            messagebox.showerror("Invalid","Invalid contact",parent=self.root)
            return False    
             
        
     









          
            


     


           

























if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()