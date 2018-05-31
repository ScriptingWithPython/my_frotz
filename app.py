from flask import Flask, request, render_template, jsonify
from read_last_command import send_command, restart_game
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/restart', methods=['PUT'])
def restart():
    return jsonify(restart_game())


@app.route('/send', methods=['POST'])
def send():
    command = request.get_json().get('command')
    return jsonify(send_command(command))


if __name__ == '__main__':
    app.run()
