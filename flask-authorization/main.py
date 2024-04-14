from flask import (Flask, render_template,
                   request, redirect, url_for, make_response)

app = Flask(__name__)

users = {'u1': 'p1', 'user2': 'password2'}

orders = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username in users and users[username] == password:
                response = make_response(redirect(url_for('order')))
                response.set_cookie('username', username)  # Устанавливаем cookie с именем пользователя
                return response
            else:
                return render_template('index.html', error='Invalid username or password')
    return render_template('index.html', error=None)


@app.route('/order')
def order():
    if 'username' in request.cookies:
        return render_template('order.html', username=request.cookies['username'], orders=orders)
    else:
        return redirect(url_for('index'))  # Если пользователь не авторизован, перенаправляем на страницу входа


if __name__ == '__main__':
    app.run(debug=True)
