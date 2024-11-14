# Import necessary modules from tkinter and other libraries
from tkinter import *  # Basic GUI functionalities
import time  # To use time-related functions
import ttkthemes  # For themed tkinter windows
from tkinter import ttk, messagebox, filedialog  # For advanced tkinter widgets
import pymysql
import pandas

def iexit():
    result=messagebox.askyesno("Confirm", "Do you want to exit")
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfile(defaultextension=".csv")
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content["values"]
        newlist.append(datalist)

    table=pandas.DataFrame(newlist, columns=["Id", "Name", "Mobile", "Email", "Address", "Gender", "D.O.B", "Added Date", "Added Time"])
    table.to_csv(url, index=False)
    messagebox.showinfo("Success","Data is Saved successfully")
    
    
def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    
    screen=Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(0,0)
    
    idLabel=Label(screen, text="Id", font=("Times new roman", 20, "bold"))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry=Entry(screen, font=("roman", 15, "bold"), width=24)
    idEntry.grid(row=0, column=1, padx=10)

    nameLabel=Label(screen, text="Name", font=("Times new roman", 20, "bold"))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry=Entry(screen, font=("roman", 15, "bold"), width=24)
    nameEntry.grid(row=1, column=1, padx=10)
    
    phoneLabel=Label(screen, text="Phone", font=("Times new roman", 20, "bold"))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry=Entry(screen, font=("roman", 15, "bold"), width=24)
    phoneEntry.grid(row=2, column=1, padx=10)
    
    emailLabel=Label(screen, text="Email ID", font=("Times new roman", 20, "bold"))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry=Entry(screen, font=("roman", 15, "bold"), width=24)
    emailEntry.grid(row=3, column=1, padx=10)
    
    addressLabel=Label(screen, text="Address", font=("Times new roman", 20, "bold"))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry=Entry(screen, font=("roman", 15, "bold"), width=24)
    addressEntry.grid(row=4, column=1, padx=10)
    
    genderLabel=Label(screen, text="Gender", font=("Times new roman", 20, "bold"))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry=Entry(screen, font=("roman", 15, "bold"), width=24)
    genderEntry.grid(row=5, column=1, padx=10)
    
    dobLabel=Label(screen, text="D.O.B", font=("Times new roman", 20, "bold"))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry=Entry(screen, font=("roman", 15, "bold"))
    dobEntry.grid(row=6, column=1, padx=10)
    
    student_button=Button(screen, text= button_text,  font=("Times new roman", 20, "bold"), width=24, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

    if title=="Update Student":
    
        indexing=studentTable.focus()
        
        content=studentTable.item(indexing)
        listdata=content['values']
        
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0,  listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


    
def update_data():
    date = time.strftime(r'%Y/%m/%d')  # Get current date in dd/mm/yy format
    currenttime = time.strftime('%H:%M:%S')  # Get current time in hh:mm:ss format
    
    query="update student set name=%s ,mobile_no=%s, email_id=%s, address=%s, gender=%s, date_of_birth=%s, date=%s, time=%s where id=%s"
    
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
    
    con.commit()
    messagebox.showinfo("Success",f"id {idEntry.get()} is modified successfully", parent=screen)
    
    screen.destroy()
    show_student()



def show_student():
    query="select * from student"
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', 'end', values=data)

def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content["values"][0]
    query="delete from student where id=%s"
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo("Deleted", f"Id {content_id} is deleted succesfully")
    query="select * from student"
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert("", END, values=data)
    

    
def search_data():
    query="select * from student where id =%s or name=%s or Mobile_No =%s or Email_ID=%s or address=%s or gender=%s "
    mycursor.execute(query, (idEntry.get(), nameEntry.get(),  phoneEntry.get(),emailEntry.get(), addressEntry.get(), genderEntry.get()))
    
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)
        




