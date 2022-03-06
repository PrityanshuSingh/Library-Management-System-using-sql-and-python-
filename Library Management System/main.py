from termcolor import colored
import mysql.connector,random,time,sys

con=mysql.connector.connect(host="localhost",user="root",passwd="fopnigsql",database="library")
c=con.cursor()
ps_chance=0

def add_b():
    s_no=int(input("Enter Serial no: "))
    bn=input("Enter Book Name: ")
    a=input("Enter Author's Name: ")
    t=input("Enter number of books to be added: ")
    ch=random.randint(100000,999999)
    print("6-digit Code for the \""+bn+"\" : ",ch)

    data=(s_no,bn,a,ch,t)
    sql="insert into books values(%s,%s,%s,%s,%s)"
    c.execute(sql,data)
    update=input("\nPress enter to update data: ")
    con.commit()
    print("\nProcessing",end="")
    for i in range(3) :
        time.sleep(1)
        print(".",end="")
    print("\nData updated successfully.")
    choices()

def del_b():
    print(colored("Available Books: ", 'yellow',  attrs=['bold']))

    sql = "select * from books"
    c.execute(sql)
    list = c.fetchall()
    for i in list:
        print("Book Name: ", i[1])
        print("Book Author: ", i[2])
        print("Book code: ", i[3])

        print("Total number of Books available: ", i[4])
        print()

    co=int(input("Enter 6-digit code of the book to be deleted: "))

    c.execute("select book_name from books where bcode=%s" % co)
    b_delete = c.fetchone()
    print("Book to be deleted: ", b_delete[0])

    confirm = input("\nPress enter to confirm the deletion: ")
    c.execute("delete from books where bcode=%s" % co)
    con.commit()
    print("\nProcessing", end="")
    for i in range(3):
        time.sleep(1)
        print(".", end="")
    print("\nBook deleted successfully.")
    choices()

def issue_b():
    print(colored("Available Books: ", 'yellow',attrs=['bold']))
    sql = "select * from books"
    c.execute(sql)
    list = c.fetchall()
    for i in list:
        print("Book Name: ", i[1])
        print("Book Author: ", i[2])
        print("Book code: ", i[3])
        print("Total number of Books available: ", i[4])
        print()


    n=input("Enter your Name: ")
    r=input("Enter Registration Number: ")
    co=int(input("Enter Book Code: "))
    d=input("Enter Date(yyyy/mm/dd) : ")

    data=(n,r,co,d)
    sql="insert into issue values(%s,%s,%s,%s)"
    c.execute(sql,data)
    c.execute("select book_name from books where bcode=%s"%co)
    b_issued=c.fetchone()

    print("Book to be issued: ",b_issued[0])# here the book is recog. by its 6 digit code
    confirm = input("\nPress enter to confirm: ")
    con.commit()
    print("\nProcessing", end="")

    for i in range(3):
        time.sleep(1)
        print(".", end="")
    print("\nBook successfully issued to "+n+" on "+d+" .")
    bookup(co,-1)

def submit_b():
    n=input("Enter your Name: ")
    r=input("Enter Registration Number: ")
    co=int(input("Enter Book Code: "))
    d=input("Enter Date(yyyy/mm/dd) : ")

    data = (n, r, co, d)
    sql = "insert into submit values(%s,%s,%s,%s)"
    c.execute(sql, data)
    c.execute("select book_name from books where bcode=%s" % co)
    b_sub = c.fetchone()

    print("Book to be submitted: ", b_sub[0])  # here the book is recog. by its 6 digit code
    confirm = input("\nPress enter to confirm: ")
    con.commit()

    print("\nProcessing", end="")
    for i in range(3):
        time.sleep(1)
        print(".", end="")
    print("\nBook successfully submitted by " + n + " on " + d + " .")
    bookup(co, 1)

def bookup(co,u):
    sql="select total from books where bcode=%s"
    data1=(co,)
    c.execute(sql,data1)
    result=c.fetchone()
    t=result[0]+u

    update="update books set total=%s where bcode=%s"
    data2=(t,co)
    c.execute(update,data2)
    con.commit()
    choices()

def display_b():
    print(colored("Available Books: ", 'yellow', attrs=['bold']))
    sql="select * from books"
    c.execute(sql)
    list=c.fetchall()

    for i in list:
        print("Book Name: ",i[1])
        print("Book Author: ",i[2])
        print("Book code: ",i[3])
        print("Total number of Books available: ",i[4])
        print()
    choices()

def choices():
    border = "\n" + "* * * " * 30
    subhead = colored('| PREFERENCES AVAILABLE |', 'blue', attrs=['bold', 'underline'])
    print(colored(border, 'red', attrs=['bold']))

    print("\n" + "\t\t\t" * 6 + "\t"+subhead, end="\n")

    print("\n" + "\t\t" * 10 + " 1. Add Book")
    print("\t\t" * 10 + " 2. Delete Book")
    print("\t\t" * 10 + " 3. Issue Book")
    print("\t\t" * 10 + " 4. Submit Book")
    print("\t\t" * 10 + " 5. Display Books")
    print("\t\t" * 10 + " 6. Exit")

    choice = colored("Enter your choice (1-6): ", 'blue', attrs=['bold'])
    print("\n" + "\t\t\t" * 6 + "\t" + choice, end="")
    ch = int(input(""))
    print()
    if ch == 1:
        add_b()
    elif ch == 2:
        del_b()
    elif ch == 3:
        issue_b()
    elif ch == 4:
        submit_b()
    elif ch == 5:
        display_b()
    elif ch == 6:
        print(colored("CLOSING APPLICATION, HAVE A GREAT DAY!", 'red', attrs=['bold']))
        sys.exit()
    else:
        print(colored("INVALID ENTRY!", 'red', attrs=['bold']))
        sys.exit()

def main():
    sql = "select * from books"
    c.execute(sql)
    list = c.fetchall()

    store=len(list)
    border = "\n" + "* * * " * 30
    heading = colored('| WELCOME TO LIBRARY MANAGEMENT SYSTEM |',

'yellow', attrs=['bold', 'underline'])
    des= colored("| Manage your Library in the most convenient way possible and save your time |", 'yellow', attrs=['bold'])
    des2= colored("| There are %s different books currently available in the library |"%store, 'yellow', attrs=['bold'])
    print(colored(border, 'red', attrs=['bold']))
    print("\n" + "\t\t\t" * 6 + heading, end="\n")
    print("\n" + "\t\t\t" * 4 + "\t"+des, end="\n")
    print("\n" + "\t\t\t" * 4 + "\t\t\t"+des2, end="\n")
    choices()

def pswd(ps_chance):
    if ps_chance < 5:
        ps = input("Enter your Password: ")
        if ps == "openlib789":
            main()
        else:
            ps_chance += 1
            if ps_chance < 5:
                print("Wrong Password, Try again! ")
                print()
            elif ps_chance >= 5:
                print("Wrong Password, Try again in 2 mins: ")
                print()
            pswd(ps_chance)

    elif ps_chance >= 5:
        for i in range(2, 0, -1):
            if i > 1:
                print(str(i) + " mins remaining")
            elif i == 1:
                print(str(i) + " min remaining ")
            for j in range(60, 0, -1):
                time.sleep(1)
        pswd(ps_chance=4)


pswd(ps_chance)
