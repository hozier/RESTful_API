from flask import Flask, jsonify, request, abort
import psqldb 
import requests


app = Flask(__name__)

@app.route('/ios/api/v1/create_db')
def index():
	return psqldb.create_schema('user_db')
	
# curl -i -H "Content-Type: application/json" -X POST -d  '{"uid":"btaylor@wpi.edu", "lname":"taylor", "fname":"bruce", "password":darkknight"}' http://localhost:3001/ios/api/v1/user
# ?uid=<uid_param>&lname=<lname_param>&fname=<fname_param>&password=<password_param>
@app.route('/ios/api/v1/user', methods=['POST'])
def api_user_control():
	
	if len(request.args) == 4:
		print 'we win!!'
		'''
		usage: 
			requests.post("http://localhost:3001/ios/api/v1/user", params=payload)
			payload = {"lname":"thanks", "fname":"cold", "password":"cmit"}
		'''
		return psqldb.insert(request.args.get('uid'), request.args.get('lname'), request.args.get('fname'), request.args.get('password'))
 	 
	return jsonify({'message':'All fields must have values.'}), 404
	
	

@app.route('/ios/api/v1/select/<user_id>', methods=['GET', 'DELETE']) 
def response(user_id):
	if request.method == 'GET':
		api_call = psqldb.select(user_id)
		for users in api_call:
			if not api_call[users]:
				return jsonify({"message":"no user found"}), 404
				
		return jsonify(api_call)
	
	elif request.method == 'DELETE':
		return psqldb.delete(user_id)
		
	
	

@app.route('/ios/api/v1/list_all', methods=['GET']) 
def list():
	return psqldb.list_all()
	
if __name__ == '__main__':
	app.run(port=3001, debug=True)
	
	