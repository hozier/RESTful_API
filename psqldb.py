import os
import psycopg2
import psycopg2.extras
import urlparse
from flask import jsonify
from psycopg2.extensions import adapt
 
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
		
''' overview: returns cursor object'''
def create_schema(new_table_name):
	conn = connect()
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'") # lists just the table(s) that the admin creates.
	
	if new_table_name == cursor.fetchone()['table_name']:
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

def is_present(uid):
	conn = connect()
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	collection = {"conn":conn, "boolean":True, "cursor":cursor}
	query_string = "select uid from user_db WHERE uid = '{0}'". format(uid) 
	cursor.execute(query_string)
	json = cursor.fetchall()
		
	if not json: # if response from query is '[]' -- the empty array, then
		collection["boolean"] = False
	return collection


def insert(uid, nickname, password):
	print "this is user input: ", password
	verify = is_present(uid)
	if verify['boolean'] == False:
		query_string = """INSERT INTO user_db (uid, nickname, password) \
      	VALUES ({0}, {1}, {2})""".format(adapt(uid), adapt(nickname), adapt(password))
		verify["cursor"].execute(query_string);
		end(verify["conn"])
		return jsonify({"message":"new user created"})
		
	else:
		end(verify["conn"])
		return jsonify({"message":"uid already exists"}), 404

def login(uid, password):
	conn = connect()
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	query_string = "select password from user_db WHERE uid = '{0}'". format(uid) 
	
	cursor.execute(query_string)
	password_db = cursor.fetchall().pop()["password"]
	
	if password_db and password_db == password:
		return jsonify({"message":"user and password verified"})
	return jsonify({"message":"login unsuccessful"}), 404
	
def select(uid):
	conn = connect()
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	query_string = "select uid, nickname from user_db WHERE uid = '{0}'". format(uid) 
	cursor.execute(query_string)
	json = cursor.fetchall()
	end(conn)

	if not json:
		return jsonify({"message":"no user found"}), 404
	return jsonify({"user":json})
	
	
def list_all():
	conn = connect()
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	query_string = "select uid, nickname from user_db "
	cursor.execute(query_string)
	json = cursor.fetchall()
	end(conn)	
		
	if not json:
		return jsonify({"message":"user_db is empty"}), 404
	return jsonify({"users":json})
	
	
def delete(uid):	
	
	verify = is_present(uid) 
	if verify['boolean'] == False: # if user is not present
		return jsonify({"message":"no rows affected -- user not found"}), 404
	else:
		query_string = "DELETE from user_db where uid='{0}'". format(uid)
		verify["cursor"].execute(query_string);
		end(verify["conn"])
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
	# query_string = "SELECT column_name FROM information_schema.columns WHERE table_name ='user_db'"
	query_string = "ALTER TABLE {0} RENAME COLUMN {1} to {2}".format('user_db','lname', 'nickname')
	cursor.execute(query_string)
	end(conn)
	'''
	return jsonify({"message":"schema altered"})
	