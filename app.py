from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aea9c1ddec6a9e7db162b41afbff9a6d'

posts = [
    {
        'author': 'Sinclair Duan',
        'title': 'Bolg',
        'content': 'Lalala',
        'date_post': 'May 24, 2019'
    },
    {
        'author': 'Sinclair Li',
        'title': 'Blog 2',
        'content': 'What?',
        'date_post': 'May 23, 2019'
    },
    {
        'author': 'Sinclair Li',
        'title': 'Blog 2',
        'content': 'What?',
        'date_post': 'May 23, 2019'
    },
    {
        'author': 'Sinclair Li',
        'title': 'Blog 2',
        'content': 'What?',
        'date_post': 'May 23, 2019'
    }
]


@app.route("/")
@app.route("/home/")
def home():
    return render_template('index.html', posts=posts)


@app.route('/about/')
def about():
    return render_template('about.html', title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = RegistrationForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
