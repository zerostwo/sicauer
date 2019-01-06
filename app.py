from flask import Flask, render_template, url_for

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
