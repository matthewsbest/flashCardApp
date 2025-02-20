import os
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    progress = db.relationship('Progress', backref='user', lazy=True)

# Define Progress Model
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    words_completed = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        progress_data = Progress.query.filter_by(user_id=current_user.id).all()
        progress_dict = {p.level: p.words_completed for p in progress_data}
        return render_template('index.html', levels=word_lists.keys(), progress=progress_dict)
    return redirect(url_for('login'))

@app.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    data = request.get_json()
    level = data.get('level')
    words_completed = data.get('words_completed')

    progress = Progress.query.filter_by(user_id=current_user.id, level=level).first()
    if not progress:
        progress = Progress(user_id=current_user.id, level=level, words_completed=0)
        db.session.add(progress)

    progress.words_completed = words_completed
    db.session.commit()

    return jsonify({"message": "Progress updated successfully!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
