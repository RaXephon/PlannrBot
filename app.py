from flask import Flask
from flask import request
from flask import send_from_directory
from flask import jsonify

app = Flask(__name__, static_url_path='')

from thought import converse

@app.route("/input")
def recieve_input():
	print('GOT REQUEST! ' + request.args.get('chunk'))
	input_chunk = request.args.get('chunk')
	response, render_this = converse(input_chunk)
	return jsonify(response=response, render_this=render_this)

@app.route('/main.html')
def render_input():
	return send_from_directory('', 'main.html')

@app.route('/artyom.window.min.js')
def send_js(): return send_from_directory('', 'artyom.window.min.js')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)
