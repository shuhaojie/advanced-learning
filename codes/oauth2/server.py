import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
client_id = None
client_secret = None

@app.route('/')
def login():
    return render_template('index.html')


@app.route('/authorize', methods=["POST"])
def authorize_to_github():
    global client_id
    global client_secret
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    redirect_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri=http://localhost:8080/oauth/redirect'
    return redirect(redirect_url)


@app.route('/oauth/redirect')
def redirect_to():
    code = request.args.get('code')
    response = requests.post(
        url='https://github.com/login/oauth/access_token',
        json={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code
        },
        headers={"content-type": "application/json"}
    )
    response_content = response.content.decode('utf8')
    access_token = response_content.split('=')[1].split('&')[0]
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {access_token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    response1 = requests.get(
        url='https://api.github.com/user',
        headers=headers
    )
    username = response1.json()['login']
    return render_template('welcome.html', username=username)


if __name__ == '__main__':
    # 启动Flask应用
    app.run(debug=False, host='0.0.0.0', port=8080)
