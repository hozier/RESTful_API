from flask import Flask, jsonify, request, abort
import psqldb 


app = Flask(__name__)

@app.route('/ios/api/v1/create_db')
def index():
	return psqldb.create_schema('user_db')
	
	
@app.route('/ios/api/v1/user', methods=['POST'])
def api_user_control():
	
	if len(request.args) == 3:
		print 'we win!!'
		'''
		usage: 
			requests.post("http://localhost:3001/ios/api/v1/user", params=payload)
			payload = {"uid":"thanks@me.com", "nickname":"cold", "password":"cmit"}
		'''
		return psqldb.insert(request.args.get('uid'), request.args.get('nickname'), request.args.get('password'))
 	 
	return jsonify({'message':'All fields must have values.'}), 404
	
	

@app.route('/ios/api/v1/select/<user_id>', methods=['GET', 'DELETE']) 
def response(user_id):
	if request.method == 'GET':
		api_call = psqldb.select(user_id)

		if not api_call:
			return jsonify({"message":"no user found"}), 404
		return jsonify(api_call)
	
	elif request.method == 'DELETE':
		return psqldb.delete(user_id)
		
	
	

@app.route('/ios/api/v1/list_all', methods=['GET']) 
def list():
	return psqldb.list_all()
	
@app.route('/ios/api/v1/login', methods=['POST'])
def api_login_control():
	if len(request.args) == 2:
		return psqldb.login(request.args.get('uid'), request.args.get('password'))
		
	return jsonify({'message':'All fields must have values.'}), 404
		
if __name__ == '__main__':
	app.run(port=3001, debug=True)
	
	