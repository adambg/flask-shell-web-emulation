from flask import Flask, render_template, request
import subprocess
from shlex import quote
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourExtraSecretSecureComplexKey'

@app.route('/')
def sessions():
    return render_template('session.html')

@app.route('/send', methods=['GET', 'POST'])
def send():

    try:
        # Set predefined commands here, only commands in this list can be executed
        if (request.form['command'] == "dmesg"):
            stdout, stderr  = subprocess.Popen(["dmesg"], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

        elif (request.form['command'] == "ls"):
            stdout, stderr  = subprocess.Popen(["ls", "-la", quote(request.form['data']) if request.form['data'] else './' ], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
                    
        else:
            stdout, stderr = (b"command not found", b"")

        data = {}
        data['command'] = request.form['command']
        data['data'] = request.form['data']
        data['result'] = stdout.decode('utf-8') + "\n" + stderr.decode('utf-8')
        return (json.dumps(data))

    except Exception as e: print(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0')