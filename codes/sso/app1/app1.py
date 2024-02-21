import requests
from flask import Flask, render_template, redirect, url_for, request, make_response
from flaskext.mysql import MySQL

app1 = Flask(__name__)
app1.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL()
app1.config['MYSQL_DATABASE_USER'] = 'root'
app1.config['MYSQL_DATABASE_PASSWORD'] = '805115148'
app1.config['MYSQL_DATABASE_DB'] = 'oauth2'
app1.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app1)


@app1.get('/')
def index():
    # 首先查看cookie中保存的session_id
    session_id = request.cookies.get("sessionId")
    # 如果有session_id, 还需要判断session_id是否有效
    if session_id:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT app1_is_login, username from session where session_id='{session_id}'")
        data = cursor.fetchone()
        is_login = data[0]
        username = data[1]
        # 如果session_id有效, 读出session中的username
        if is_login:
            return render_template('index.html', logged_in=True, username=username)
        # 如果session_id无效, 是因为其他系统已经退出登录了，而本系统还没有退出登录，此时需要主动退出登录
        else:
            response = make_response(redirect("http://sso.com/is_login?callback_url=http://app2.com"))
            response.delete_cookie("sessionId")
            return response
    # 如果没有session_id, 需要跳转到sso来判断，是否在其他系统上已经登录
    else:
        return redirect("http://sso.com/is_login?callback_url=http://app1.com")


# 登录请求，用于sso来做跳板的
@app1.get('/login')
def login():
    return render_template('index.html', logged_in=False)


# sso登录请求，用于跳转到sso做登录的
@app1.get('/sso_login')
def sso_login():
    return redirect('http://sso.com/login?callback_url=http://app1.com')


# 验证service_ticket是否有效
@app1.get('/confirm')
def confirm():
    service_ticket = request.args.get('service_ticket')
    username = request.args.get('username')
    session_id = request.args.get('session_id')
    response = requests.post(
        url='http://sso.com/confirm',
        json={
            "service_ticket": service_ticket,
            "username": username,
            "url": "http://app1.com"
        },
        headers={"content-type": "application/json"}
    )
    data = response.json()
    verify = data['verify']
    # 如果验证通过
    if verify:
        response = make_response(redirect(f"http://app1.com"))
        # session_id = str(uuid.uuid4())
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from session where username='{username}'")
        data = cursor.fetchone()
        if data:
            cursor.execute(f"UPDATE session SET session_id='{session_id}', app1_is_login=TRUE, app2_is_login=TRUE, "
                           f"sso_is_login=TRUE where username='{username}'")
            conn.commit()
        else:
            cursor.execute(
                f"INSERT INTO session(username, session_id, app1_is_login, app2_is_login, sso_is_login) "
                f"values ('{username}', '{session_id}', TRUE, TRUE, TRUE)")
            conn.commit()
        response.set_cookie('sessionId', session_id)
        return response
    else:
        return redirect(url_for('index', logged_in=False))


@app1.get('/logout')
def logout():
    session_id = request.cookies.get("sessionId")
    response = make_response(redirect(f'http://sso.com/logout?callback_url=http://app1.com&session_id={session_id}'))
    response.delete_cookie("sessionId")
    return response


if __name__ == '__main__':
    app1.run(debug=True, port=5001)
