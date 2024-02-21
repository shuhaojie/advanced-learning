import uuid

from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for
from flaskext.mysql import MySQL
from util import SSOService

app = Flask(__name__)
# 使用session时, 需要设置一个随机值
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '805115148'
app.config['MYSQL_DATABASE_DB'] = 'oauth2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

REGISTER_LIST = ['http://app1.com', 'http://app2.com']


@app.route('/')
def hello_world():
    return render_template('index.html')


# 判断用户是否已登录
@app.get('/is_login')
def user_is_login():
    is_login = False
    callback_url = request.args.get('callback_url')
    session_id = request.cookies.get('sessionId')
    # 如果有session_id, 还需要判断session_id是否有效
    if session_id:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT sso_is_login, username from session where session_id='{session_id}'")
        data = cursor.fetchone()
        if data:
            is_login = data[0]
            username = data[1]
    # 如果用户已经登录, 携带用户名和st跳转
    if is_login:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT code from users where name='{username}'")
        data = cursor.fetchone()
        code = data[0]
        return redirect(f"{callback_url}/confirm?username={username}&service_ticket={code}&session_id={session_id}")
    # 如果用户未登录, 跳转到app的登录页面
    else:
        return redirect(f"{callback_url}/login")


# sso登录前端页面, 由app跳转而来
@app.get('/login')
def login():
    is_login = False
    callback_url = request.args.get('callback_url')
    session_id = request.cookies.get("sessionId")
    # 首先判断用户是否登录, 如果已登录就不用二次登录, 如果没有登录，需要二次登录
    if session_id:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT sso_is_login, username from session where session_id='{session_id}'")
        data = cursor.fetchone()
        if data:
            is_login = data[0]
            username = data[1]
    if is_login:
        sso_service = SSOService()
        service_ticket = sso_service.generate_service_ticket()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from users where name='{username}'")
        data = cursor.fetchone()
        if data:
            cursor.execute(f"UPDATE users SET code='{service_ticket}' where name='{username}'")
            conn.commit()
        else:
            cursor.execute(f"INSERT INTO users(name, code) values ('{username}', '{service_ticket}')")
            conn.commit()
        response = make_response(
            redirect(f'{callback_url}/confirm?service_ticket={service_ticket}&username={username}&session_id={session_id}'))
        return response
    else:
        return render_template('login.html', callback_url=callback_url)


# 用户在没有登录的情况下，填写登录页面，发出post请求
@app.post('/login')
def login_post():
    username = request.form.get('username')
    callback_url = request.form.get('callback_url')
    # 将登录状态写入SSO的session
    # 跳转回去
    sso_service = SSOService()
    service_ticket = sso_service.generate_service_ticket()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from users where name='{username}'")
    data = cursor.fetchone()
    if data:
        cursor.execute(f"UPDATE users SET code='{service_ticket}' where name='{username}'")
        conn.commit()
    else:
        cursor.execute(f"INSERT INTO users(name, code) values ('{username}', '{service_ticket}')")
        conn.commit()
    session_id = str(uuid.uuid4())
    response = make_response(
        redirect(f'{callback_url}/confirm?service_ticket={service_ticket}&username={username}&session_id={session_id}'))
    response.set_cookie("sessionId", session_id)
    return response


@app.post('/confirm')
def confirm():
    data = request.json
    service_ticket = data['service_ticket']
    username = data['username']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from users where name='{username}' and code='{service_ticket}'")
    data = cursor.fetchone()
    if data:
        return jsonify({"verify": True})
    else:
        return jsonify({"verify": False})


@app.get('/logout')
def logout():
    session_id = request.args.get('session_id')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE session SET app1_is_login=FALSE, app2_is_login=FALSE, "
                   f"sso_is_login=FALSE where session_id='{session_id}'")
    conn.commit()
    callback_url = request.args.get('callback_url')
    response = make_response(redirect(callback_url))
    response.delete_cookie('sessionId')
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
