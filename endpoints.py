from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
import csv
import re

app = Flask(__name__)

# Hardcoded username and password for JWT authentication
USERNAME = "username"
PASSWORD = "password"
SECRET_KEY = "your-secret-key"  # Change this to a secure secret key

#NON outbound functions:

def get_csv_rows(filepaths):
    rlist = []
    for filepath in filepaths:
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Iterate through each row in the CSV
            for row in reader:
                try:
                    if row and int(row[-1]) >= 10:
                        username_pattern = r'^([\w\.-]+)@'

                        # Search for the username using the pattern
                        match = re.search(username_pattern, filepath)

                        # Check if a match was found
                        if match:
                            username = match.group(1)
                        rlist.append((row, username))
                except:
                    continue
    return rlist
        


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(data, *args, **kwargs)

    return decorated

# JWT Authentication Endpoint
@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if data and 'username' in data and 'password' in data:
        if data['username'] == USERNAME and data['password'] == PASSWORD:
            token = jwt.encode({'user': USERNAME, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=130)}, SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token})
    return jsonify({'message': 'Authentication failed'}), 401


@app.route('/postcron', methods=['POST'])
@jwt_required
def getinfo(data):

    request_data = request.get_json()
    print(request_data)
    # rlist = []
    if(request_data and 'userpass' in request_data):
            with open("cronusers.txt",'w') as f:
                for key in request_data['userpass'].keys():
                    print(key)
                    f.write(key + ",")
            with open("cronpasswords.txt",'w') as f:
                for key in request_data['userpass'].keys():
                    print(request_data['userpass'][key])
                    f.write(request_data['userpass'][key] + ",")
            return jsonify(request_data)

    #     print(request_data['filepaths'])
    #     rlist = get_csv_rows(request_data['filepaths'].split(','))
        
    # #receive data about csv rows here and outbound
    # return jsonify({'row': rlist[0], 'recipient': rlist[1]})

@app.route('/getinfo', methods=['POST'])
@jwt_required
def post(data):
    #admin entry of required employees and passwords
    request_data = request.get_json()
    rlist = []
    if(request_data and 'filepaths' in request_data):
        print(request_data['filepaths'])
        rlist = get_csv_rows(request_data['filepaths'].split(','))
        
    #receive data about csv rows here and outbound
    return jsonify({'row': rlist[0], 'recipient': rlist[1]})



if __name__ == '__main__':
    app.run()
