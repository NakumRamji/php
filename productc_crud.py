from tkinter import *
import mariadb as sql
from tkinter import ttk

class con:
    def __init__(self) -> None:
        try:
            # Connect to the MySQL server
            self.db = sql.connect(host="localhost", username="root", password="")
            self.cur = self.db.cursor()
            # Create database if it doesn't exist
            self.cur.execute("CREATE DATABASE IF NOT EXISTS productdb")
            # Connect to the 'college' database
            self.db = sql.connect(host="localhost", username="root", password="", database="productdb")
            self.cur = self.db.cursor()
            # Fix typo in table creation: 'table stud' -> 'stud'
            self.cur.execute("CREATE TABLE IF NOT EXISTS product (pid INT, productname VARCHAR(100), price double,quantity INT ")
        except sql.Error as e:
            print(f"Error: {e}")

    def ins(self):
        try:
            # Use parameterized query to prevent SQL injection
            self.cur.execute("INSERT INTO product (pid, productname, price, quantity) VALUES (%s, %s, %s, %s)", 
                             (pid.get(), pname.get(), price.get(),quantity.get()))
            self.db.commit()
            self.show()
            self.clear()
        except sql.Error as e:
            print(f"Error: {e}")

    def upd(self):
        try:
            # Use parameterized query for update
            self.cur.execute("UPDATE product  SET pname=%s, price=%s,  quantity=%s WHERE pid=%s", 
                             (pid.get(), pname.get(), price.get(),quantity.get()))

            self.db.commit()
            self.show()
            self.clear()
        except sql.Error as e:
            print(f"Error: {e}")

    def dele(self):
        try:
            # Use parameterized query for delete
            self.cur.execute("DELETE FROM product  WHERE pid=%s", (pid.get(),))
            self.db.commit()
            self.show()
            self.clear()
        except sql.Error as e:
            print(f"Error: {e}")

    def show(self):
        
        try:
            self.cur.execute("SELECT * FROM product ")
            data = self.cur.fetchall()  # Corrected typo: fatchall -> fetchall
            for child in lv.get_children():
                lv.delete(child)
            for i, (pid, pname, price, quantity) in enumerate(data, start=1):
                lv.insert("", "end", values=(pid, pname, price, quantity))
        except sql.Error as e:
            print(f"Error: {e}")

    def clear(self):
        pid.delete(0, END)  # Use END instead of len(uid.get())
        pname.delete(0, END)
        price.delete(0, END)
        quantity.delete(0, END)

global pid,pname,price,quantity

#gui
ob = con()
top = Tk()
top.geometry("500x500")

pid = Entry(top, width=20)
pid.place(x=120, y=30)

pname = Entry(top, width=20)
pname.place(x=120, y=60)

price = Entry(top, width=20)
price.place(x=120, y=90)

quantity= Entry(top, width=20)
quantity.place(x=120, y=120)

lb = Label(top, text="P_Id:")
lb.place(x=20, y=30)
lb = Label(top, text="P_Name:")
lb.place(x=20, y=60)
lb = Label(top, text="Price:")
lb.place(x=20, y=90)
lb = Label(top, text="Quntity:")
lb.place(x=20, y=120)

add = Button(top, text="Insert", width=10, bg="green",command=ob.ins)
add.place(x=10, y=150)
upd = Button(top, text="Update", width=10, bg="blue",command=ob.upd)
upd.place(x=110, y=150)
dele = Button(top, text="Delete", width=10, bg="red",command=ob.dele)
dele.place(x=210, y=150)

columns = ["P_Id", "P_Name", "Price","Quntity"]  # Corrected variable name: column -> columns
lv = ttk.Treeview(top, columns=columns, show="headings",height=15)
for col in columns:  # Corrected variable name: column -> col
    lv.heading(col, text=col)
    lv.column(col, width=100, anchor="center")
lv.place(x=40, y=180,width=420, height=300)

ob.show()

top.mainloop()


