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

2.1 : SQLite Fixture
--------------------

In this turorial We are going to make the fixture equivalent of https://flask.palletsprojects.com/en/2.0.x/extensiondev/
as a comparison to those of you familiar with **Flask** amd flask extensions.

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

2.2 SPA's
---------
In this tutorial we will walk through two diffent way to build **SPA's** or **client side** apps with **WebSaw**.

We will look at using the following:-

    * **Vue.js**
    * **PyJsaw**

Using Vue.js  
............

Under construction

Introduction
::::::::::::

Under construction

Checking dependancies
:::::::::::::::::::::

Under construction

The Vue Todo App
::::::::::::::::

Under construction

Using PyJsaw
............

What is PyjSaw?
:::::::::::::::

**Pyjsaw** in its simplest terms is a sophisticated transpiler that allows us to develop SPA's in a more 
pythonic way inlcuding components, store and all the other good **Vue** things required for client side application processing.

Irrespective of the size and complexity of the app we are building we will always end up with a single **.js** file
commonly **index.js** which is the entry point for our SPA.

The **Pyjsaw** IDE is a good example of the power of **Pyjsaw** as it was written using **Pyjsaw** itself.

Installation
::::::::::::

Installation of **Pyjsaw** can be done via **PYPI** or installing from **Github**. Either way it integrtates semailessy
with **WebSaw** and can be viewed as part of the **WebSaw** framework.

To install **Pyjsaw** in your websaw working environment simply open a terminal window

If you are using a venv (reccomended) make sure you have it activated before installing **Pyjsaw**.
::

    source ./bin/activate
    cd websaw #if not already in the websaw directory
    pip install https://github.com/valq7711/pyjsaw/archive/main.zip

In order to test the installation make sure that websaw is still running then head on over to your 
browser and
::

    http://localhost:8000/pyjsaw

If all is good you should see recieve prompt for the administrator password.

If you do not see this it may well be that you have not set up the **Websaw** admin password when installing **Websaw**.

In order to do this from your command prompt or terminal window type the following:
::
    cd websaw # if you are not already there
    python -m websaw set_password

You will be prompted to enter and confirm the admin password of your choice.

If all is good you can now run **Websaw** again from the terminal as such:
::
    python -m websaw run apps

Head on back to your browser and refresh and you should be prmpted to enter and re-enter the admin 
password.

If that does not work please refer to the `Websaw User Guide <https://websaw-userguide.readthedocs.io/en/latest/getting_started.html>`_
and take a look at the **Installytion** seciton for further information.

All things being good you should see the **Pyjsaw** IDE in your browser.
 
Time to create some amazing apps!!

The IDE
:::::::

Under construction

Pyjsaw Todo App
:::::::::::::::

Under Construction
