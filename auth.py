import functools

from flask import redirect, g, url_for


def fully_authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


def admin_granted(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.admin:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
