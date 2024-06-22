from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time
class ReturnClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #All variables
        self.var_oid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_invoice=StringVar()
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        self.var_status=StringVar()
        self.Date = StringVar()
        self.Date.set(time.strftime("%d/%m/%Y"))
       
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        #Return product frame
        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=495)
        
        #Return product frame title
        title=Label(product_Frame,text="Manage Return Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        
        #column1
        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_invoice=Label(product_Frame,text="Invoice no.",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_CName=Label(product_Frame,text="Cust.name",font=("goudy old style",18),bg="white").place(x=30,y=310)
        lbl_contact=Label(product_Frame,text="Contact no.",font=("goudy old style",18),bg="white").place(x=30,y=360)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=410)
       

        #===Column2
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=200)

        #Calling function for check price
        validate_pic=self.root.register(self.checkprice)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow",validate="key", validatecommand=(validate_pic, '%P')).place(x=150,y=210,width=200)
        txt_invoice=Entry(product_Frame,textvariable=self.var_invoice,font=("goudy old style",15),bg="lightyellow",validate="key", validatecommand=(validate_pic, '%P')).place(x=150,y=260,width=200)
        txt_cname=Entry(product_Frame,textvariable=self.var_cname,font=("goudy old style",15),bg="lightyellow").place(x=150,y=310,width=200)

        #Contact field limitsize function
        def limitSize(*args):
            value =self.var_contact.get()
            if len(value) > 2: self.var_contact.set(value[:10])
        self.var_contact.trace('w', limitSize)
        
        txt_contact=Entry(product_Frame,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow",validate='key',validatecommand=(validate_pic,"%P")).place(x=150,y=360,width=200)
        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Select","Issue Solved","Issue Not Solved","Refund","Exchange"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=410,width=200)
        cmb_status.current(0)
        
          
        #Buttons===
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=445,width=100,height=40)
        btn_udate=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=445,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=445,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=445,width=100,height=40)     
        
        
        #===Search Frame===
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=460,y=0,width=630,height=80)

        #==OPtions===
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)
        


        #Return Product Table frame
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=460,y=80,width=630,height=425)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        #Return Product Table
        self.product_table=ttk.Treeview(p_frame,columns=("oid","Category","Supplier","name","price","invoice","cname","contact","status","date"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("oid",text="O ID")
        self.product_table.heading("Category",text="Category")
        self.product_table.heading("Supplier",text="Supplier")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("invoice",text="Invoice no.")
        self.product_table.heading("cname",text="Cust name")
        self.product_table.heading("contact",text="Contact")
        self.product_table.heading("status",text="Status")
        self.product_table.heading("date",text="Date")
        
        self.product_table["show"]="headings"

        self.product_table.column("oid",width=90)
        self.product_table.column("Category",width=100)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("invoice",width=100)
        self.product_table.column("cname",width=100)
        self.product_table.column("contact",width=100)
        self.product_table.column("status",width=100)
        self.product_table.column("date",width=100)
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        
    #Fetch category & supplier function
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0]) 
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)     

    #Add return product function
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="" or self.var_cname.get()=="" or self.var_contact.get()=="" or self.var_invoice.get()=="" or self.var_price.get()=="" or self.var_status.get()=="Select":
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            else:
                cur.execute("Select * from purchase where invoice=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Return Product Already Available,Try Different",parent=self.root)
                else:
                    cur.execute("Insert into purchase(Category,Supplier,name,price,invoice,cname,contact,status,date) values(?,?,?,?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_invoice.get(),
                        self.var_cname.get(),
                        self.var_contact.get(),
                        self.var_status.get(),  
                        self.Date.get()
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Return Product Added Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
        
    #Show return product function
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from purchase")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    
    
    #Get return product details function
    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_oid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_invoice.set(row[5])
        self.var_cname.set(row[6])
        self.var_contact.set(row[7])
        self.var_status.set(row[8])
        self.Date.set(row[9])

    #Update return product function 
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_oid.get()=="" :
                messagebox.showerror("Error","Please Select return Product",parent=self.root)
            else:
                cur.execute("Select * from purchase where oid=?",(self.var_oid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Return Product",parent=self.root)
                else:
                    cur.execute("Update purchase set Category=?,Supplier=?,name=?,price=?,invoice=?,cname=?,contact=?,status=?,date=? where oid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_invoice.get(),
                        self.var_cname.get(),
                        self.var_contact.get(),
                        self.var_status.get(),
                        self.Date.get(),
                        self.var_oid.get()
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Return Product Updated Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Delete return product function
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_oid.get()=="" :
                messagebox.showerror("Error","Please Select return product",parent=self.root)
            else:
                cur.execute("Select * from purchase where oid=?",(self.var_oid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Return Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from purchase where oid=?",(self.var_oid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Return Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Clear return product details
    def clear(self):
        self.var_oid.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_invoice.set("")
        self.var_cname.set("")
        self.var_contact.set("")
        self.var_status.set("Select")
        self.Date.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
 
    #Search return product
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search Input Should Be Required",parent=self.root)

            else:
                cur.execute("select * from purchase where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)        
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)       

    #Validation for price field  
    def checkprice(self,p):
        if p.isdigit():
            return True
        if len(str(p))==0:
            return True
        else:
            messagebox.showerror("Invalid","Invalid Entry",parent=self.root)
            return False

if __name__=="__main__":
    root=Tk()
    obj=ReturnClass(root)
    root.mainloop()
