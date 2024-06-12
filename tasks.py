from invoke import task

@task
def initdb(contex):
    from Viliar.src.extensions.sqla import db
    from Viliar.factory import app
    with app.app_context():
        db.create_all()

@task
def server(contex, host="0.0.00", port=5000, pty=False, gunicorn=False):
    if not gunicorn:
        command = "python3 Viliar/factory.py"
        contex.run(command, pty=False)
