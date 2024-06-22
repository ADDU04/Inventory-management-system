from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(0,0)

        #===Variables===
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #==Title===
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
 
        #Content of category window
        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)
        
        #Buttons
        btn_add=Button(self.root,text="Add",command=self.add,font=("goudy old style",18),bg="green",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",18),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)
        
        #Category frame
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=120)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)
        
        #Category table
        self.category_table=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid",text=" C ID")
        self.category_table.heading("name",text="Name")
      
        self.category_table["show"]="headings"

        self.category_table.column("cid",width=90)
        self.category_table.column("name",width=100)
       
        self.category_table.pack(fill=BOTH,expand=1)
        self.category_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        
        #Images
        self.im1=Image.open("Images/cat1.jpeg")
        self.im1=self.im1.resize((500,250),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("Images/phone.jpg")
        self.im2=self.im2.resize((500,250),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)


    #Add category function
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="" :
                messagebox.showerror("Error","Please enter category name",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error"," Category Already Present ,Try Different",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)",(self.var_name.get(),))   
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root) 
                    self.show() 
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   

    #Show category name , id in category table function
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert('',END,values=row)
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    

    #get category name id in cateory table function
    def get_data(self,ev):
        f=self.category_table.focus()
        content=(self.category_table.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
    
    #Delete category function
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="" :
                messagebox.showerror("Error","Please Select Category ",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error,Please Try Again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   





if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()        