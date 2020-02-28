<p align="center">
  <a href="https://github.com/zerostwo/sicauer" rel="nofollow">
    <img src="https://zzmath.top/static/favicon.ico" alt="CodyHouse logo" width="80" height="80" data-canonical-src="https://zerostwo.github.io/favicon.png" style="max-width:100%;">
  </a>
</p>

基于Python的Web应用开发，冲鸭:grin:！
---
[![](https://img.shields.io/badge/Ubuntu-18.04.4%20LTS-orange.svg)](https://www.ubuntu.com/download/desktop)
[![](https://img.shields.io/badge/Python-3.7.4-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![](https://img.shields.io/badge/Flask-1.1.1-red.svg)](http://flask.pocoo.org/)
[![](https://img.shields.io/badge/IDE-Vim-green.svg)](https://www.jetbrains.com/pycharm/)
[![](https://img.shields.io/github/license/zerostwo/sicauer.svg)](https://github.com/zerostwo/sicauer/blob/master/LICENSE)
![](http://progressed.io/bar/19?title=Done)

我的开发环境是基于`Ubuntu 18.04.4 LST`系统环境下的`Python 3.7.4`，IDE使用的`Vim`，在这个项目中我所使用的所有Python包及其版本号我都会记录在[`requirements.txt`](https://github.com/zerostwo/zzmath/blob/master/requirements.txt)文件中。可以使用以下命令批量安装我所使用的包：
```bash
$ wget https://github.com/zerostwo/zzmath/blob/master/requirements.txt      
$ pip install -r requirement.txt
```
### 使用虚拟环境中的pip安装flask框架
使用第三方工具`virtualenve`创建，若未安装，在`bash`下输入以下代码来安装：
```bash
$ sudo apt-get install python-virtualenv
```
工具安装好以后，任意新建一个文件夹存放之后的所有文件。这里我新建一个名为`sicauer`的文件夹：
```bash
$ mkdir zzmath
$ cd zzmath
```
进入新建文件夹后，使用`virtualenv`创建一个虚拟环境`venv`（通常虚拟环境都被命名为这个）：
```bash
$ virtualenv venv
```
在使用这个虚拟环境之前需要激活：
```bash
$ source venv/bin/activate
```
退出虚拟环境使用以下命令：
```bash
$ deactivate
```

当我们进入虚拟环境后，使用虚拟环境自带的`pip`安装`flask`框架：

```bash
(venv) $ pip install flask
```

### 三步搭建flask程序

#### 第一步：初始化
所有Flask程序都必须创建一个程序实例。程序实例是Flask类的对象，使用以下代码创建：
```python
from flask import Flask
app = Flask(__name__)
```
Flask类的构造函数必须有`__name__`这个指定参数，即程序主模板或包的名字。

##### 第二步：定义路由和视图函数
处理URL与函数之间关系的程序称为**路由**，使用`app.route`这个修饰器来声明路由：
```python
@app.route('/')
def index():
    return 'Index page'
```

<div align=center>

![](https://img.cdn.zzmath.top/static/images/Flask-web/1.png)

</div>

上面的`index()`即为**视图函数**。在route修饰器中使用尖括号`<...>`，即可定义动态路由：
```python
@app.route('/user/<name>')
def user(name):
    return 'Hello, %s' % name
```

<div align=center>

![](https://img.cdn.zzmath.top/static/images/Flask-web/2.png)

</div>

#### 第三步：启动服务器
程序实例用`run`方法启动Flask集成的开发Web服务器：
```python
if __name__ == '__main__':
    app.run(debug=True)
```
其中`debug=True`是启用调试模式，启用该模式后，你可以的在网页中直接调试你的程序。

### Jinjia2 模板引擎
[Jinjia2](http://docs.jinkan.org/docs/jinja2/) 是一个模板引擎。使用以下代码导入渲染模板引擎：
```python
from flask import render_template
```
#### 渲染模板
默认情况下，Flask在程序文件夹中的`templates`子文件夹中寻找模板。现在我们在`templates`子文件夹中新建一个模板`user.html`。
```html
<h1>Hello, {{ name }}</h1>
```
然后修改程序中的视图函数：
```python
@app.route('/user/<name>')
def user(name):
    return render_template(login.html, name=name)
```
Flask提供的`render_template`函数第一个参数是模板文件名，随后跟的是键值对。上面中的键值对的含义是：左边表示参数名，也就是模板中使用的占位符，右边的是当做一个变量。

#### 变量

在上面模板中使用的`{{ name }}`结构表示一个变量。Jinja2能识别Python中所有类型的变量。例如：
```html
<p>字典: {{ mydic['key'] }}</p>
<p>列表: {{ mylist[2] }}</p>
```
#### 控制结构
Jinja2提供了多种控制结构，可用来改变模板的渲染流程。

1. 条件控制语句：
    ```html
    {% if user %}
        Hello, {{ user }}
    {% else %}
        Hello, Stranger
    {% endif %}
    ```
2. 循环控制语句
    ```html
    {% for comment in comments $}
       {{ commment }}
    {% endfor %}
    ```
3. 继承控制语句
    
    为了避免重复造轮子，所以我们可以把重复使用的模板放入一个基础模板`base.html`中：
    ```html
    <html>
    <head>
       {% block head %}
       <title>{% block title %}{% endblock %}</title>
       {% endblock %}
    </head>
    <body>
       {% block body %}
       {% endblock %}
    </body>
    </html>
    ```
    `block`标签定义的元素可在衍生模板中修改。在上面这个代码中，我们定义了名为`head`，`body`和`title`块。注意，`title`包含在`head`中。下面这个代码是个基于`base.html`的衍生模板：
    ```html
    {% extends "base.html" %}
    {%block title %}Index{% endblock %}
    {% block head %}
        {{ super() }}
        <style>
        </style>
    {% endblock %}
    {% block body %}
    <h1>Index Page</h1>
    {% endblock %}
    ```
    `extends`指令声明这个模板衍生来自于`base.html`。在这之后，基础模板中的三个块被重新定义,模板引擎会将其插入到适当的位置。注意新定义的`head`块，在基础模板中它不是空的，所以要使用`super()`来获取原来的内容。
    
#### Flask-Bootstrap 扩展
[Bootstrap](https://getbootstrap.com/)是Twitter开发的一个开源框架。在Flask中最简单使用Bootstrap的方法是使用[Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)扩展。在虚拟环境下使用`pip`安装：
```bash
(venv) $ pip install flask-bootstrap
```
`Flask-Bootstrap`的初始化方法如下：
```python
from flask_bootstrap import Bootstrap
from flask import Flask
app = Flask(__name__)
Bootstrap(app)
```
初始化之后即可使用Bootstrap中的所有模板。下面我来用Flask-Bootstrap写一个`base.html`模板，当然，这个基础模板还是得放在`templates`文件夹下、
```html
{% extends "bootstrap/base.html" %}

{% block title %}{% endblock %}

{% block head %}
{{ super() }}
<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
{% endblock %}


{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Zerostwo</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a> </li>
                <li><a href="/">Contact</a></li>
                <li><a href="/">About</a></li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}


{% block content %}
<div class="container">
    {% block page_content %}{% endblock %}
</div>
{% endblock %}
```
其中值得注意的是，在一行中的`{% extends "bootstrap/base.html" %}`，这个的意思是使用`extends`指令从`bootstrap`中导入`bootstrap/base.html`，也就是引入了Bootstrap中的所有CSS和JS文件。
