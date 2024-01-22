import customtkinter
from tkinter import *
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkLabel
import sqlite3
import tkinter as tk
import datetime
from tkcalendar import Calendar
from datetime import datetime
import subprocess
from tkinter import filedialog
from tkinter import ttk

calendar = None



appbg = customtkinter.CTk()
appbg.title('Ice Cream Chilling')
appbg.geometry("550x550")
appbg.config(bg="#25283b")
appbg.resizable(False, False)


conn = sqlite3.connect(r"D:\ice cream py\bills.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY,
        customer_name TEXT,
        bill_date TEXT,
        total_price REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Menu (
        id INTEGER PRIMARY KEY,
        item_name TEXT,
        price REAL,
        image_path BLOB
    )
''')
cursor.execute("SELECT COUNT(*) FROM menu")
count = cursor.fetchone()[0]

if count == 0:
    menu_items = [
            ("ice cream set 1", 50, "icecream1.png"),
            ("ice cream set 2", 50, "icecream2.png"),
            ("ice cream set 3", 50, "icecream3.png"),
            ("ice cream set 4", 50, "icecream4.png"),
            ("ice cream set 5", 50, "icecream5.png"),
            ("ice cream set 6", 50, "icecream6.png"),
            ("ice cream set 7", 50, "icecream7.png"),
            ("ice cream set 8", 50, "icecream8.png"),
            ("ice cream set 9", 50, "icecream9.png"),
            ("ice cream set 10", 50, "icecream10.png"),  
    ]

    cursor.executemany('''
        INSERT INTO menu (item_name, price, image_path)
        VALUES (?, ?, ?)
    ''', menu_items)
    conn.commit()

price_list =[50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
total_price = 0



def insert_bill(customer_name, bill_date, total_price):
    cursor.execute('''
        INSERT INTO bills (customer_name, bill_date, total_price)
        VALUES (?, ?, ?)
    ''', (customer_name, bill_date, total_price))
    conn.commit()


def show_data():
    global calendar, bgadmin_frame, total_price_label,total_price_var

    def refresh_window():
        screen.destroy()  
        show_data()  

    screen = Toplevel(appbg)
    screen.title("App")
    screen.geometry("1500x843")
    screen.configure(bg="white")
    screen.resizable(False, False)
    Label(screen, image=imgbgadmin).pack(expand=True)

    calendar = Calendar(screen)
    calendar.place(x=1195, y=85)

    bgadmin_frame = customtkinter.CTkFrame(screen, width=855, height=900, fg_color="white")
    bgadmin_frame.place(x=42, y=145)
    bgadmin_frame2 = customtkinter.CTkFrame(screen, width=100, height=30, fg_color="white")
    bgadmin_frame2.place(x=65, y=130)

    total_price_var = tk.StringVar()
    total_price_var.set("Total Price for Today: 0 $")
    total_price_label = tk.Label(bgadmin_frame2, textvariable=total_price_var, font=('Arial', 12))
    total_price_label.pack(side="top", pady=(30,0))



    def search_data():
        global total_price_var

       
        widgets = bgadmin_frame.winfo_children()
        for widget in widgets:
            if widget != total_price_label: 
                widget.destroy()

        selected_date_str = calendar.get_date()

        
        selected_date = datetime.strptime(selected_date_str, "%m/%d/%y")

        
        year = selected_date.year
        month = selected_date.month
        day = selected_date.day

        
        formatted_date = f"{year:04d}-{month:02d}-{day:02d}"

        
        conn = sqlite3.connect(r"D:\ice cream py\bills.db")
        cursor = conn.cursor()
        cursor.execute("SELECT customer_name, bill_date, total_price FROM bills WHERE bill_date = ?", (formatted_date,))
        data = cursor.fetchall()
        conn.close()

        total_price_today = 0
        
        
        
        for i, (customer_name, bill_date, total_price) in enumerate(data, start=1):
            bill_info = f"Bill {i} - Customer Name: {customer_name}, Bill Date: {bill_date}, Total Price: {total_price} $"
            bill_label = tk.Label(bgadmin_frame, text=bill_info, font=('Arial', 12))
            bill_label.place(x=10, y=20 + i * 30)  
            total_price_today += total_price

        
        total_price_var.set(f"Total Price for {formatted_date}: {total_price_today} $                                                                                 ")

        

    def calculate_monthly_total():
        global total_price_var, total_price_today

        
        widgets = bgadmin_frame.winfo_children()
        for widget in widgets:
            if widget != total_price_label:  
                widget.destroy()

        selected_date_str = calendar.get_date()

        
        selected_date = datetime.strptime(selected_date_str, "%m/%d/%y")

        
        year = selected_date.year
        month = selected_date.month

       
        formatted_month = f"{year:04d}-{month:02d}"

        
        conn = sqlite3.connect(r"D:\ice cream py\bills.db")
        cursor = conn.cursor()
        cursor.execute("SELECT customer_name, bill_date, total_price FROM bills WHERE strftime('%Y-%m', bill_date) = ?", (formatted_month,))
        data = cursor.fetchall()
        conn.close()

        total_price_monthly = 0

       
        for i, (customer_name, bill_date, total_price) in enumerate(data, start=1):
            bill_info = f"Bill {i} - Customer Name: {customer_name}, Bill Date: {bill_date}, Total Price: {total_price} $"
            bill_label = tk.Label(bgadmin_frame, text=bill_info, font=('Arial', 12))
            bill_label.place(x=10, y=20 + i * 30)
            total_price_monthly += total_price

        
        total_price_var.set(f"Total Price for {formatted_month}: {total_price_monthly} $                                                                                                                               ")

    

    

        
    calculate_monthly_button = tk.Button(screen, text="Calculate Monthly Total",width=20, pady=7, font=font3, command=calculate_monthly_total)
    calculate_monthly_button.place(x=1220, y=350)

    search_button = tk.Button(screen, text="Search",width=10, pady=7, font=font3, command=search_data)
    search_button.place(x=1275, y=300)

    refresh_button = tk.Button(screen, text="Refresh", width=10, pady=7, font=font3, bg='#57a1f8', fg='white', command=refresh_window)
    refresh_button.place(x=1000, y=100)

    editmanu_button = tk.Button(screen, text="Edit Manu", width=10, pady=7, font=font3, bg='#57a1f8', fg='white', command=edit_menu)
    editmanu_button.place(x=1000, y=50)

    backhp_button = tk.Button(screen, text="Back", width=10, pady=7, font=font3, bg='#57a1f8', fg='white', command=lambda: close_and_open_appbg(screen))
    backhp_button.place(x=25, y=25)

    screen.mainloop()

def close_and_open_appbg(screen_to_close):
    screen_to_close.destroy()
    edit_menu()

def close_and_open_appbg(screen):
    screen.destroy()
    appbg.deiconify()

def open_creator_window():
    def close_creator_window():
        creator_window.destroy()

    creator_window = Toplevel()
    creator_window.title("Creator")
    creator_window.geometry("1200x700")
    creator_window.config(bg="#25283b")
    creator_window.resizable(False, False)
    
    pyimage1 = PhotoImage(file="bgcreator.png")
    Label(creator_window, image=pyimage1, bg='white').place(x=0, y=0)
    
    closecreator_Button = Button(creator_window, text='Close', width=20, pady=7, font=font3, bg='#f73e50', fg='white', command=close_creator_window)
    closecreator_Button.place(x=500, y=625)
    
    creator_window.mainloop()

def Admin():
    appbg.withdraw()
    root = Toplevel(appbg)
    root.title("Admin page")
    root.geometry('925x500+300+200')
    root.configure(bg="#fff")
    root.resizable(False, False)
    Img = PhotoImage(file="Ice Cream login.png")
    Label(root, image=Img, bg='white').place(x=50, y=50)

    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Admin', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=125, y=5)

    def on_enter(e):
        user.delete(0, 'end')
    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')


    user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


    def on_enter(e):
        code.delete(0, 'end')
    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    def sign_in():
        username = user.get()
        password = code.get()

        valid_username = "1234"
        valid_password = "1234"

        if username == valid_username and password == valid_password:
            
            root.destroy()
            
            
            show_data()
        else:
            messagebox.showerror('Invalid', "Invalid username or password")
 


    login_Button = Button(frame, text='Login',width=30, pady=7,font=font3, bg='#57a1f8', fg='white', command=sign_in)
    login_Button.place(x=25, y=204)  

    backlogin_Button = Button(frame, text='Back', width=20, pady=7, font=font3, bg='#fa7b14',fg='white', command=lambda: close_and_open_appbg(root))
    backlogin_Button.place(x=75, y=300) 
    
    def close_and_open_appbg(screen):
        
        screen.destroy()
        
        appbg.deiconify()
        
    root.mainloop()



def open_menu():
    appbg.withdraw()
    menu_window = Toplevel()
    menu_window.title('Menu')
    menu_window.geometry('1815x800')
    menu_window.config(bg="#25283b")
    menu_window.resizable(False, False)

    bill_frame = customtkinter.CTkFrame(menu_window, width=310, height=720, fg_color="#3090b1")
    bill_frame.place(x=1150, y=0)


    menu_label = customtkinter.CTkLabel(menu_window, text="Manu", font=font1, text_color="#FFFFFF", bg_color="#25283b")
    menu_label.place(x=540, y=20)
    

    def open_homepage():
        menu_window.withdraw()  
        appbg.deiconify()
    homepage_button = customtkinter.CTkButton(menu_window, command=open_homepage, text="Home page", font=font2, fg_color="#c26406", hover_color="#c26406", corner_radius=20, cursor="hand2")
    homepage_button.place(x=100, y=600)

font1 = ('Arial', 25, 'bold')
font2 = ('Arial', 15, 'bold')
font3 = ('Arial', 12, 'bold')



def update_price_list():
    conn = sqlite3.connect(r"D:\ice cream py\bills.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM menu ORDER BY id")
    prices = cursor.fetchall()
    conn.close()
    
    # Update price_list with the prices from the database
    for i, price in enumerate(prices):
        price_list[i] = price[0]



imgbg = PhotoImage(file="Ice Cream Chilling.png")

imgbgadmin = PhotoImage(file="halloween.png")

qrcodepp= PhotoImage(file="qrcode pp.png")

imgbg_label = customtkinter.CTkLabel(appbg, image=imgbg)
imgbg_label.place(x=0, y=0)




def open_menu():

    appbg.withdraw()
    
    def show_view_menu():
       
        appbg.destroy()
    menu_window = Toplevel()
    menu_window.title('Menu')
    menu_window.geometry('1815x800')
    menu_window.config(bg="#25283b")
    menu_window.resizable(False, False)

    bill_frame = customtkinter.CTkFrame(menu_window, width=310, height=720, fg_color="#3090b1")
    bill_frame.place(x=1150, y=0)


    menu_label = customtkinter.CTkLabel(menu_window, text="Manu", font=font1, text_color="#FFFFFF", bg_color="#25283b")
    menu_label.place(x=540, y=20)

    cursor.execute("SELECT id, item_name, price, image_path FROM menu")
    menu_items = cursor.fetchall()
    
    quantity_comboboxes = []

    # วนซ้ำเพื่อสร้างและวางคอมโบบ็อกซ์ปริมาณ
    for i in range(10):
        quantity_combobox = customtkinter.CTkComboBox(menu_window, font=font3, text_color="#000000", fg_color="#FFFFFF", values=('0', '1', '2', '3', '4', '5'), state="readonly")
        quantity_combobox.place(x=63 + (i % 5) * 220, y=220 + (i // 5) * 230)
        quantity_combobox.set(0)
        quantity_comboboxes.append(quantity_combobox)

    def pay():
        update_price_list()
        if customer_entry.get() == '':
            messagebox.showerror(title="Error", message="Please enter your name.")
        else:
            total_price = 0
           
            
            quantities = [int(combobox.get()) if combobox else 0 for combobox in quantity_comboboxes]

            conn = sqlite3.connect(r"D:\ice cream py\bills.db")
            cursor = conn.cursor()
            
            # ดึงราคาสำหรับรายการที่เลือกจากฐานข้อมูล
            for i in range(1, 11):
                cursor.execute("SELECT price FROM menu WHERE id = ?", (i,))
                price = cursor.fetchone()[0]
                total_price += quantities[i - 1] * price
            
            conn.close()

            if total_price == 0:
                messagebox.showerror(title="Error", message="Please select some dishes.")
            else:
                customer_name = customer_entry.get()
                bill_date = date.today()
                
                #ใส่บิลเข้าฐานข้อมูล
                insert_bill(customer_name, bill_date, total_price)

                name_label = customtkinter.CTkLabel(bill_frame, text=f'Customer Name: {customer_name}', font=font3,
                                                bg_color="#3090b1", width=320, anchor=W)
                name_label.place(x=10, y=0)

                price_label = customtkinter.CTkLabel(bill_frame, text=f'Total Price: {total_price} $', font=font3,
                                                bg_color="#3090b1", width=320, anchor=W)
                price_label.place(x=10, y=590)

                date_label = customtkinter.CTkLabel(bill_frame, text=f'Bill Data: {bill_date}', font=font3,
                                                bg_color="#3090b1", width=320, anchor=W)
                date_label.place(x=10, y=610)

                qrcodepp_label = customtkinter.CTkLabel(menu_window, image=qrcodepp)
                qrcodepp_label.place(x=1185, y=350)

                ordered_items = []
                for i in range(1, 11):
                    quantity = quantities[i - 1]
                    if quantity > 0:
                        item_name = f"ice cream set {i}"
                        ordered_items.append(f"{item_name}: {quantity} x {price_list[i-1]}$ = {quantity * price_list[i-1]}$")

        
                ordered_items_label = customtkinter.CTkLabel(bill_frame, text="Ordered Items:", font=font3, bg_color="#3090b1", width=320, anchor=W)
                ordered_items_label.place(x=10, y=30)

                y_offset = 50
                for item in ordered_items:
                    ordered_item_label = customtkinter.CTkLabel(bill_frame, text=item, font=font3, bg_color="#3090b1", width=320, anchor=W)
                    ordered_item_label.place(x=10, y=y_offset)
                    y_offset += 20

            
                customer_name = customer_entry.get()
                bill_data = date.today()
                bill_filename = f"{customer_name}Bill.txt"

                with open(bill_filename, 'w') as bill_file:
                    bill_file.write(f'Ice Cream Chilling\nCustomer Name: {customer_name}\n')
                    bill_file.write(f'Bill Data: {bill_data}\n')
                    bill_file.write(f'Total Price:{total_price} $\n')
                    bill_file.write("Ordered Items:\n")
                    
                    for item in ordered_items:
                        bill_file.write(f'{item}\n')

                messagebox.showinfo(title="Saved", message=f"Bill has been saved as {bill_filename}")
                
                bill_filename = f"{customer_name}Bill.txt"
                subprocess.Popen(['notepad.exe', bill_filename])

    def new():
    
        menu_window.destroy()
    
   
        open_menu()
       
    
    menu_items = cursor.execute('SELECT item_name, price, image_path FROM menu').fetchall()

#สร้างรายการจัดเก็บป้ายเมนู
    menu_labels = []

    # สร้างวัตถุ CTkLabel สำหรับแต่ละรายการเมนู
    for i, (item_name, price, image_path) in enumerate(menu_items):
        img_label = customtkinter.CTkLabel(
            menu_window,
            text=f"{item_name}\n Price: {price}$",
            font=font2,
            text_color="#FFFFFF",
            fg_color="#090b17",
            width=200,
            height=200,
            corner_radius=20,
            compound=TOP,
            anchor=N
        )
        
        # โหลดรูปภาพสำหรับรายการเมนูโดยใช้ image_path จากฐานข้อมูล
        img = PhotoImage(file=image_path)
        img_label.configure(image=img)
        img_label.img = img  # เก็บการอ้างอิงถึงรูปภาพเพื่อป้องกันไม่ให้ถูกเก็บขยะ
        
        img_label.place(x=30 + (i % 5) * 220, y=70 + (i // 5) * 230)
        
        menu_labels.append(img_label)

        quantity_comboboxes = []  # เพิ่มบรรทัดนี้เพื่อสร้างลิสต์ของ CTkComboBox

        
        # สร้างวัตถุ CTkLabel สำหรับแต่ละรายการเมนู
        for i, (item_name, price, image_path) in enumerate(menu_items):
            # ตรวจสอบว่าราคามากกว่า 0 หรือไม่
            if price > 0:
                label_text = f"{item_name}\n Price: {price}$"
            else:
                label_text = item_name

            img_label = customtkinter.CTkLabel(
                menu_window,
                text=label_text,
                font=font2,
                text_color="#FFFFFF",
                fg_color="#090b17",
                width=200,
                height=200,
                corner_radius=20,
                compound=TOP,
                anchor=N
            )

            # โหลดรูปภาพสำหรับรายการเมนูโดยใช้ image_path จากฐานข้อมูล
            img = PhotoImage(file=image_path)
            img_label.configure(image=img)
            img_label.img = img  # เก็บการอ้างอิงถึงรูปภาพเพื่อป้องกันไม่ให้ถูกเก็บขยะ

            img_label.place(x=30 + (i % 5) * 220, y=70 + (i // 5) * 230)

            menu_labels.append(img_label)


            # สร้างและวางคอมโบบ็อกซ์ปริมาณเฉพาะในกรณีที่ราคามากกว่า 0
            if price > 0:
                quantity_combobox = customtkinter.CTkComboBox(
                    menu_window,
                    font=font3,
                    text_color="#000000",
                    fg_color="#FFFFFF",
                    values=('0', '1', '2', '3', '4', '5'),
                    state="readonly"
                )
                quantity_combobox.place(x=63 + (i % 5) * 220, y=220 + (i // 5) * 230)
                quantity_combobox.set(0)
                quantity_comboboxes.append(quantity_combobox)
            else:
                quantity_comboboxes.append(None)

            # Create and place quantity comboboxes
            # quantity_combobox = customtkinter.CTkComboBox(
            #     menu_window,
            #     font=font3,
            #     text_color="#000000",
            #     fg_color="#FFFFFF",
            #     values=('0', '1', '2', '3', '4', '5'),
            #     state="readonly"
            # )
            # quantity_combobox.place(x=63 + (i % 5) * 220, y=220 + (i // 5) * 230)
            # quantity_combobox.set(0)
            # quantity_comboboxes.append(quantity_combobox)



    customer_label = customtkinter.CTkLabel(menu_window, text="Customer Name:", font=font2, text_color="#FFFFFF", fg_color="#25283b")
    customer_label.place(x=345, y=550)

    customer_entry = customtkinter.CTkEntry(menu_window, font=font2, fg_color="#FFFFFF", text_color="#000000", width=300)
    customer_entry.place(x=470, y=550)

    pay_button = customtkinter.CTkButton(menu_window,command=pay, text="Pay Bill", font=font2, fg_color="#ad0c78", hover_color="#ad0c78", corner_radius=20, cursor="hand2")
    pay_button.place(x=470, y=600)
   
    new_button = customtkinter.CTkButton(menu_window,command=new, text="New Bill", font=font2, fg_color="#c26406", hover_color="#c26406", corner_radius=20, cursor="hand2")
    new_button.place(x=625, y=600)
    
    def open_homepage():
        menu_window.withdraw()  
        appbg.deiconify()
    homepage_button = customtkinter.CTkButton(menu_window, command=open_homepage, text="Home page", font=font2, fg_color="#c26406", hover_color="#c26406", corner_radius=20, cursor="hand2")
    homepage_button.place(x=100, y=600)
   
def browse_image(entry_widget):
    file_path = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("Image files", "*.jpg *.png *.gif"), ("all files", "*.*")))
    entry_widget.delete(0, END)  
    entry_widget.insert(0, file_path)



def delete_menu(menu_id, item_frame, item_name_entries, price_entries, image_path_entries, delete_buttons):
    conn = sqlite3.connect(r"D:\ice cream py\bills.db")
    cursor = conn.cursor()

    # รับรายละเอียดรายการก่อนที่จะลบ
    cursor.execute("SELECT item_name, price FROM menu WHERE id=?", (menu_id,))
    deleted_item = cursor.fetchone()

    # อัปเดตชื่อรายการ ราคา และรูปภาพให้ว่างเปล่า (หรือค่าเริ่มต้นที่คุณต้องการ)
    cursor.execute("UPDATE menu SET item_name='', price=0, image_path='' WHERE id=?", (menu_id,))

    #ยอมรับการเปลี่ยนแปลง
    conn.commit()

   #ปิดการเชื่อมต่อ
    conn.close()

    # อัปเดตการอ้างอิงไปยังวิดเจ็ตรายการและปุ่มลบ
    item_name_entries[menu_id - 1].delete(0, END)
    price_entries[menu_id - 1].delete(0, END)
    image_path_entries[menu_id - 1].delete(0, END)

    # ตั้งราคาเข้าเป็น 0
    price_entries[menu_id - 1].insert(0, 0)
 
    #อัพเดทแถวและคอลัมน์รายการที่เหลือ
    for i, (item_name_entry, price_entry, image_path_entry, delete_button) in enumerate(
            zip(item_name_entries, price_entries, image_path_entries, delete_buttons)):
        row = i // 5
        column = i % 5

        item_name_entry.grid(row=row * 4, column=column * 3 + 1)
        price_entry.grid(row=row * 4 + 1, column=column * 3 + 1)
        image_path_entry.grid(row=row * 4 + 2, column=column * 3 + 1)
        delete_button.grid(row=row * 4 + 3, column=column * 3)



        conn.commit()
        
        #ปิดการเชื่อมต่อ
        conn.close()
    



def edit_menu():
    edit_window = Toplevel()
    edit_window.title('Edit Menu')
    edit_window.geometry('1300x250')
    
    conn = sqlite3.connect(r"D:\ice cream py\bills.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    
    item_name_entries = []
    price_entries = []
    image_path_entries = []

    delete_buttons = []  # เพิ่มรายการเพื่อเก็บปุ่มลบ

    def save_changes():
        update_price_list()
        conn = sqlite3.connect(r"D:\ice cream py\bills.db")
        cursor = conn.cursor()

        for i in range(len(item_name_entries)):
            new_item_name = item_name_entries[i].get()
            new_price = price_entries[i].get()
            new_image_path = image_path_entries[i].get()

            cursor.execute("UPDATE menu SET item_name = ?, price = ?, image_path = ? WHERE id = ?",
                        (new_item_name, new_price, new_image_path, i + 1))

        conn.commit()
        conn.close()
        edit_window.destroy()

    for i, (id, item_name, price, image_path) in enumerate(menu_items):
        item_frame = Frame(edit_window)
        item_frame.grid(row=i // 5, column=i % 5)

        image_path_label = Label(item_frame, text="Image Path:")
        image_path_label.grid(row=2, column=0)
        image_path_entry = Entry(item_frame)
        image_path_entry.grid(row=2, column=1)
        image_path_entry.insert(0, image_path)
        image_path_entries.append(image_path_entry)

        browse_button = Button(item_frame, text="Browse", command=lambda entry=image_path_entry: browse_image(entry))
        browse_button.grid(row=2, column=2)

        item_name_label = Label(item_frame, text="Item Name:")
        item_name_label.grid(row=0, column=0)
        item_name_entry = Entry(item_frame)
        item_name_entry.grid(row=0, column=1)
        item_name_entry.insert(0, item_name)
        item_name_entries.append(item_name_entry)

        price_label = Label(item_frame, text="Price:")
        price_label.grid(row=1, column=0)
        price_entry = Entry(item_frame)
        price_entry.grid(row=1, column=1)
        price_entry.insert(0, price)
        price_entries.append(price_entry)
        
        # def add_new_item():
        #     item_frame = Frame(edit_window)
        #     item_frame.grid(row=(len(menu_items) // 5), column=(len(menu_items) % 5))

        #     image_path_label = Label(item_frame, text="Image Path:")
        #     image_path_label.grid(row=2, column=0)
        #     image_path_entry = Entry(item_frame)
        #     image_path_entry.grid(row=2, column=1)
        #     image_path_entries.append(image_path_entry)

        #     browse_button = Button(item_frame, text="Browse", command=lambda entry=image_path_entry: browse_image(entry))
        #     browse_button.grid(row=2, column=2)

        #     item_name_label = Label(item_frame, text="Item Name:")
        #     item_name_label.grid(row=0, column=0)
        #     item_name_entry = Entry(item_frame)
        #     item_name_entry.grid(row=0, column=1)
        #     item_name_entries.append(item_name_entry)

        #     price_label = Label(item_frame, text="Price:")
        #     price_label.grid(row=1, column=0)
        #     price_entry = Entry(item_frame)
        #     price_entry.grid(row=1, column=1)
        #     price_entries.append(price_entry)

        # add_item_button = Button(edit_window, text="Add New Item", command=add_new_item)
        # add_item_button.grid(row=5, column=0, columnspan=5)
        # เพิ่มปุ่มลบ
        delete_button = Button(item_frame, text="Delete", command=lambda menu_id=i + 1, frame=item_frame, item_name_entries=item_name_entries, price_entries=price_entries, image_path_entries=image_path_entries, delete_buttons=delete_buttons: delete_menu(menu_id, frame, item_name_entries, price_entries, image_path_entries, delete_buttons))
        delete_button.grid(row=3, column=0)
        delete_buttons.append(delete_button)

    save_button = Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=(len(menu_items) // 5), column=0, columnspan=5)
    
    conn.close()

creator_button = customtkinter.CTkButton(appbg, text="Creator", command=open_creator_window, font=font2, fg_color="#c435fc", hover_color="#25b1db", corner_radius=0, cursor="hand2")
creator_button.place(x=200, y=390)

admin_button =customtkinter.CTkButton(appbg, command=Admin, text="Admin", font=font2, fg_color="#2e79db", hover_color="#e82056", corner_radius=0, cursor="hand2") 
admin_button.place(x=200, y=500)
   
home_button = customtkinter.CTkButton(appbg, text="View menu", command=open_menu, font=font2, fg_color="#f2c216", hover_color="#f76874", corner_radius=0, cursor="hand2")
home_button.place(x=200, y=350)

appbg.mainloop()
