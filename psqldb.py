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
	
	print connect
	return connect


def dictionary(values, keys):
	data = {}
	index = 0
	if not values:
		data = {}
	elif len(values[0]) == len(keys):
		for row in values:
			a_user_record = {}
			for i in range(len(keys)):
				import re
				extracted_key = " ".join(re.findall("[a-zA-Z]+", str(keys[i])))
				a_user_record[extracted_key] = row[i]
			data["ID{0}".format(index)] = (a_user_record)
			index+=1
			
	return data
	
	
''' overview: returns cursor object'''
def create_schema():
	conn = connect()
	cursor = conn.cursor()
	cursor.execute('''
		Create table user_db(
		uid text primary key		not null,
		lname text 				not null,
		fname text 				not null,
		password text			not null
		);
		
	''')
	
	conn.commit()
	conn.close()
	
def insert(uid, lname, fname, password):
	conn = connect()
	cursor = conn.cursor()
	query_string = "INSERT INTO user_db (uid,lname,fname,password) \
      VALUES ('{0}', '{1}', '{2}', '{3}' )".format(uid, lname, fname, password)
	 
	verify = select(uid)
	
	if not verify:
		cursor.execute(query_string);
		conn.commit()
		conn.close()
		return jsonify(verify)
	else:
		conn.commit()
		conn.close()
		return jsonify({"Message":"uid already exists"}) #revisit

def select(uid):
	conn = connect()
	cursor = conn.cursor()
	query_string = "select * from user_db WHERE uid = '{0}'". format(uid) 
	cursor.execute(query_string)
	values = cursor.fetchall()

	query_string = "SELECT column_name FROM information_schema.columns WHERE table_name ='user_db'"
	cursor.execute(query_string)
	keys = cursor.fetchall()
			
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
			
	return jsonify(dictionary(values, keys))