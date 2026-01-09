from flask import render_template, request, redirect, url_for, send_from_directory, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from models import db, User, Post, Like, Comment


def init_routes(app):
    # Главная
    @app.route('/')
    def index():
        posts = Post.query.order_by(Post.created_at.desc()).all()

        # Добавляем дополнительную информацию к постам
        for post in posts:
            post.comment_count = Comment.query.filter_by(post_id=post.id).count()
            post.user_liked = False
            if current_user.is_authenticated:
                post.user_liked = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None

        return render_template('index.html', posts=posts)

    # Авторизация
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            if User.query.filter_by(username=request.form['username']).first():
                return render_template('register.html', error='Пользователь уже существует')

            user = User(username=request.form['username'])
            user.set_password(request.form['password'])
            if User.query.count() == 0:
                user.is_admin = True

            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()
            if user and user.check_password(request.form['password']):
                login_user(user)
                return redirect('/')
            return render_template('login.html', error='Неверный логин или пароль')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    # Файлы
    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        if request.method == 'POST':
            file = request.files['file']

            if not file or file.filename == '':
                return render_template('upload.html', error='Файл не выбран')

            ext = file.filename.lower().split('.')[-1]
            allowed = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'txt', 'doc', 'docx']

            if ext not in allowed:
                return render_template('upload.html', error=f'Формат .{ext} не поддерживается')

            # Сохраняем файл
            filename = f"{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Сохраняем в БД
            post = Post(
                title=request.form.get('title', 'Без названия'),
                filename=filename,
                user_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()

            return redirect('/')

        return render_template('upload.html')

    # Лайк
    @app.route('/like/<int:post_id>', methods=['POST'])
    @login_required
    def like(post_id):
        existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        post = Post.query.get_or_404(post_id)

        if existing:
            db.session.delete(existing)
            post.likes -= 1
        else:
            db.session.add(Like(user_id=current_user.id, post_id=post_id))
            post.likes += 1

        db.session.commit()
        return redirect(request.referrer or '/')

    # Пост
    @app.route('/post/<int:post_id>')
    def view_post(post_id):
        post = Post.query.get_or_404(post_id)
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at).all()

        # Проверяем лайк текущего пользователя
        user_liked = False
        if current_user.is_authenticated:
            user_liked = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None

        return render_template('post.html', post=post, comments=comments, user_liked=user_liked)

    # Комментарий
    @app.route('/comment/<int:post_id>', methods=['POST'])
    @login_required
    def add_comment(post_id):
        comment = Comment(
            text=request.form['text'],
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view_post', post_id=post_id))

    # Удаление
    @app.route('/delete_post/<int:post_id>', methods=['POST'])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)

        if current_user.is_admin or current_user.id == post.user_id:
            # Удаляем файл
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.filename))
            except:
                pass

            # Удаляем из БД
            Like.query.filter_by(post_id=post_id).delete()
            Comment.query.filter_by(post_id=post_id).delete()
            db.session.delete(post)
            db.session.commit()

        return redirect('/')

    # Отдача файлов
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)