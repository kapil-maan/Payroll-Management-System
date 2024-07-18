import mysql.connector

import datetime
from tabulate import tabulate

db=input('enter name of your database :- ')

mydb =mysql.connector.connect(host='localhost', user='root',passwd='ravinder')
mycursor = mydb.cursor()


sql="create database if not exists %s" % (db,)
mycursor.execute(sql)
print("Database created sucessfully ....")
mycursor=mydb.cursor()
mycursor.execute("use "+db)

tablename=input("Name of the table to be created :-")
query="create table if not exists "+tablename+" \
(empno int primary key,\
name varchar(15) not null ,\
job varchar(15),\
basic_salary int,\
DA float,\
HRA float,\
Gross_salary float,\
tax float,\
Net_salry float)"

print("table "+tablename+" created sucessfully ")
mycursor.execute(query)


while True:
	print("\n\n\n")
	print("*"*95)
	print("\t\t\t\tMAIN MENU")
	print("*"*95)
	print("\t\t\t\t 1:-Adding Employee records")
	print("\t\t\t\t 2:-For Displaying Record Of all the Employee ")

	print("\t\t\t\t 3:-For Displaying Record Of a particular Employee ")
	print("\t\t\t\t 4:-For Deleting Record Of all the Employee ")
	print("\t\t\t\t 5:-For Deleting a Record Of a particular Employee ")
	print("\t\t\t\t 6:-For Modification in a record")
	print("\t\t\t\t 7:-For Displaying Payroll ")
	print("\t\t\t\t 8:-For Displaying Salary Slip for all the Employee ")
	print("\t\t\t\t 9:-For Displaying Salary Slip for a particular Employee ")
	print("\t\t\t\t 10:-For Exit ")

	print("enter choice....",end="")
	choice=int(input())
	if choice==1:
		try:
			print("enter employee information .....")
			mempno=int(input("enter employee no :-"))
			mname=input("enter employee name:-")
			mjob=input("enter employee job:-")
			mbasic=float(input("enter basic salary"))

			if mjob.upper()=="OFFICER":
				mda=mbasic*0.5
				mhra=mbasic*0.35
				mtax=mbasic*0.2
			elif mjob.upper()=="MANAGER":
				mda=mbasic*0.45
				mhra=mbasic*0.30
				mtax=mbasic*0.15
			else:
				mda=mbasic*0.40
				mhra=mbasic*0.25
				mtax=mbasic*0.1

			mgross=mbasic+mda+mhra
			mnet=mgross-mtax
			rec = (mempno,mname,mjob,mbasic,mda,mhra,mgross,mtax,mnet)
			query="insert into "+tablename+" values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			mycursor.execute(query,rec)

			mydb.commit()
			print("Record added sucessfully.....")
		except Exception as e:
			print("something went wrong",e)

	elif choice==2:
		try:
			query="select * from "+tablename
			mycursor.execute(query)

			print(tabulate(mycursor,headers=["empno","name","job","basic","Salary","DA","HRA","Gross salary","Tax","Net Salary"], tablefmt='psql'))


		except Exception as e:
			print("something went wrong",e)



	elif choice==3:
		try:
			en=input("enter employee no. of the record to be displayed :-")
			query="select * from "+tablename+" where empno="+en
			mycursor.execute(query)
			myrecord=mycursor.fetchone()
			print("\n\n Record of Employee No:-"+en)
			print(myrecord)
			c=mycursor.rowcount

			if c==-1:
				print("Nothing to display ")

		except Exception as e:
			print("something went wrong",e)



	elif choice==4:
		try:
			ch= input("Do you want to delete all the records (y/n)")
			if ch.upper()=="Y":
				mycursor.execute("delete from "+tablename)
				mydb.commit()
				print("All the records are deleted....")
		except Exception as e:
			print("something went wrong",e)



	elif choice==5:
		try:
			en=input("Enter employee no. of the record to be deleted:- ")
			query="delete from "+tablename+" where empno="+en
			mycursor.execute(query)
			mydb.commit()
			c=mycursor.rowcount
			if c>0:
				print("Deletion done")
			else:
				print("Employee no ",en," not found")
				
		except Exception as e:
			print("something went wrong",e)


	elif choice==6:
		try:
			en=input("Enter employee no. of the record to be modified:- ")
			query="select * from "+tablename+" where empno="+en
			mycursor.execute(query)
			myrecord=mycursor.fetchone()
			c=mycursor.rowcount
			if c==-1:
				print("Empno "+en+" does not exist")
			else:
				mname=myrecord[1]
				mjob=myrecord[2]
				mbasic=myrecord[3]
				print("Empno  :",myrecord[0])
				print("name   :",myrecord[1])
				print("job    :",myrecord[2])
				print("basic  :",myrecord[3])
				print("da     :",myrecord[4])
				print("hra    :",myrecord[5])
				print("gross  :",myrecord[6])
				print("tax    :",myrecord[7])
				print("net    :",myrecord[8])
				print("------------------------")
				print("Type Value to modify below or just press Enter for no change")
				x=input("Enter name ")
				if len(x)>0:
					mname=x
				x=input("Enter job ")
				if len(x)>0:
					mjob = x
				x=input("Enter basic salary ")
				if len(x)>0:
					mbasic=float(x)
				query="update "+tablename+" set name= "+"'"+mname+"'"+','+'job='+"'"+mjob+"'"+','+"basic_salary="+str(mbasic)+" where empno="+en      #+mbasic+"'"

				print(query)
				mycursor.execute(query)
				mydb.commit()
				print("Record modified")


		except Exception as e :
			print("something went wrong",e)
	elif choice==7:
		try:
			query="select * from "+tablename
			mycursor.execute(query)
			myrecords=mycursor.fetchall()
			print("\n\n\n")
			print("*"*95)
			print("Employee Payroll".center(90))
			print("*"*95)
			now = datetime.datetime.now()
			print("Current Date and Time:",end=' ')
			print(now.strftime("%Y-%m-%d %H:%M:%S"))
			print()
			print("-"*95)
			print("%-5s %-15s %-10s %-8s %-8s %-8s %-9s %-8s %-9s" % ('Empno','Name','Job','Basic','DA','HRA','Gross','Tax','Net'))
			
			print("-"*95)
			for rec in myrecords:
				print('%4d %-15s %-10s %8.2f %8.2f %8.2f %9.2f %8.2f %9.2f'%rec)
			print("-"*95)
			
		except Exception as e:
			print("something went wrong",e) 




	elif choice==8:
		try:
			query="select * from "+tablename
			mycursor.execute(query)
			now = datetime.datetime.now()
			print("\n\n\n")
			print("-"*95)
			print("\n\n\n\t\t\t\tSALARY SLIP ")
			print("-"*95)
			print("Current Date and Time:", end=' ')
			print(now.strftime("%Y-%m-%d %H:%M:%S"))
			myrecords=mycursor.fetchall()
			for rec in myrecords:
				print('%4d %-15s %-10s %8.2f %8.2f %8.2f %9.2f %8.2f %9.2f'%rec)
		except Exception as e:
			print("something went wrong",e)

			

	elif choice==9:
		try:
			en=input("Enter employee number whose pay slip you want to retreive:")
			query="select * from "+tablename+" where empno="+en
			mycursor.execute(query)
			now = datetime.datetime.now()
			print("\n\n\n\t\t\t\tSALARY SLIP ")
			print("Current Date and Time:", end=' ')
			print(now.strftime("%Y-%m-%d %H:%M:%S"))

			print(tabulate(mycursor,headers=['Empno','Name','Job','Basic Salary','DA','HRA','Gross salary','Tax','Net Salary'],tablefmt='psql'))			


		except Exception as e:
			print("something went wrong",e)


	elif choice==10:

		break

	else:
		print("wrong choice !!!!! ") 


