from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to ExpensesShare.com api endpoint'


if __name__ == '__main__':
    app.run(host='192.168.1.15')
