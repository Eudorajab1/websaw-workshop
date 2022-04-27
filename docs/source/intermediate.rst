.. _intermediate:

======================
Intermediate Tutorials
======================

In this set of **Tutorials** we are going to focus on creating slightly more usefull **Websaw** *fixtures* and *mixins* 
both of which are fundamental building blocks for any **Websaw** application.

In order to understand what  **fixtures** and **mixins** are used for please refer to the appropriate `Websaw User Guide <https://websaw-userguide.readthedocs.io/en/latest//>`_ 
sections for a more in depth description. For the purposes of these tutorials we assume you are already familiar with
these concepts.

In addition we are going to be introducing **Pyjsaw** for the first time and showing you how to install it and create 
awesome SPA's in **Websaw**

SQLite3 Fixture
---------------

In this turorial We are going to make the fixture equivalent of https://flask.palletsprojects.com/en/2.0.x/extensiondev/
as a comparison to those of you familiar with flask extensions.

So lets get going and create our **fixture**.
::

    # apps/sqlite3_demo/app_fixtures.py

    import sqlite3

    from websaw.core import Fixture

    class SQLite3(Fixture):
        def __init__(self, uri_or_fpath, **kwargs):
            self.uri_or_fpath = uri_or_fpath
            self.kwargs = kwargs

        def take_on(self, ctx):
            # self.data - thread safe local storage 
            conn = self.data.db = sqlite3.connect(self.uri_or_fpath, **self.kwargs)
            conn.row_factory = sqlite3.Row
            return conn

        def take_off(self, ctx: DefaultContext):
            db: sqlite3.Connection = self.data.db
            if ctx.exception:
                # there is some error(s) during action processing or/and
                # in other fixtures, so we don't want to save changes
                db.rollback()
            else:
                db.commit()
            db.close()


Now lets put it to use:
::

    # apps/sqlite3_demo/controllers.py

    import sqlite3

    from websaw import DefaultApp, DefaultContext, Reloader, HTTP
    from websaw.core import Fixture

    from .app_fixtures import SQLite3

    sqlite_db = Reloader.package_folder_path(__package__,  'demo_db.sqlite')

    # lets create the table in our db
    def init_db(sqlite_db):
        db = sqlite3.connect(sqlite_db)
        db.execute('CREATE TABLE IF NOT EXISTS thing(id INTEGER PRIMARY KEY, name TEXT)')

    init_db(sqlite_db)


    # extend default context with our fixture
    class Context(DefaultContext):
        # to get right autocomplete in action (e.g. when ctx.sdb.exe...)
        # we need to force IDE to think that cxt.sdb is type of sqlite3.Connection
        sdb: sqlite3.Connection = SQLite3(sqlite_db)

    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)

    @app.route('sdb')
    def sdb(ctx: Context):
        q = ctx.request.query
        action = q.get('action')
        if not action:
            cur = ctx.sdb.execute('SELECT * FROM thing')
            ret = [{**r} for r in cur.fetchall()]
        elif action == 'create':
            name = q.get('name')
            if not name:
                raise HTTP(429, 'Name is required')
            cur = ctx.sdb.execute('INSERT INTO thing(name) values(?)', (name,))
            ret = cur.lastrowid
        else:
            raise HTTP(400, f'Unkown action: {action}')
        return dict(result=ret)

Now we need to mount our app so 
::

    # apps/sqlite3_demo/__init__.py

    from .controllers import app
    
    app.mount()

And finally lets test it:
::

    # to insert any name into db
    http://127.0.0.1:8000/sqlite3_demo/sdb?action=create&name=John

    # to view all rows in db
    http://127.0.0.1:8000/sqlite3_demo/sdb

And that is pretty much it for this tutorial. Pretty awesome stuff!!

Pyjsaw
------
In this tutorial we will walk through installing **Pyjsaw** into our working environment, take a look at the IDE
and create a fully functional ToDo app. There is no additional integration required with **Websaw**.

Installation
............

The IDE
.......

Pyjsaw Todo App
...............

