import MySQLdb
import random
import re
from soc.config import *


def entry(code, example_id, dependency_exists):
	foo="exec"
	b= 0
	c= 1303985023
	d= example_id
	conn = MySQLdb.connect(host= "127.0.0.1",
		user=DB_USER_DEFAULT,
		passwd=DB_PASS_DEFAULT,
		db=DB_NAME_DEFAULT)
	x = conn.cursor()

	if foo in code:
		if dependency_exists :
			return dependency_exists
		aa = code.find('exec(\'')	
		if aa > 0: 
			bb = code.find('\'',aa+7)	
			value = code[(aa+6):bb]		
		elif (aa == code.find('exec (\"')):
			bb = code.find('\"',aa+7)
			value = code[(aa+7):bb]
		elif(aa == code.find('exec(\"')):
			bb = code.find('\'',aa+7)	
			value = code[(aa+6):bb]
		else:
			print("unknown exec format")
			dependency_exists= False
			return dependency_exists
			
			
		x.execute("""SELECT id FROM textbook_companion_dependency_files WHERE filename = %s""", [value]) #get the dependency id	
		data = x.fetchone()  # extract the id 
		if data is not None:
			role = int(data[0])
			#role1 = int(data[1])
			#print role1
			if not dependency_exists:
				x.execute(""" INSERT into textbook_companion_example_dependency (example_id, dependency_id, approval_status,timestamp) values (%s, %s, %s, %s)""", (d, role, b, c))   #insert new dependency file entry 
				conn.commit()
				conn.close()
				dependency_exists= True
	else:
		dependency_exists= False

	return dependency_exists 
		






