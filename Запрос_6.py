from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    return


if __name__ == '__main__':
    main()