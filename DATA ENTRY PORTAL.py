from tkinter import *
import sqlite3

root = Tk()
root.title("Data Entry App")
root.iconbitmap("C:/Users/USER/Documents/PYTHON PROJECTS/Icons/coffee_icon.ico")

#DATABASE

#Connecting to/Creating Database
conn = sqlite3.connect("biodata.db")

#Defining Cursor Variable
c = conn.cursor()

#Delete Existing Patient Bio Table because this is project is just for demonstration purposes
c.execute("DROP TABLE IF EXISTS patient_bio")

#Creating a new Patient Bio Data Table
c.execute("""CREATE TABLE patient_bio(
            first_name text,
            last_name text,
            age integer,
            genotype text,
            gender text
            )
            """)

#Updating Changes to the Database
conn.commit()

#Closing connection
conn.close()

#Frame of Bio Data
entry_frame = LabelFrame(root, text = "Bio-Data", padx = 10, pady = 10)
entry_frame.grid(row = 0, column = 0, padx = 30, pady = 10)

#Frame for Gender Radios
gender_frame = LabelFrame(root, text = "Gender", padx = 10, pady = 10)
gender_frame.grid(row = 0, column = 1, padx = 30, pady = 20)

#Bio Data Field Entry Boxes
f_name = Entry(entry_frame, width = 30)
f_label = Label(entry_frame, text = "First Name: ")
f_label.grid(row = 0, column = 0)
f_name.grid(row = 0, column = 1, pady = 10)

l_name = Entry(entry_frame, width = 30)
l_label = Label(entry_frame, text = "Last Name: ")
l_label.grid(row = 1, column = 0, pady = 10)
l_name.grid(row = 1, column = 1)

age = Entry(entry_frame, width = 30)
age_label = Label(entry_frame, text = "Age: ")
age_label.grid(row = 2, column = 0, pady = 10)
age.grid(row = 2, column = 1)

genotype = Entry(entry_frame, width = 30)
gen_label = Label(entry_frame, text = "Genotype: ")
gen_label.grid(row = 3, column = 0, pady = 10)
genotype.grid(row = 3, column = 1)

query_label = Label(root, text = "Records displayed Here...", relief = SUNKEN)
query_label.grid(row = 2, column = 0, columnspan = 2, pady = 15, sticky = W+E)

#Creating Radio Buttons for Gender
genders = [
            ("Male", "Male"),
            ("Female", "Female")
            ]

sex = StringVar()
sex.set("Male")

for a, b in genders:
    gender_radio = Radiobutton(gender_frame, text = a, variable = sex, value = b )
    gender_radio.pack(anchor = W)

#CREATING QUERY AND SUBMIT BUTTONS

#Create Submit Function
def submit():
    global sex

    #Connecting to/Creating Database
    conn = sqlite3.connect("biodata.db")

    #Defining Cursor Variable
    c = conn.cursor()

    #Submitting fields to data table
    c.execute("INSERT INTO patient_bio VALUES (:first_name, :last_name, :age, :genotype, :gender)",

                #Create Python Dictionary to assign values to fields
                {
                    "first_name": f_name.get(),
                    "last_name": l_name.get(),
                    "age": age.get(),
                    "genotype": genotype.get(),
                    "gender": sex.get(),
                }
                )
    
    #Updating Changes to the Database
    conn.commit()

    #Closing connection
    conn.close()

    #Clear field boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    age.delete(0, END)
    genotype.delete(0, END)
    


#Create Query Function
def query():
    global query_label
    global patient_record

    #Connecting to/Creating Database
    conn = sqlite3.connect("biodata.db")

    #Defining Cursor Variable
    c = conn.cursor()

    #Selecting all records in our patient table
    c.execute("SELECT * FROM patient_bio")
    records = c.fetchall()

    patient_record = ""
    
    for record in records:
        patient_record += "Name: " + str(record[0]) + " " + str(record[1]) + "\n" + "Gender: " + str(record[-1]) + "\n" + "Genotype: " + str(record[-2]) + "\n"

    #Displays records on query label
    query_label = Label(root, text = patient_record, relief = SUNKEN)
    query_label.grid(row = 2, column = 0, columnspan = 2, pady = 15, sticky = W+E)

    #Updating Changes to the Database
    conn.commit()

    #Closing connection
    conn.close()

#Create and place Submit Button
submit = Button(entry_frame, text = "Submit", command = submit, bg = "#00FF00")
submit.grid(row = 4, column = 0, columnspan = 2, sticky = W+E)

#Create and place Query Button
query = Button(root, text = "Query", command = query, bg = "#FF0000")
query.grid(row = 1, column = 0, columnspan = 2, sticky = W+E, padx = 20, pady = 30)




root.mainloop()