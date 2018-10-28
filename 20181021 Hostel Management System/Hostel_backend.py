import sqlite3

def connect():
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS student (  regno text NOT NULL PRIMARY KEY, \
                                                        name text, \
                                                        father_name text, \
                                                        room_no INTEGER, \
                                                        contact_no INTEGER, \
                                                        dob text, \
                                                        hostel_building text, \
                                                        FOREIGN KEY(hostel_building) REFERENCES Hostel(hostel_building), \
                                                        FOREIGN KEY(room_no) REFERENCES Room(room_no))")

    cur.execute("CREATE TABLE IF NOT EXISTS hostel (hostel_building text NOT NULL PRIMARY KEY, \
                                                    no_of_rooms INTEGER, \
                                                    no_of_students INTEGER, \
                                                    expenses INTEGER, \
                                                    location text)")

    cur.execute("CREATE TABLE IF NOT EXISTS room (  room_no INTEGER NOT NULL PRIMARY KEY, \
                                                    capicity INTEGER, \
                                                    hostel_building text, \
                                                    room_type text, \
                                                    FOREIGN KEY(hostel_building) REFERENCES Hostel(hostel_building))")

    cur.execute("CREATE TABLE IF NOT EXISTS staff ( emp_ID text NOT NULL PRIMARY KEY, \
                                                    name text, \
                                                    hostel_building text, \
                                                    salary INTEGER, \
                                                    contact_no INTEGER, \
                                                    street text, \
                                                    state text, \
                                                    pincode INTEGER, \
                                                    works_mess_type text, \
                                                    FOREIGN KEY(hostel_building) REFERENCES Hostel(hostel_building), \
                                                    FOREIGN KEY(works_mess_type) REFERENCES Mess(mess_type))")

    cur.execute("CREATE TABLE IF NOT EXISTS mess (  mess_type text NOT NULL PRIMARY KEY, \
                                                    expenses INTEGER, \
                                                    incharge text, \
                                                    bf_timings text, \
                                                    ln_timings text, \
                                                    dn_timings text, \
                                                    FOREIGN KEY(incharge) REFERENCES Staff(emp_ID))")

    cur.execute("CREATE TABLE IF NOT EXISTS fee (   student_ID text NOT NULL, \
                                                    fee_amount INTEGER, \
                                                    fee_status text, \
                                                    FOREIGN KEY(student_ID) REFERENCES Student(regno))")

    cur.execute("CREATE TABLE IF NOT EXISTS furniture ( furniture_ID Integer NOT NULL PRIMARY KEY, \
                                                        furniture_type text, \
                                                        room_no Integer, \
                                                        FOREIGN KEY(room_no) REFERENCES Room(room_no))")

    conn.commit()
    conn.close()

'''
def insert(title,author,year,isbn):
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)",(title,author,year,isbn))
    conn.commit()
    conn.close()
    view()
'''

'''
The tab name becomes the object-name of the widget set as the tab's page. 
When the tab is added, the page will be automatically re-parented to the internal 
stack-widget of the tab-widget. This means you can get a reference to the page like this:

### self.Management_TabWidget = QtWidgets.QTabWidget(Form)
### self.student_tab = QtWidgets.QWidget()

# page = tabwidget.findChild(QWidget, tabname)

and get its index like this:

# index = tabwidget.indexOf(page)

or set the current tab directly by name like this:

# tabwidget.setCurrentWidget(tabwidget.findChild(QWidget, tabname))



'''


# insert("hostel_tab", "Bblock",256,1024,468456,"chennai") working!!!!!!!



# backup
def insert(table, *args):
    # here table takes the tab name (student_tab) "as a string"
    # remove the _tab part to get the table name
    # args will be taken from lineEdit
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    
    command = "INSERT INTO "+ str(table)[:-4] +" VALUES ("

    # the text should be in ' ' but the integer should not
    ##for a in args:
        ##command = command + "'" + str(a) + "'" +" ,"
    
    command = command + "?, "*len(args)
    command = command[:-2]
    command = command + ")"

    cur.execute(command, args)
    #cur.execute("INSERT INTO ? VALUES (?"+",?"*(len(args)-1)+")", (str(table)[:-4],*args))
    conn.commit()
    conn.close()
    # view() remove if any display issues    


def view(table):
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    command = "SELECT * FROM "+str(table)[:-4]
    cur.execute(command)
    #cur.execute("SELECT * FROM ?",(str(table)[:-4]))
    rows=cur.fetchall()
    conn.close()
    return rows

'''
def search(table, **kwargs):
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    command = "SELECT * FROM {} WHERE ".format(str(table)[:-4])
    for k,v in kwargs.items():
        command = command +str(k) + "="+ str(v)+" AND "
    command = command[:-5]
    cur.execute(command)
    rows=cur.fetchall()
    conn.close()
    return rows
'''

def search(table, **kwargs):
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    command = "SELECT * FROM {} WHERE ".format(str(table)[:-4])
    for k,v in kwargs.items():
        command = command +str(k) + "= ?" +" AND "
    command = command[:-5]
    cur.execute(command, list(kwargs.values()))
    rows=cur.fetchall()
    conn.close()
    return rows


def delete(table, **kwargs):
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    command = "DELETE FROM {} WHERE ".format(str(table)[:-4])
    for k,v in kwargs.items():
        command = command +str(k) + "= ?"+" AND "
    command = command[:-5]
    cur.execute(command, list(kwargs.values()))
    conn.commit()
    conn.close()
    # view() # remove if any display issues occur


# update is a bit complicated
# how to get the pimary key for each table ?
'''
def update(id,title,author,year,isbn):
    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title,author,year,isbn,id))
    conn.commit()
    conn.close()
    view() # remove if any display bugs
'''


def update(table, *args, **kwargs):
    ''' updates the selected row with the text in the lineEdit 
        if any lineEdit is empty then the original value of that column is kept
        else, it is replaced by the lineEdit value
    '''
    # args will give the table values
    # kwargs will give the lineEdit values (which will replace the table values)

    conn=sqlite3.connect("management.db")
    cur=conn.cursor()
    command = "UPDATE {} SET ".format(str(table)[:-4])
    for k,v in kwargs.items():
        command = command + str(k) +"=?, "
    command = command[:-2]
    command = command + " WHERE "
    
    for k,v in kwargs.items():
        command = command + str(k) +"=? AND "
    command = command[:-5]

    kw_vals = list(kwargs.values())

    replacement_values = []
    for i in range(len(kw_vals)):
        if kw_vals[i] == '':
            replacement_values.append(args[i])
        elif kw_vals[i] != '':
            replacement_values.append(kw_vals[i])
        else:
            pass
    final_parameters = replacement_values + list(args)

    cur.execute(command, final_parameters)


    conn.commit()
    conn.close()
    #view() # remove if any display bugs


connect()

#insert("The Sun","John Smith",1918,913123132)
#delete(3)
#update(4,"The moon","John Smooth",1917,99999)
#print(view())
#print(search(author="John Smooth"))



# to add functionality to a button
# self.view_btn.clicked.connect(backend_fucntion)
