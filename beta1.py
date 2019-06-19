import sqlite3

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
	address = input("Enter Visitor address (can leave blank)")

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

	conn.close()

def viewVisitors():
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()

	try:
		cur.execute("SELECT count(*) FROM Visitors")
		list1 = list(cur)
		print(list1[0])
		if list1[0] == (0,): print("Table Empty")
		cur.execute("SELECT * FROM Visitors")
		#if len(list(cur)) == 0: print("Table Empty\n")
	except sqlite3.OperationalError as e:
		print(e)

	print("Vis No:\tName:\tAge\tAddress\n")
	for row in cur:
		print(row)
	conn.close()

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
