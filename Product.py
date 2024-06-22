from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import re
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(0,0)
        
        #All variables
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_war=StringVar()
        self.var_exp=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        #Product details frame
        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=460,height=490)
       
       #Title of Product details frame
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        
        #column1
        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_war=Label(product_Frame,text="Warranty",font=("goudy old style",18),bg="white").place(x=30,y=310)
        lbl_exp=Label(product_Frame,text="ExpiryDate",font=("goudy old style",18),bg="white").place(x=30,y=360)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=400)

        #===Column2
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=250)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=250)
        cmb_sup.current(0)
        
        #Calling function for check price quantity field 
        validate_pq=self.root.register(self.checkpriceqty)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=250)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow",validate="key", validatecommand=(validate_pq, '%P')).place(x=150,y=210,width=250)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow",validate="key", validatecommand=(validate_pq, '%P')).place(x=150,y=260,width=250)
        txt_war=Entry(product_Frame,textvariable=self.var_war,font=("goudy old style",15),bg="lightyellow").place(x=150,y=310,width=250)
        
        txt_exp=Entry(product_Frame,textvariable=self.var_exp,font=("goudy old style",15),bg="lightyellow").place(x=150,y=360,width=250)
        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=400,width=250)
        cmb_status.current(0)

        
        #Buttons===
        btn_check=Button(product_Frame,text="Check",command=self.validation,font=("goudy old style",15),bg="green",fg="white",cursor="hand2").place(x=0,y=440,width=90,height=28)
        
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=92,y=440,width=90,height=28)
        btn_udate=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=184,y=440,width=90,height=28)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=276,y=440,width=90,height=28)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=368,y=440,width=90,height=28)     
        
        
        #===Search Frame===
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #==OPtions===
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)
        


        #Product table frame
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=400)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)
        
        #Product table
        self.product_table=ttk.Treeview(p_frame,columns=("pid","Supplier","Category","name","price","qty","warranty","exp","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid",text="P ID")
        self.product_table.heading("Category",text="Category")
        self.product_table.heading("Supplier",text="Supplier")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Qty")
        self.product_table.heading("warranty",text="Warranty")
        self.product_table.heading("exp",text="Exp Date")
        self.product_table.heading("status",text="Status")
    
        self.product_table["show"]="headings"

        self.product_table.column("pid",width=90)
        self.product_table.column("Category",width=100)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=100)
        self.product_table.column("warranty",width=100)
        self.product_table.column("exp",width=100)
        self.product_table.column("status",width=100)
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()
          
    #validation function for expiry date field   
    def validation(self):
        
        if self.var_cat.get()=='Select':
            messagebox.showerror("Error","Please select category",parent=self.root) 
        elif self.var_sup.get()=='':
            messagebox.showerror("Error","Please select supplier",parent=self.root) 
        elif self.var_name.get()=='':
            messagebox.showerror("Error","Please enter product name",parent=self.root) 
        elif self.var_price.get()=='':
            messagebox.showerror("Error","Please enter price of product",parent=self.root) 
        elif self.var_qty.get()=='':
            messagebox.showerror("Error","Please enter quantity",parent=self.root) 
        elif self.var_war.get()=='':
            messagebox.showerror("Error","Please enter warranty period",parent=self.root) 
        elif self.var_exp.get()=='':
            messagebox.showerror("Error","Please enter expiry date",parent=self.root) 
        elif self.var_exp.get()!=None:
            x=self.checkdate(self.var_exp.get())
        
            

        
    #Fetch category & supplier from category and supplier table
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
    
        
            
            
    #Add product function      
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="" or self.var_price.get()=="" or self.var_qty.get()=="" or self.var_exp.get()=="" or self.var_war.get()=="" :
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product Already Available,Try Different",parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Supplier,name,price,qty,warranty,exp,status) values(?,?,?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_war.get(),
                        self.var_exp.get(),
                        self.var_status.get()       
                    ))   
                    con.commit()
                    self.validation()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)  
                    self.show()

        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Show product details function
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    
    
    #Fet product details function
    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_sup.set(row[1])
        self.var_cat.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_war.set(row[6])
        self.var_exp.set(row[7])
        self.var_status.set(row[8])
        
    #Update function  
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        
        try:        
            if self.var_pid.get()=="" :
                messagebox.showerror("Error","Please Select Product",parent=self.root)
            
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,qty=?,warranty=?,exp=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_war.get(),
                        self.var_exp.get(),
                        self.var_status.get(),
                        self.var_pid.get()                   
                    ))   
                    con.commit()
                
                    #self.validation()
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Delete product function
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="" :
                messagebox.showerror("Error","Please Select Product",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Clear details function
    def clear(self):
        self.var_pid.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_war.set("")
        self.var_exp.set("")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    #Search product function
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search Input Should Be Required",parent=self.root)

            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)        
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)       

    #Validation function  
    def checkpriceqty(self,pq):
        if pq.isdigit():
            return True
        if len(str(pq))==0:
            return True
        else:
            messagebox.showerror("Invalid","Invalid Entry",parent=self.root)
            return False

    def checkdate(self,date):
        if len(date)<=10:
            if re.match('(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])',date):
                return True
            else:
                messagebox.showerror("Error",'Wrong Date format example(YYYY-MM-DD)',parent=self.root) 
                return False 
        else:
            messagebox.showerror("Invalid","Date length try to exceed",parent=self.root) 
            return False 

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()
