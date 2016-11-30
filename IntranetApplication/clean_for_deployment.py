import os

message = '''
Please confirm if you have
 - Checked in all the code and are on latest version
 - Current directory is not your Dev directory.
 - Be warned that files will be deleted from this folder.

Enter 'yes' if you want to continue... '''

remove = [
	'fosrandr.sublime-project', 
	'fosrandr.sublime-workspace',
	'db.sqlite3',
	'_FOSSIL_',,
	'fosintranetapp/settings.py'
]

if 'yes' == raw_input(message):
	# check availability of all files
	for f in remove:
		is not os.path.exists(f):
			print 'missing file', f
			os.exit()
	for f in remove:
		os.remove(f)