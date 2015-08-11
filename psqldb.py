import os
import psycopg2
import urlparse
from flask import jsonify
 
def connect():
	os.environ["DATABASE_URL"] = "postgres://ehaxtcxuugahlv:6vv92WKuRCvNV6-1gMHlbbeOMM@ec2-54-83-10-210.compute-1.amazonaws.com:5432/d5cd7ej8t9fbns"
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])
	connect = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)
	
	return connect

def extracted_key(raw):
	import re
	return " ".join(re.findall("[a-zA-Z_]+", str(raw)))
	
def dictionary(values, keys):
	data = []
	if not values:
		data = {}
	elif len(values[0]) == len(keys):
		for row in values:
			a_user_record = {}
			for i in range(len(keys)):
				key = extracted_key(keys[i])
				if key == 'password':
					continue
				a_user_record[key] = row[i]
			data.append(a_user_record)
			
	return {"users":data}
	
	
''' overview: returns cursor object'''
def create_schema(new_table_name):
	conn = connect()
	cursor = conn.cursor() 
	cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'") # lists just the table(s) that the admin creates.
	for table in cursor.fetchall():
		if extracted_key(table) == new_table_name:
			end(conn)
			return jsonify({"message":"table already exists"}), 404
	
	cursor.execute('''
		Create table {0}(
		uid text primary key		not null,
		nickname text 				not null,
		password text			not null
		);
		
	''' . format(new_table_name))
	
	end(conn)
	return jsonify({"message":"new table created."})
	
def insert(uid, nickname, password):
	 
	verify = select(uid)
	if not verify['users']:
		conn = connect()
		cursor = conn.cursor()
		query_string = "INSERT INTO user_db (uid, nickname, password) \
      	VALUES ('{0}', '{1}', '{2}')".format(uid, nickname, password)
		cursor.execute(query_string);
		end(conn)
		return jsonify({"message":"new user created"})
	else:
		return jsonify({"message":"uid already exists"}), 404

def login(uid, password):
	user = select(uid)['users'][0]
	print "within user_db: user: {0}, password: {1}", .format(user["uid"], user['password'])
	print "from client_side: user: {0}, password: {1}", .format(uid, password)
	if uid == user["uid"] and user['password'] == password:
		return jsonify({"message":"user and password verified"})
	return jsonify({"message":"login unsuccessful"}), 404
	
def select(uid):
	conn = connect()
	cursor = conn.cursor()
	query_string = "select * from user_db WHERE uid = '{0}'". format(uid) 
	cursor.execute(query_string)
	values = cursor.fetchall()

	query_string = "SELECT column_name FROM information_schema.columns WHERE table_name ='user_db'"
	cursor.execute(query_string)
	keys = cursor.fetchall()
	end(conn)
			
	return dictionary(values, keys)
	
def list_all():
	conn = connect()
	cursor = conn.cursor()
	query_string = "select * from user_db "
	cursor.execute(query_string)
	values = cursor.fetchall()
	
	query_string = "SELECT column_name FROM information_schema.columns WHERE table_name ='user_db'"
	cursor.execute(query_string)
	keys = cursor.fetchall()
	end(conn)	
		
	return jsonify(dictionary(values, keys))
	
def delete(uid):	
	
	verify = select(uid)
	if not verify['users']: # if no user found.
		return jsonify({"message":"no rows affected -- user not found"}), 404
	else:
		conn = connect()
		cursor = conn.cursor()
		query_string = "DELETE from user_db where uid='{0}'". format(uid)
		cursor.execute(query_string);
		end(conn)
		return jsonify({"message":"user deleted"})

def end(conn):
		conn.commit()
		conn.close()

''' for admin purposes only. this function should never be placed permanently under any route. '''
def _alter_psql_interface():
	'''
	conn = connect()
	cursor = conn.cursor()
	query_string = "ALTER TABLE {0} DROP COLUMN {1}".format('user_db','fname')
	cursor.execute(query_string)
	
	query_string = "ALTER TABLE {0} RENAME COLUMN {1} to {2}".format('user_db','lname', 'nickname')
	cursor.execute(query_string)
	end(conn)
	'''
	return jsonify({"message":"schema altered"})
	