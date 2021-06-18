from tkinter import *
#from tkinter import photoImage
#from PIL import ImageTk, Image
import geocoder
import webbrowser
from tkinter import messagebox
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import ibm_db
import random
conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=khn40929;PWD=rlt63tx5m+1v6mts;", "", "")
#stmt = ibm_db.exec_immediate(conn, "CREATE TABLE Persons (PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255));")
#stmt = ibm_db.exec_immediate(conn, "INSERT INTO  userData (FIRSTNAME,LASTNAME,GENDER,DOB,MAIL,USERNAME,PASSWORD) VALUES('Vethanathan','VK','Male','02-12-2001','vethanathanvk@gmail.com','vethanathan','alpha');")
#stmt = ibm_db.exec_immediate(conn, "CREATE TABLE  treecut (treename varchar(255),family varchar(255),reason varchar(255),weight int,height int,location varchar(255),geoloc varchar(255),treecount int);")


g = geocoder.ip('me')
todays_date = date.today()
curr = todays_date.year

#import ibm_db
root=Tk()
root.title("Hackathon")
#bg = PhotoImage(file = "/home/vetha/Downloads/download.jpeg")
#root.geometry("1000x1000")

def plant():
    dashboard.grid_forget()
    plantframe.grid()

def update():
    dashboard.grid_forget()
    mainframe.grid()

