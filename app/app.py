from flask import Flask
from flask_login import LoginManager
import os
from models import db, User
from routes import init_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Создаем папку для загрузок
os.makedirs('uploads', exist_ok=True)

# Инициализация БД
db.init_app(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Инициализация роутов
init_routes(app)

# Создание БД и админа при первом запуске
with app.app_context():
    db.create_all()

    if User.query.count() == 0:
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("=" * 50)
        print("СОЗДАН АДМИН АККАУНТ:")
        print("=" * 50)

if __name__ == '__main__':
    print("\n=== Raha2008 готов к делу ===")
    print("Сайт: http://localhost:8080")
    print("Админ: логин 'admin', пароль 'admin123'")
    print("================================\n")
    app.run(debug=True, host='0.0.0.0', port=8080)