def add_data():
    if idEntry.get()==""or nameEntry.get() =="" or phoneEntry.get()==""or emailEntry.get()=="" or addressEntry.get()=="" or genderEntry.get() ==""or dobEntry.get()=="":
        messagebox.showerror("Error", "All Feilds are required", parent=screen)
    
    else:
        date = time.strftime(r'%Y/%m/%d')  # Get current date in dd/mm/yy format
        currenttime = time.strftime('%H:%M:%S')  # Get current time in hh:mm:ss format
        try:
            query="insert into student values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"  
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            result=messagebox.askyesno("confirm","Data Added successfullly. Do you want to clean the form?", parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror("Error", "Id cannot be repeated", parent=screen)
            return
            
            
        query="select * from student"
        mycursor.execute(query)
        fectch_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fectch_data:
            datalist=list(data)
            studentTable.insert("",END, values=datalist)

                

def connect_database():
   
    
    def connect():
        
        global mycursor,con
        try:
            con=pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor=con.cursor()
            
        
        except:
            messagebox.showerror("Error", "Invalid Details", parent=connectWindow)   
            return      
        
        try:
            
            query="create database studentmanagementsystem"
            mycursor.execute(query)
        
            query="use studentmanagementsystem"
            mycursor.execute(query)
        
            query="create table student(Id int not null primary key, Name varchar(30), Mobile_No varchar(10), Email_Id varchar(30), Address varchar(100), Gender varchar(20), Date_Of_Birth varchar(15), Date date, Time time);"
            mycursor.execute(query)
            
        except:
            query="use studentmanagementsystem"
            mycursor.execute(query)
        
        messagebox.showinfo("Success","Database Connection is successful..", parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state="NORMAL")
        searchstudentButton.config(state="NORMAL")
        updatestudentButton.config(state="NORMAL")
        showstudentButton.config(state="NORMAL")
        exportstudentButton.config(state="NORMAL")
        deletestudentButton.config(state="NORMAL")     

    
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry("470x250+730+230")
    connectWindow.title("Database connection")
    connectWindow.resizable(0,0)
    
    hostnamelabel=Label(connectWindow, text="Host Name", font=("arial", 20, "bold"))
    hostnamelabel.grid(row=0, column=0, padx=20)
    hostEntry=Entry(connectWindow, font=("roman", 15, "bold"), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)
    
    usernamelabel=Label(connectWindow, text="User Name", font=("arial", 20, "bold"))
    usernamelabel.grid(row=1, column=0, padx=20)
    usernameEntry=Entry(connectWindow, font=("roman", 15, "bold"), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)
    
    passwordlabel=Label(connectWindow, text="Password", font=("arial", 20, "bold"))
    passwordlabel.grid(row=2, column=0, padx=20)
    passwordEntry=Entry(connectWindow, font=("roman", 15, "bold"), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)
    
    connectButton=ttk.Button(connectWindow, text="Connect", command= connect)
    connectButton.grid(row=3, columnspan=2)


# Function to update the clock every second
def clock():
    global date,currenttime
    date = time.strftime(r'%d/%m/%Y')  # Get current date in dd/mm/yy format
    currenttime = time.strftime('%H:%M:%S')  # Get current time in hh:mm:ss format
    datetimeLabel.config(text=f"Date: {date}\nTime: {currenttime}")  # Update label with date and time
    datetimeLabel.after(1000, clock)  # Call this function every 1 second (1000ms)

# Variables and function for sliding text
count = 0  # Counter to track character position
text = ""  # Variable to store current sliding text

# Function to display sliding text effect
def slider():
    global text, count  # Access global variables
    if count == len(s):  # Reset if end of text is reached
        count = 0
        text = ""  # Reset text to empty
    text = text + s[count]  # Append current character to text
    sliderLabel.config(text=text)  # Update label with the new text
    count += 1  # Move to the next character
    sliderLabel.after(250, slider)  # Call this function every 250ms


# Create the main application window using ttkthemes
root = ttkthemes.ThemedTk()  # Initialize themed tkinter window
root.get_themes()  # Get available themes
root.set_theme("radiance")  # Set theme to 'radiance'

# Set window geometry and properties
root.geometry("1174x680+0+0")  # Set window size and position
root.resizable(0, 0)  # Disable window resizing
root.title("Student Management System Created by Avinash")  # Set window title

# Label to display current date and time
datetimeLabel = Label(root, font=("times new roman", 18, "italic bold"))  # Configure label style
datetimeLabel.place(x=5, y=5)  # Place label at specific coordinates
clock()  # Start the clock function

# Label to display sliding text
s = "Student Management System"  # Text to slide
sliderLabel = Label(root, text=s, font=("arial", 18, "bold"), width=30)  # Configure label style and size
sliderLabel.place(x=200, y=0)  # Place label at specific coordinates
slider()  # Start the slider function

# Button to connect to the database
connectButton = ttk.Button(root, text="Connect database", command=connect_database)  # Create button with text
connectButton.place(x=980, y=0)  # Place button at specific coordinates

# Frame on the left side to hold buttons and image
leftFrame = Frame(root)  # Create a frame widget
leftFrame.place(x=50, y=80, width=300, height=600)  # Place frame at specific coordinates

# Add an image above the 'Add Student' button
logo_image = PhotoImage(file=r"C:\Users\Abhinash Kumar\Downloads\students (1).png")  # Load image
logoLabel = Label(leftFrame, image=logo_image)  # Create a label to hold the image
logoLabel.grid(row=0, column=0)  # Place the image in the frame using grid layout

# Buttons for various student operations
addstudentButton = ttk.Button(leftFrame, text="Add Student", width=20, state=DISABLED, command=lambda :toplevel_data("Add Student", "Add", add_data))  # 'Add Student' button
addstudentButton.grid(row=1, column=0, pady=15)  # Place button with padding

searchstudentButton = ttk.Button(leftFrame, text="Search Student", width=20, state=DISABLED, command=lambda :toplevel_data("Search Student", "Search",search_data))  # 'Search Student' button
searchstudentButton.grid(row=2, column=0, pady=15)  # Place button with padding

updatestudentButton = ttk.Button(leftFrame, text="Update Student", width=20, state=DISABLED, command=lambda :toplevel_data("Update Student", "Update",update_data))  # 'Update Student' button
updatestudentButton.grid(row=3, column=0, pady=15)  # Place button with padding

deletestudentButton = ttk.Button(leftFrame, text="Delete Student", width=20, state=DISABLED, command=delete_student)  # 'Delete Student' button
deletestudentButton.grid(row=4, column=0, pady=15)  # Place button with padding

showstudentButton = ttk.Button(leftFrame, text="Show Student", width=20, state=DISABLED, command=show_student)  # 'Show Student' button
showstudentButton.grid(row=5, column=0, pady=15)  # Place button with padding

exportstudentButton = ttk.Button(leftFrame, text="Export data", width=20, state=DISABLED, command=export_data)  # 'Export Data' button
exportstudentButton.grid(row=6, column=0, pady=15)  # Place button with padding

exitstudentButton = ttk.Button(leftFrame, text="Exit", width=20, command=iexit)  # 'Exit' button
exitstudentButton.grid(row=7, column=0, pady=15)  # Place button with padding

# Frame on the right side to display student data
rightFrame = Frame(root)  # Create a frame widget
rightFrame.place(x=350, y=80, width=820, height=600)  # Place frame at specific coordinates

# Horizontal scrollbar for the student table
scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)  # Create horizontal scrollbar
scrollBarX.pack(side=BOTTOM, fill=X)  # Place it at the bottom of the frame