def login(username,password):
    sql = "SELECT username,password FROM userData where username='{}' and password ='{}'".format(username,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    print(type(tuple))
    if type(tuple)==type((12,12)):
        loginframe.grid_forget()
        dashboard.grid()
    else:
        messagebox.showwarning("warning","Invalid Credentials")

def submit(firstname,lastname,gender,dob,mailid,username,password):
    stmt = ibm_db.exec_immediate(conn, "INSERT INTO  userData (FIRSTNAME,LASTNAME,GENDER,DOB,MAIL,USERNAME,PASSWORD) VALUES('{}','{}','{}','{}','{}','{}','{}');".format(firstname,lastname,gender,dob,mailid,username,password))
    num = ibm_db.num_rows(stmt)
    if num !=1:
        messagebox.showerror("error","Something went wrong")
    else:
        messagebox.showinfo("info","Account created")
        signupframe.grid_forget()
        loginframe.grid()


def submit_final(name,family,reason,weight,height,location,geoloc,treecount,year):
    stmt = ibm_db.exec_immediate(conn, "insert into treecut (treename,family,reason,weight,height,location,geoloc,treecount,years) values('{}','{}','{}',{},{},'{}','{}',{},'{}');".format(name,family,reason,weight,height,location,geoloc,treecount,year))
    num = ibm_db.num_rows(stmt)
    if num !=1:
        messagebox.showerror("error","Something went wrong")
    else:
        messagebox.showinfo("info","updated to database" + "your reference is is " + str( random.randrange(10000,10156484)))
        mainframe.grid_forget()
        dashboard.grid()

def vetha(year):
    sql = "select sum(treecount) from  treecut where years='{}';".format(year)
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    #print(type(tuple))
    return tuple

def nathan(year):
    sql = "select sum(no) from  treeplant where year='{}';".format(year)
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple = ibm_db.fetch_tuple(stmt)
    #print(type(tuple))
    return tuple



def signup():
    loginframe.grid_forget()
    signupframe.grid()

def getgeolocation1():
    pgeolocation1.insert(0,str(g.latlng)[1:-1])

def getgeolocation():
    geolocation1.insert(0,str(g.latlng)[1:-1])

def back1():
    plantframe.grid_forget()
    dashboard.grid()


def viewgraph():
    t=[];yy=[]
    for i in range(2018,curr+1):
        val =(vetha(i)[0])
        if val==None:
            val=0
        t.append(val)
        yy.append(i)
        

    #print(t,y,sep='\n')
    y = np.array(t)
    year = yy[:]
    plt.title("graph")
    plt.xlabel('Year')
    plt.ylabel('Deforestation % ')

    plt.plot(year,y)
    plt.show() 

def awareness():
    webbrowser.open('https://www.theenvironmentalblog.org/')

def viewstats():
    t=[];yy=[]
    for i in range(2018,curr+1):
        val =(nathan(i)[0])
        if val==None:
            val=0
        t.append(val)
        yy.append(i)
        

    #print(t,y,sep='\n')
    y = np.array(t)
    year = yy[:]
    plt.title("graph")
    plt.xlabel('Year')
    plt.ylabel('Afforestation % ')

    plt.plot(year,y)
    plt.show() 


def contactus():
    webbrowser.open('https://sites.google.com/view/vethanathan')

def back():
    mainframe.grid_forget()
    dashboard.grid()

def psubmiit(name,family,loc,gloc,no,year):
    stmt = ibm_db.exec_immediate(conn, "insert into treeplant (name,family,location,geoloaction,no,year) values('{}','{}','{}','{}',{},'{}');".format(name,family,loc,gloc,no,year))
    num = ibm_db.num_rows(stmt)
    if num !=1:
        messagebox.showerror("error","something went wrong")
    else:
        messagebox.showinfo("info","updated to database" + "your reference is is " + str( random.randrange(10000,10156484)))
        plantframe.grid_forget()
        dashboard.grid()


#bg= ImageTk.photoImage(file='/home/vetha/Downloads/download.jpeg')
#label = Label(root,image=bg).grid(row=0)

loginframe=Frame(root)
loginframe.config(bg='#8705a1')
loginframe.grid()

signupframe=Frame(root)
signupframe.config(bg='#8705a1')

mainframe = Frame(root)
mainframe.config(bg='#8705a1')

dashboard =Frame(root)
dashboard.config(bg='#8705a1')

plantframe=Frame(root)
plantframe.config(bg='#8705a1')


pTreename=Label(plantframe,text="Tree Name",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
pTreefamily=Label(plantframe,text="Tree Family",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
plocation = Label(plantframe,text="Location",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
pgeolocation= Label(plantframe,text="Geolocation",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
ptree_count = Label(plantframe,text="Tree Count",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
py1 = Label(plantframe,text="Year",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')



pTreename1=Entry(plantframe,text="Tree Name",font=("Times", "24", "bold italic"),bg="#cfccc6")
pTreefamily1=Entry(plantframe,text="Tree Family",font=("Times", "24", "bold italic"),bg="#cfccc6")
plocation1 = Entry(plantframe,text="Location",font=("Times", "24", "bold italic"),bg="#cfccc6")
pgeolocation1= Entry(plantframe,text="Geolocation",font=("Times", "24", "bold italic"),bg="#cfccc6")
ptreeno= Entry(plantframe,text="Tree Count",font=("Times", "24", "bold italic"),bg="#cfccc6")
pyear = Entry(plantframe,text="Year",font=("Times", "24", "bold italic"),bg="#cfccc6")

pgeobutton = Button(plantframe,text="Get Coordinates",font=("Times", "24", "bold italic"),command =getgeolocation1,bg="black",foreground = 'white')
pgeobutton.grid(row=3,column=2,padx=10,pady=10)



pTreename.grid(row=0,column=0,padx=10,pady=10)
pTreefamily.grid(row=1,column=0,padx=10,pady=10)
plocation.grid(row=2,column=0,padx=10,pady=10)
pgeolocation.grid(row=3,column=0,padx=10,pady=10)
ptree_count.grid(row=4,column=0,padx=10,pady=10)
py1.grid(row=5,column=0,padx=10,pady=10)

pTreename1.grid(row=0,column=1,padx=10,pady=10)
pTreefamily1.grid(row=1,column=1,padx=10,pady=10)
plocation1.grid(row=2,column=1,padx=10,pady=10)
pgeolocation1.grid(row=3,column=1,padx=10,pady=10)
ptreeno.grid(row=4,column=1,padx=10,pady=10)
pyear.grid(row=5,column=1,padx=10,pady=10)


psubmit = Button(plantframe,text="Submit",font=("Times", "24", "bold italic"),bg="black",foreground = 'white',command =lambda : psubmiit(pTreename1.get(),pTreefamily1.get(),plocation1.get(),pgeolocation1.get(),ptreeno.get(),pyear.get()))
psubmit.grid(row=6,column=1,padx=10,pady=10)
pback = Button(plantframe,text="Back",font=("Times", "24", "bold italic"),bg="black",foreground = 'white',command =back1)
pback.grid(row=6,column=0,padx=10,pady=10)




update_button = Button(dashboard,text="Cut Tree",font=("Times", "24", "bold italic"),command =update,bg="black",foreground = 'white')
plant_button = Button(dashboard,text="Plant Tree",font=("Times", "24", "bold italic"),command=plant,bg="black",foreground = 'white')
update_button.grid(row=0,column=0,padx=10,pady=10)
plant_button.grid(row=0,column=1,padx=10,pady=10)

view_graph = Button(dashboard,text="View  Deforestation Graph",font=("Times", "24", "bold italic"),command =viewgraph,bg="black",foreground = 'white')
view_graph.grid(row=0,column=2,padx=10,pady=10)
awareness = Button(dashboard,text="Awareness",font=("Times", "24", "bold italic"),command =awareness,bg="black",foreground = 'white')
awareness.grid(row=1,column=0,padx=10,pady=10)

view_stats = Button(dashboard,text="View Afforestation graph",font=("Times", "24", "bold italic"),command =viewstats,bg="black",foreground = 'white')
view_stats.grid(row=1,column=1,padx=10,pady=10)

contact = Button(dashboard,text="Contact us",font=("Times", "24", "bold italic"),command =contactus,bg="black",foreground = 'white')
contact.grid(row=1,column=2,padx=10,pady=10)

back = Button(mainframe,text="Back",font=("Times", "24", "bold italic"),command =back,bg="black",foreground = 'white')
back.grid(row=9,column=0,padx=10,pady=10)







Treename=Label(mainframe,text="Tree Name",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
Treefamily=Label(mainframe,text="Tree Family",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
reason=Label(mainframe,text="Reason",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
Weight = Label(mainframe,text="Weight",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
height = Label(mainframe,text="Height",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
location = Label(mainframe,text="Location",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
geolocation= Label(mainframe,text="Geolocation",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
tree_count = Label(mainframe,text="Tree Count",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
y1 = Label(mainframe,text="Year",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')



Treename1=Entry(mainframe,text="Tree Name",font=("Times", "24", "bold italic"),bg="#96ffd5")
Treefamily1=Entry(mainframe,text="Tree Family",font=("Times", "24", "bold italic"),bg="#96ffd5")
reason1=Entry(mainframe,text="Reason",font=("Times", "24", "bold italic"),bg="#96ffd5")
Weight1 = Entry(mainframe,text="Weight",font=("Times", "24", "bold italic"),bg="#96ffd5")
height1 = Entry(mainframe,text="Height",font=("Times", "24", "bold italic"),bg="#96ffd5")
location1 = Entry(mainframe,text="Location",font=("Times", "24", "bold italic"),bg="#96ffd5")
geolocation1= Entry(mainframe,text="Geolocation",font=("Times", "24", "bold italic"),bg="#96ffd5")
treeno= Entry(mainframe,text="Tree Count",font=("Times", "24", "bold italic"),bg="#96ffd5")
year = Entry(mainframe,text="Year",font=("Times", "24", "bold italic"),bg="#96ffd5")



geobutton = Button(mainframe,text="Get coordinates",font=("Times", "24", "bold italic"),command =getgeolocation,bg="black",foreground = 'white')
submit2 = Button(mainframe,text="Submit",font=("Times", "24", "bold italic"),bg="black",foreground = 'white',command =lambda : submit_final(Treename1.get(),Treefamily1.get(),reason1.get(),Weight1.get(),height1.get(),location1.get(),geolocation1.get(),treeno.get(),year.get()))
submit2.grid(row=9,column=1,padx=10,pady=10)
geobutton.grid(row=6,column=2,padx=10,pady=10)

Treename.grid(row=0,column=0,padx=10,pady=10)
Treefamily.grid(row=1,column=0,padx=10,pady=10)
reason.grid(row=2,column=0,padx=10,pady=10)
Weight.grid(row=3,column=0,padx=10,pady=10)
height.grid(row=4,column=0,padx=10,pady=10)
location.grid(row=5,column=0,padx=10,pady=10)
geolocation.grid(row=6,column=0,padx=10,pady=10)
tree_count.grid(row=7,column=0,padx=10,pady=10)
y1.grid(row=8,column=0,padx=10,pady=10)

Treename1.grid(row=0,column=1,padx=10,pady=10)
Treefamily1.grid(row=1,column=1,padx=10,pady=10)
reason1.grid(row=2,column=1,padx=10,pady=10)
Weight1.grid(row=3,column=1,padx=10,pady=10)
height1.grid(row=4,column=1,padx=10,pady=10)
location1.grid(row=5,column=1,padx=10,pady=10)
geolocation1.grid(row=6,column=1,padx=10,pady=10)
treeno.grid(row=7,column=1,padx=10,pady=10)
year.grid(row=8,column=1,padx=10,pady=10)









firstname = Entry(signupframe,text="First name : ",font=("Times", "24", "bold italic"),bg="#cfccc6")
lastname = Entry(signupframe,text="Last name: ",font=("Times", "24", "bold italic"),bg="#cfccc6")
Gender = Entry(signupframe,text="Gender",font=("Times", "24", "bold italic"),bg="#cfccc6")
dateofbirth = Entry(signupframe,text="DOB : ",font=("Times", "24", "bold italic"),bg="#cfccc6")
mailid = Entry(signupframe,text="Mail id: ",font=("Times", "24", "bold italic"),bg="#cfccc6")
username1 = Entry(signupframe,text="Username : ",font=("Times", "24", "bold italic"),bg="#cfccc6")
password1 = Entry(signupframe,text="Password",font=("Times", "24", "bold italic"),show='*',bg="#cfccc6")


name1 = Label(signupframe,text="First name : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
name2 = Label(signupframe,text="Last name: ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
g1= Label(signupframe,text="Gender : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
dob = Label(signupframe,text="DOB : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
m1 = Label(signupframe,text="Mail : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
u1 = Label(signupframe,text="User name : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
u2 = Label(signupframe,text="password",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
b1 = Button(signupframe,text="Submit",font=("Times", "24", "bold italic"),command =lambda : submit(firstname.get(),lastname.get(),Gender.get(),dateofbirth.get(),mailid.get(),username1.get(),password1.get()),bg="black",foreground = 'white')

name1.grid(row=0,column=0,padx=10,pady=10)
name2.grid(row=1,column=0,padx=10,pady=10)
g1.grid(row=2,column=0,padx=10,pady=10)
dob.grid(row=3,column=0,padx=10,pady=10)
m1.grid(row=4,column=0,padx=10,pady=10)
u1.grid(row=5,column=0,padx=10,pady=10)
u2.grid(row=6,column=0,padx=10,pady=10)
b1.grid(row=8,column=1,padx=10,pady=10)

firstname.grid(row=0,column=1,padx=10,pady=10)
lastname.grid(row=1,column=1,padx=10,pady=10)
Gender.grid(row=2,column=1,padx=10,pady=10)
dateofbirth.grid(row=3,column=1,padx=10,pady=10)
mailid.grid(row=4,column=1,padx=10,pady=10)
username1.grid(row=5,column=1,padx=10,pady=10)
password1.grid(row=6,column=1,padx=10,pady=10)






#creating components

username = Entry(loginframe,text="Username : ",font=("Times", "24", "bold italic"),bg="#cfccc6")
password = Entry(loginframe,text="Password : ",font=("Times", "24", "bold italic"),show="*",bg="#cfccc6")
button1= Button(loginframe,text="Login",font=("Times", "24", "bold italic"),command =lambda : login(username.get(),password.get()),bg="black",foreground = 'white')
button2= Button(loginframe,text="Signup",font=("Times", "24", "bold italic"),command =signup,bg="black",foreground = 'white')

textbox1 = Label(loginframe,text="Username : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')
textbox2 = Label(loginframe,text="Password : ",font=("Times", "24", "bold italic"),bg="black",foreground = 'white')


# deploying components
username.grid(row=0,column=1,padx=10,pady=10)
password.grid(row=1,column=1,padx=10,pady=10)
textbox1.grid(row=0,column=0,padx=10,pady=10)
textbox2.grid(row=1,column=0,padx=10,pady=10)
button1.grid(row=2,column=1,padx=10,pady=10)
button2.grid(row=2,column=2,padx=10,pady=10)






mainloop()