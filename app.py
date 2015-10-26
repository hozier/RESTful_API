from flask import Flask, jsonify, request, abort
import psqldb


app = Flask(__name__)

@app.route('/ios/api/v1/create_db')
def index():
	# return psqldb.create_schema('user_db')
	return psqldb.create_schema('note_metrics')

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


@app.route('/ios/api/v1/note', methods=['POST'])
def new_note():
	if len(request.args) == 2:
		print 'we win!!'
		'''
		usage:
			requests.post("http://localhost:3001/ios/api/v1/note", params=payload)
			payload = {"uid":"thanks@me.com", "note":"no class today!!"}
		'''
		return psqldb.make_note(request.args.get('uid'), request.args.get('note'))
	return jsonify({'message':'All fields must have values.'}), 404


@app.route('/ios/api/v1/note_metric', methods=['POST'])
def modify_note_metric():
	if len(request.args) == 2:
		print 'we win!!'
		'''
		usage:
			requests.post("http://localhost:3001/ios/api/v1/note_metric", params=payload)
			payload = {"note_id":"3", "tag":"down_btn_tag"}
		'''
		return psqldb.update_note_metric(request.args.get('note_id'), request.args.get('tag'))
	return jsonify({'message':'All fields must have values.'}), 404


@app.route('/ios/api/v1/select/<user_id>', methods=['GET', 'DELETE'])
def response(user_id):
	if request.method == 'GET':
		json = psqldb.select(user_id)
		if not json:
			return jsonify({"message":"no user found"}), 404
		return jsonify({"user":json})

	elif request.method == 'DELETE':
		return psqldb.delete(user_id)




@app.route('/ios/api/v1/list_all', methods=['GET'])
def list():
	return psqldb.list_all()

@app.route('/ios/api/v1/list_all_notes', methods=['GET'])
def listn():
	return psqldb.list_all_notes()

@app.route('/ios/api/v1/login', methods=['POST'])
def api_login_control():
	if len(request.args) == 2:
		return psqldb.login(request.args.get('uid'), request.args.get('password'))

	return jsonify({'message':'All fields must have values.'}), 404

if __name__ == '__main__':
	app.run(port=3001, debug=True)
