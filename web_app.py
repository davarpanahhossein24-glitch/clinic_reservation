from flask import Flask, redirect, url_for, request


app = Flask(__name__)

@app.route('/')
def home():
    return "home page"

@app.route('/user/<username>')
def say_hello(username):
    if username == "admin":
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('users', username=username))

@app.route('/admin/')
def admin():
    return "hello admin"

@app.route('/users/<username>')
def users(username):
    return "hello %s" % username

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        if username == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('users', username=username))


if __name__ == '__main__':
    app.run(debug=True)


