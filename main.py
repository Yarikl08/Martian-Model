import datetime
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login_email.data).first():
            return render_template('register.html', form=form, message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login_email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# Добавляем капитана, Первая работа
def main():
    db_session.global_init("db/mars_explorer.db")

    session = db_session.create_session()

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    session.add(user)

    user = User()
    user.surname = "Weir"
    user.name = "Andy"
    user.age = 40
    user.position = "colonist"
    user.speciality = "cook"
    user.address = "module_2"
    user.email = "weir_chief@mars.org"
    session.add(user)

    user = User()
    user.surname = "Watney"
    user.name = "Mark"
    user.age = 23
    user.position = "colonist"
    user.speciality = "pilot"
    user.address = "module_1"
    user.email = "watney_chief@mars.org"
    session.add(user)

    user = User()
    user.surname = "Sanders"
    user.name = "Teddy"
    user.age = 29
    user.position = "colonist"
    user.speciality = "programmer"
    user.address = "module_3"
    user.email = "sanders_chief@mars.org"
    session.add(user)

    job = Jobs()
    job.team_leader = 1
    job.job = 'Deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)

    job = Jobs()
    job.team_leader = 2
    job.job = 'Exploration of mineral resources'
    job.work_size = 15
    job.collaborators = '4, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)

    job = Jobs()
    job.team_leader = 3
    job.job = 'Development of a management system'
    job.work_size = 25
    job.collaborators = '5'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)

    session.commit()

    for job in session.query(Jobs).all():
        print(job)

    app.run()


if __name__ == '__main__':
    main()