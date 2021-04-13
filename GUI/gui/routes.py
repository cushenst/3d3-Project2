from flask import render_template, url_for, flash, redirect
from gui import app
from gui.forms import RegistrationForm, LoginForm
from gui.models import User, Post
from flask import Flask, request, render_template, jsonify
import json

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    }
]

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/send',methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        message = request.form['message']
        priority = request.form['priority']
        json_var = jsonify(request.form)
        return jsonify(request.form)

        return render_template('send.html', message=message, priority=priority)
    return render_template('home.html')

