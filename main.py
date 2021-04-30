from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class SecretForm(FlaskForm):
    # Email validator class requires email_validation download from wtforms
    email = StringField(label="email",
                        validators=[DataRequired(), Email(message="Email address must contain a '.' and '@'.")])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=8, max=50,
                                                                                  message='Password must be at least '
                                                                                          'eight characters in '
                                                                                          'length.')])
    submit = SubmitField(label='Log In')


def hello_app():
    app = Flask(__name__)
    # enables the csfr security token in the login.html form
    app.secret_key = 'el_secreto'
    # applies flask_bootstrap Bootstrap class to generated app
    Bootstrap(app)

    return app


admin_credentials = ['admin@email.com', '12345678']

app = hello_app()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = SecretForm()

    # this code runs upon submission of form, checks to see if the initialized validators are passed
    if form.validate_on_submit():
        # checks to see if specific admin requirements are met (method = POST)
        if form.email.data == admin_credentials[0] and form.password.data == admin_credentials[1]:
            return render_template("success.html")
        else:
            return render_template("denied.html")

    # this is the code that runs 'first', e.g. while the form is unsubmitted (method = GET)
    # and/or the initial validation check is unmet
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
