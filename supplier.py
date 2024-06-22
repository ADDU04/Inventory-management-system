from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image,ImageTk
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(0,0)

        #===All Variables===
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()


        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        #==OPtions===
        lbl_search=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)
 
        #calling Check contact function for contact field
        validate=self.root.register(self.checkcontactInvoice)
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow",validate='key',validatecommand=(validate,"%P")).place(x=800,y=80,width=160)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=980,y=79,width=110,height=28)
        
        #====Title===
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)


        #===Content===
        #===Row1===
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow",validate='key',validatecommand=(validate,"%P")).place(x=180,y=80,width=180)
        
        #====Row2=====

        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #===Row3===
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow",validate='key',validatecommand=(validate,"%P")).place(x=180,y=160,width=180)

        #limitsize function for contact
        def limitSize(*args):
            value =self.var_contact.get()
            if len(value) > 10: self.var_contact.set(value[:10])
    
        self.var_contact.trace('w', limitSize)

        #===Row4====
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
        
        
        #Buttons===
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_udate=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)        
        
        #===Supplier Details table frame=====

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=160)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        
        #Image
        self.im=Image.open("Images/great.png")
        self.im=self.im.resize((380,200),Image.ANTIALIAS)
        self.im=ImageTk.PhotoImage(self.im)
        self.lbl_im=Label(self.root,image=self.im,bd=2,relief=RAISED)
        self.lbl_im.place(x=700,y=290)
         
        #Supplier table
        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")
        
        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
    
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

#===========================================All functions===============================================
    
    #Add supplier function
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="" or  self.var_name.get()=="" or self.var_contact.get()=="":
                messagebox.showerror("Error","All fields are Required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error"," This Invoice No. Already Assigned ,Try Different",parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                                        
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
        
    #Show supplier function
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    

    #Get supplier details function
    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    #Update supplier function    
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="" :
                messagebox.showerror("Error","Please select supplier",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_sup_invoice.get()
                    ))   
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)  
                    self.show()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Delete supplier function 
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="" :
                messagebox.showerror("Error","Please select supplier",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Clear function
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()
    
    #Search function
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. Required",parent=self.root)

            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                rows=cur.fetchall()
                if rows!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)        
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    #Validation function
    def checkcontactInvoice(self,contact):
        if contact.isdigit():
            return True
        if len(str(contact))==0:
            return True
        else:
            messagebox.showerror("Invalid","Invalid Entry",parent=self.root)
            return False

if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()
