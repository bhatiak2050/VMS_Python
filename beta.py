import sqlite3
import os
import platform

dbname='visitors.sqlite'

def addVisitor():
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()

	cur.execute('''CREATE TABLE IF NOT EXISTS Visitors (
		vno INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		age INTEGER NOT NULL,
		address TEXT)''')

	name = input("Enter visitor name: ")
	age = int(input("Enter visitor age: "))
	address = input("Enter Visitor address (can leave blank)\n")

	cur.execute("INSERT INTO Visitors (name, age, address) VALUES (? ,?, ?)", (name, age, address))
	conn.commit()
	conn.close()

def rmVisitor():
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()

	#id = int(input("Enter vno of visitor to be deleted: "))
	id = input("Enter vno of visitor to be deleted: ")

	cur.execute("DELETE FROM Visitors WHERE vno = (?)" ,(id))
	conn.commit()

	cur.execute("SELECT count(*) FROM Visitors")
	list1 = list(cur)
	if list1[0] == (0,): cur.execute("DROP TABLE IF EXISTS Visitors")

	conn.close()
	updateTable()

def updateTable():
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()

	try:
		cur.execute("SELECT * FROM Visitors")
	except sqlite3.OperationalError as e:
		if e.find('no such table') != -1: print("Table Does Not Exist")
		conn.close()
		return

	temp_dbname = 'temp.sqlite'
	conn_temp = sqlite3.connect(temp_dbname)
	cur_temp = conn_temp.cursor()

	cur_temp.execute("DROP TABLE IF EXISTS Visitors")
	cur_temp.execute('''CREATE TABLE Visitors (
                vno INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                address TEXT)''')

	i=1
	for row in cur:
		cur_temp.execute("INSERT INTO Visitors (vno, name, age, address) VALUES (?, ?, ?, ?)",(i, row[1], row[2], row[3]))
		conn_temp.commit()
		i+=1

	conn_temp.close()
	conn.close()

	if platform.system() == 'Linux':
		os.system('rm %s && mv %s %s' % (dbname, temp_dbname, dbname))
	elif platform.system() == 'Windows':
		os.system('del %s && rename %s %s' % (dbname, temp_dbname, dbname))

def viewVisitors():
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()

	try:
		cur.execute("SELECT * FROM Visitors")
	except sqlite3.OperationalError as e:
		e = str(e)
		if e.find('no such table') != -1: print("Table Does Not Exist")
		conn.close()
		return

	print("Visitor No:\tName:\t\tAge\t\tAddress")
	for row in cur:
		print("%d\t\t%s\t\t%d\t\t%s" % (row[0], row[1], row[2], row[3]))
	conn.close()

#Main Block
choice=0
while choice !=4:
	print("\nMenu:\n1)Add visitor\n2)Remove visitor\n3)View all visitors\n4)Exit\nEnter your choice: ")
	try: choice = int(input())
	except:
		print("Please enter a number between 1-4");
		continue

	if choice == 1: addVisitor()
	elif choice == 2: rmVisitor()
	elif choice == 3: viewVisitors()
	elif choice == 4:
		print("Goodbye")
		exit()
	else:
		print("Please enter a number between 1-4")
		continue