# Vertical scrollbar for the student table
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)  # Create vertical scrollbar
scrollBarY.pack(side=RIGHT, fill=Y)  # Place it on the right side of the frame

# Create a table to display student information
studentTable = ttk.Treeview(
    rightFrame,
    columns=("Id", "Name", "Mobile No", "Email Id", "Address", "Gender", "D.O.B", "Added Date", "Added Time"),
    xscrollcommand=scrollBarX.set,  # Link horizontal scrollbar
    yscrollcommand=scrollBarY.set  # Link vertical scrollbar
)
studentTable.pack(fill=BOTH, expand=1)  # Make the table fill the frame

# Configure scrollbars to work with the table
scrollBarX.config(command=studentTable.xview)  # Link horizontal scrollbar with table
scrollBarY.config(command=studentTable.yview)  # Link vertical scrollbar with table

# Define table headings
studentTable.heading('Id', text="Id")  # Column for student ID
studentTable.heading('Name', text="Name")  # Column for student name
studentTable.heading("Mobile No", text="Mobile No")  # Column for mobile number
studentTable.heading('Email Id', text="Email Id")  # Column for email ID
studentTable.heading('Address', text="Address")  # Column for address
studentTable.heading('Gender', text="Gender")  # Column for gender
studentTable.heading('D.O.B', text="B.O.B")  # Column for date of birth
studentTable.heading('Added Date', text="Added Date")  # Column for added date
studentTable.heading('Added Time', text="Added Time")  # Column for added time


studentTable.column("Id", width=50, anchor=CENTER)
studentTable.column("Name", width=300)
studentTable.column("Mobile No", width=200, anchor=CENTER)
studentTable.column("Email Id", width=300, anchor=CENTER)
studentTable.column("Address", width=300, anchor=CENTER)
studentTable.column("Gender", width=100, anchor=CENTER)
studentTable.column("D.O.B", width=100, anchor=CENTER)
studentTable.column("Added Date", width=200, anchor=CENTER)
studentTable.column("Added Time", width=200, anchor=CENTER)


style=ttk.Style()
style.configure("Treeview", rowheight=40, font=("arial", 12, "bold"),  background="white", fieldbackground="white")

style.configure("Treeview.Heading", font=("arial",14,"bold"), foreground="red")

# Show only the defined headings (no extra column)
studentTable.config(show="headings")

# Start the main event loop
root.mainloop()  # Keeps the window open until closed by the user
