from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash

from auth import admin_granted
from db import get_user_repository
from model.user import User

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@admin_granted
def users_list():
    user_repository = get_user_repository()
    username = request.args.get('username')

    if username is not None:
        users = user_repository.find_all_by_column('username', username)
    else:
        users = user_repository.find_all()

    return render_template('users/list.html', users=users, username=username)


@bp.route('/create', methods=("GET", "POST"))
@admin_granted
def users_create():
    user_repository = get_user_repository()
    user = User(None, '', '', 'USER')
    errors = []

    if request.method == "POST":
        user.username = request.form['username']
        user.admin = request.form['role'].upper() == 'ADMIN'

        if len(request.form['password']) > 0:
            user.password = generate_password_hash(request.form['password'])

        errors = user_repository.validate(user)

        if len(errors) == 0 and \
                user_repository.save(user) is not None:
            flash('User created.')
            return redirect(url_for('users.users_list'))

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
        create=True
    )


@bp.route('/<int:user_id>/edit', methods=("GET", "POST"))
@admin_granted
def users_edit(user_id):
    user_repository = get_user_repository()
    user = user_repository.find_one_by_id(user_id)
    errors = []

    if request.method == "POST":
        user.username = request.form['username']
        user.admin = request.form['role'].upper() == 'ADMIN'

        if len(request.form['password']) > 0:
            user.password = generate_password_hash(request.form['password'])

        errors = user_repository.validate(user)

        if len(errors) == 0 and \
                user_repository.save(user) is not None:
            flash('User saved.')

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
        create=False
    )


@bp.route('/<int:user_id>/delete', methods=["POST"])
@admin_granted
def users_delete(user_id):
    user_repository = get_user_repository()
    if user_repository.delete(user_id) is not None:
        flash('User deleted.')

    return redirect(url_for('users.users_list'))
