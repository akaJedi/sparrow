#!/usr/bin/python

import sqlite3
import subprocess
import os
import string
import re

username =  os.popen("whoami").read().strip()

skypenames = os.popen("ls /home/bacon/.Skype/ | grep -v 'DbTemp\|shared_\|shared.'").read().strip()
existnames = string.split(skypenames,'\n')
print (25 * '-')
print (" List of Skype accounts:")
print (25 * '-')
for index,name in enumerate(existnames):
	print index+1,'. ',name
max = len(existnames)
smax = str(max)
welcome = 'Enter your name [1-'+smax+'] or type 0 for exit:\n'
is_valid=0
 
while not is_valid :
        try :
                choice = raw_input(welcome)
                is_valid = 1
        except ValueError, e :
                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])

match = re.search(r'[0-9]', choice)
if  match:
	choice = int(choice)

	if choice > max:
        	print ('You can choose only 1-'+smax+' , choose right')
	elif choice < 1:
		print ('You choose only 1-'+smax+' , choose right')
	else:
		choice = choice-1
		conn = sqlite3.connect('/home/'+username+'/.Skype/'+existnames[choice]+'/main.db')
                sql ="CREATE TRIGGER IF NOT EXISTS undo_delete_message BEFORE UPDATE OF body_xml ON Messages FOR EACH ROW WHEN NEW.body_xml = '' BEGIN SELECT CASE WHEN (NEW.body_xml = '' AND NEW.author != '" + existnames[choice] + "') THEN RAISE(ROLLBACK, '42') END; END;"
		cursor = conn.execute(sql)
		if cursor:
			print 'From now you can see all delited messages.'
