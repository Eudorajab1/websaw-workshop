
.. _getting_started:

Getting Started
===============
   
Assuming you have successfully installed *Websaw* as per the `Websaw User Guide <https://websaw-userguide.readthedocs.io/en/latest/getting_started.html/>`_ 
we are ready to go. If not please install and verify your installation using the above link.



1.1 : Hello World
-----------------

As per tradition we are going to create a simple Hello World app to understnad the basics of the *Websaw* framewok 
after which we will get into a lot more depth and detail regarding the tools and techniques being used.

Please ensure that you have a websaw/apps folder with either the example apps as subfolders or an empty ``__init__.py`` file in the root
before you continue.

Now we can create our hello_world app folder as such:
::
    mkdir hello_world
    cd hello_world
    touch __init__.py


Now in our apps/hello_world folder we should have a single file __init__.py. If you have copied an existing folder or 
renameed an exisrting example we reccomend deleting everything other than the __init__.py in order to follow this example.

Now that we have our directory structure sorted out lets get coding!!.

Before we dive in however there a number of differnt conventions that can be used for python projects. 
Looking at differnt covnetions is beyond the scope of this workshop and we suggest that your apps take 
on a structured approach with modules and sub folders.

To this end lets start off by creating a controllers.py to hold all of our **actions**.
::

    touch . controllers.py

.. important:: 

    For the sake of clarity an **action** in **WebSaw** is deemed to be a **routeable function**
    There will be a lot more about **routes** a little bit later

Then lets open **controllers.py** in the editor of choice and add the following code.
::

    ### controllers.py ###

    from websaw import DefaultApp, DefaultContext
    import ombott
   
    ombott.default_app().setup(dict(debug=True))
    class Context(DefaultContext):
        ...

    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)

    @app.route('index')
    def hello_world(ctx: Context):
        return 'Hello Websaw World'

*So what is going on here?*

First we import the **App** and **Context** base clases from *Websaw* along with the **ombott** (or any other compatible webserver) package. 
More inofrmation on bottle can be found at `The Official Bottle Site <https://bottlepy.org/docs/dev/>`_

Next we create our **Context** class using the imported **DefaultContext** as our base class and pass it to our app intitiliser

As we dont need anything else for now in our **context**  we can simply use the standard **Default** context. 
In later chapters you will see how we can customise and leverage the local **Context** in order to make our applications extremely 
flexible yet super secure.

Next we set up our app using the **DefaultApp** as our base class. This will effecively procide us with all the hooks and mehods needed
to run our app. 

.. note:: 

    All the above could be done in any other module and imported but for the sake of readablilty lets keep it all here for now.

    **example:** If you have an app with multiple modules we suggest you create a common.py module where all initialisation is done 
    then you can simply imprt what you need into each module but more on that later.

Then we get to our actual **action**.

The first thing we need to do is declare our **route**. This lets our app know where to find the function **hello_world**.

There will be a lot more on **Routes** later on but for now lets just register a route called 'index'

.. note:: 
    
    We do not need seperate routing tables setup. This is all done by *Websaw* under the hood by using the convenice 
    **app.route** decorator.


Followd by our function decleration. Once again it is important to note that the route and function 
names need not be the same. For the sake of clarity the **route** name will always take precedence over the function name and there is nothing
to stop us declraring multiple **routes** to the same **function**

In this case as we only have one function in our module it is common convention to register our route as **index** as 
you will see later. The **index** route is typically the entry point inot most web applications.

.. important:: 
    
    All **actions** in *Websaw* take context as a mandatory first argument

and all that ourt **action** now needs to do it return our 'Hello Webasw World' string.

Before we can actually run the application there are a few more things we need to do 

You can close and save controllers.py and open __init__.py

.. note:: 

    Once aganin we could probably have all this code in a single module but as your app grows it 
    becomes paramount to have things structured.

Add the following:
::

    ## __init__.py ##
    
    from .controllers import app

    app.mount()

The above should be pretty self expanatory in that we import our **app** instance from our controllers.py and then 
then mount our app using **app.mount()**

You can now save and close the __init__.py

Thats it. Lets check it out.

In your terminal run the following:
::

    python -m websaw run apps

head over to your browser and 
::

    http://localhost:8000/hello_world

All things being well you should see the reults of your very first **WebSaw** app

Not very exciting and not very pretty but the foundation for things to come.

.. note::

    We declared our route as 'index' in our app but not on our URL. *Websaw* automatially defaults to /index
    if forget to add it and in effect http://localhost:8000/hello_world and http://localhost:8000/hello_world/index
    are equivalent

Congratulation you have completed your first **WebSaw** application.

Before moving on lets recap what we have covered so far in this **tutorial**

    * We created an application using the *Default* websaw settings
    * We told our application to use the *Default* context 
    * We created and registered a route *index*
    * We linked this route to our function which returns our application output   


1.2 : Working with Templates
----------------------------

Templates are the traditional way to give application a uniform *look and feel* whilst at the same
time allowing you to use one or more standard .css styling libraries including your own custom styling.

In this tuorial we are going to explore different ways to render or format the output of our **actions** using templates.

We will take a look at both the *traditional* HTML/CSS approach which most developers will be familiar with and will introduce
**WebSaw's** *preferred* method of rendering HTML using **UPYTL**.

Ultimately it is entirely up to you which mehtod you choose or you could even mix both in your apps so lets get to it.

Using HTML Templates
....................

If you are not familiar with HTML and CSS there are many excellent sites that can get you up to speed quickly and it is beyond the scope
of this document to cover this.

That having been said lets jump into adding a bit of 'zing' to our otherwise drab and sad looking *hello_world* app.

All the code for this tutorial can be found in the `Websaw Workshop <https://github.com/Eudorajab1/websaw-workshop.git>`_ apss/hello_world_html
so you can either copy your *hello_world* folder into *apps/hello_world_html* or just keep working in your *hello_world* folder. Choice is yours.

The first thing we need to do is create a directory where we will be storing our templates. By convention we call this 
directory **templates** and create and empty __init__.py.

From within your hello_world or hello_world_html directory run the following:
::

    mkdir templates
    touch templates/__init__.py
    cd templates

Now with your editor of choice create a new file called **app_layout.html** which we will use as our application
wide template.

Once open lets add the following:
::

    ## templates/app_layout.html ##
    <!DOCTYPE html>
    <html>
      <head>
        <base href="[[=URL('static')]]/">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" href="data:image/x-icon;base64,AAABAAEAAQEAAAEAIAAwAAAAFgAAACgAAAABAAAAAgAAAAEAIAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAPAAAAAA=="/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" />
        [[block page_head]]<!-- individual pages can customize header here -->[[end]]
      </head>
      <body>
        <header>
        <!-- Navigation bar -->
          <nav class="navbar is-light" role="navigation" aria-label="main navigation">
            <a class="navbar-item " href="#">
              <div class="has-text-primary is-size-5 has-text-weight-semibold">Home</span>
            </a>
            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="my-navbar">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>

            <!-- Left menu ul/li -->
            [[block page_menu_items]]<!-- individual pages can add menu items here -->[[end]]

            [[block page_left_menu]][[end]]
            <!-- Right menu ul/li -->
          </nav>
        </header>
        <!-- beginning of HTML inserted by extending template -->
          [[include]]
        <!-- end of HTML inserted by extending template -->
        <footer class="footer is-small">
          <div class="content has-text-centered">
            <p>Powered by <strong>&nbsp;WEBSAW</strong> <a href="https://websaw.com"></a>
            </p>
          </div>
        </footer>
      </body>
      [[block page_scripts]]<!-- individual pages can add scripts here -->[[end]]
    </html>

Feel free to use the styling library of your choide. Here we are using **Bulma** but we could equally well have used
**Bootstrp** or eve **no.css**. The choice is really yours.

.. note::
    Here we are using the cdn's which is again by choice. If you wanted to use local files you need to create a 
    **static** folder in the hello_world or hello_world_html app and create a **css** and **js** subfolder.

The most important thing to notice here is the **[[include]]** directive. We will extend all our templates (.html files) 
with this app_layout.html to give them a consitant and similar look and feel.

It also saves us the hassle of having to import libraries for every template we generate.

So .. now that we have our app layout sorted out .. lets take a look at what we can to do with our application.

We start by creating a new file called **index.html** which will extend the app_layout.html as follows:
::
    ## templates/index.html ##

    [[extend "app_layout.html"]]
    <div class = "columns">
      <div class = "column has-text-centered">
        <div class = "notification is-primary">
          [[=msg]]
        </div>
      </div>
    </div>

and that should be it.

.. note:: 

    [[=msg]] is the information that we will display on this page as proviced by our hello_world function.
    
So lets head over to our controllers.py and see what we need to do.

The first thing we need to do is to tell our function to use the index.html template. We do this by adding the 
followng:
::
    ### controller.py ###

    @app.use('index.html')

.. note:: 

    This should be declared after the route directive and before the function decleration

*So what is all this about?*

In much the same way our convenience decorator **@app.route(...)** tells **WebSaw** that we want to declare and register
a route our convenience decorator **@app.use(...)*** is telling **WebSaw** that we want to add something to our 
**local application context**. In this case it is our html template called *index.html*

**WebSaw** has a built in **template fixture** that deals with initialising and rendering our index.html all under the hood and we 
dont have to do anything else right now. 

Using UPYTL
...........

**UPYTL** is an acronym for **Utlimate Python Templating Language** and as the name suggests it allows us to build our templates
in a *pythonic* way and is inspired by **Vue.js**. 

In much the same way that **Vue** leverages the use of reusable components for client side processing, **WebSaw**
leverages the use of *re-usable* components for client/server applications.

All the code for this tutorial can be found in the `Websaw Workshop <https://github.com/Eudorajab1/websaw-workshop.git>`_ apss/hello_world_upytl
so you can either copy your *hello_world* folder into *apps/hello_world_upytl* or just keep working in your *hello_world* folder. Choice is yours.

If you havent already done so and in order to follow this turorial now is the time time to install **UPYTL**

Insatllaion is extremely straight forward as follows:
::
    pip install upytl

.. important::
    Make sure you are still in your virtual environment before installing unless you want UPYTL available globally

**UPYTL** ships with a number of standard components which can be used *out of the box* but for the purposes of this 
tutorial we will be building a simple template of our own from scratch.

As this is a very simple application and we want to compare apples with apples we will be using only the elements
of **UPYTL** relevent to this app. For a much more in-depth look at **UPYTL** and creating custom components such as **Pages**, **Forms** and 
custom **Field types** you can head over to the **Advanced Tutorials** section of this user guide where **UPYTL** is covered in a LOT more depth.

The first thing we need to do is to create a module / library to store our components /templates. Later on we will make this 
library available to all of our apps by leveraging on **WebSaw's** built in **mixin** functionality.

But for now lets head over to our app directory and create a file called *templates.py* and paste the following code.
::
    ## templates.py ##
    from upytl import html as h
    
    index = {
        h.Html():{
            h.Head():{
                h.Title():"[[app_get('app_name')]]",
                    h.Meta(charset='utf-8'):'',
                    h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css'):None, 
                },
                h.Body():{
                    h.Nav(Class='navbar is-light', role='navigation'):{
                        h.A(Class='navbar-item',  href="#"):{
                            h.Div(Class='has-text-primary is-size-5 has-text-weight-semibold'):'Home'
                        },
                    },
                    h.Div(Class = 'columns'):{
                        h.Div(Class='column has-text-centered'):{
                            h.Div(Class='notification is-primary'):'[[msg]]',
                        },
                    },
                },
                h.Footer():{
                    h.Div(Class='subtitle has-text-centered'): 'This is the footer generated by UPYTL',
                }
            }
        }

    
As you can see our **HelloWorld** component does not do much and its sole purpose in life if to receive a message from
our **Hello World ** action response with a bit of styling thrown in.

.. note ::
    We could have easily included the template in the controller.py but for the sake of clarity it is much better to keep them seperate
    particularly as your app grows.


The last thing we need to do is open up our controllers.py, import our template and tell our action to use the 'index' template as opposed to 'index.html'

so lets do that:
::
    ## controllers.py ##
    ...
    import . templates as ut
    ....
    @app.use(ut.index)

Our complete action should now look like this:
::
    ## controllers.py ##
    
    @app.route('index')
    @app.use(ut.index)
    def hello_world(ctx: Context):
        return dict(msg='Hello Websaw World')

Great ... lets run it.

We should see a by now very familiar message in our browser.

We will leave it up to you to decide which method you chose to render html in **WebSaw** but from now on we will 
be aiming the tutorials toward **UPTL** as our preferred rendering method.

In the next tutorial we will be creating a custom **fixture** which we will add to our application in order
to demonstrate the power and flexibility of **WebSaw** fixtures.

1.3 : Introducing Fixtures
--------------------------

*Websaw* has a number of "out of the box" fixtures which we can subclass or extend in order to generate 
specific functionaltiy that we may need within the context of our application. 

These are all detailed extensively in the `Websaw User Guide <https://websaw-userguide.readthedocs.io/en/latest/fixtures.html>`_
and you have already used the **Template** fixture by including the ``app.use('index.html')`` in your hello_world_html app.

For now the important things to note about **Fixtures** are as follows:

  * they are only initialised when required (on the fly).
  * they are context specific and can comprise of other fixtures.
  * they are completely thread safe and secure.

So lets get to it. Our objective is to create a simple *fixture* that will simply count the number of times a particular
browser has visited our site.

We can extend this later to store the results in a database of our chosing but for now we will use the session
to keep a count.

As the session itself is a **fixture** we will leverage this by getting our fixture to initialise the session when needed.

So lets get going.

We are going to focus on the hello_world_upytl app as the basis for our turorial so go ahead and copy the 
hello_world_upytl app into a new folder called hello_world_fixture.

Next lets head into our newly created app and get busy.

.. note ::
    As usual the complete code for this turorial can be found in the apps/hello_world_fixture folder on github.


The first thing we need to do is to import the Fixture base class from websaw.core
::

    from websaw.core import Fixture

Then we can define our new fixture called **Visited** as follows:
::
    ### controllers.py ###

    class Visited(Fixture):
        def take_on(self, ctxd: 'Context'):
            self.data.session = ctxd.session
            self.data.session['counter'] = ctxd.session.get('counter', 0) + 1
            
        def get_visits(self):
            return self.data.session['counter']

Lets examine this code in a bit more detail.

As per the `Websaw User Guide <https://websaw-userguide.readthedocs.io/en/latest/fixtures.html>`_ we can see that 
there are three main methods that we can use when using a fixture.

    * app_mounted()
    * take_on()
    * take_off()

The app_mounted() which is used specifically when the app is mounted or intialsised is of no real interest to us at this point in time 
but will be covered later.

The method that we are interested in for the sake of this excercise is the take_on() method which we will use to tell our 
fixture that we want it to start working only when an action that uses it is accessed.

We then add a custom fixture method called get_visits which we will use in our action to access our fixture data and include
it to our application context.
::
    ## controllers.py##
    
    class Context(DefaultContext):
        visited = Visited()

By adding our **Fixture** to the application context as above, all actions in the application will have access to our fixture.

Alternatively we can let only one or more actions use our fixture simply by removiing from the app context and installed
including it in the **@app_use(...)** decorator for each action required.

For now as we only have one action it is neither here not there.

In our action we now can use our new fixture simply by adding the following code
::
    ## controllers.py ##
    
    ....
    def_index(ctx):
        ...
        visited = ctx.visited.get_visits()
        ...
where ctx is our **context**, **visited** is our **custom fixture** and **get_visits()** is our custom fixture method.

and we simply add visted to the dictionary we are returning to the template
::
    ## controllers.py ##
    
    ...
    return dict(msg='Hello Websaw World', visit=visited)

*But Hang on just a second here !!*

Where did the **session** come from all of a sudden in our action? and more importantly how come it is 
available all of a sudden in our action?

.. important:: 

    *Simply by touching the session in our fixture we initialise and make it available in our action by using ctx*

Now all that is left for us to do is to style and display the infomration in our template as such:
::
    ## templates.py##
    
    index = {
    h.Html():{
        h.Head():{
            h.Title():"[[app_get('app_name')]]",
                h.Meta(charset='utf-8'):'',
                h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css'):None, 
            },
            h.Body():{
                h.Nav(Class='navbar is-light', role='navigation'):{
                    h.A(Class='navbar-item',  href="#"):{
                        h.Div(Class='has-text-primary is-size-5 has-text-weight-semibold'):'Home'
                    },
                },
                h.Div(Class = 'columns'):{
                    h.Div(Class='column has-text-centered'):{
                        h.Div(Class='notification is-primary'):'[[msg]]',
                        h.Div(Class='title'):'You have now visited me [[visits]] times',
                    },
                },
            },
            h.Footer():{
                h.Div(Class='subtitle has-text-centered'): 'This is the footer generated by UPYTL',
            }
        }
    }

Or use any other styling you prefer.

.. note::
    We have added a single line of code to our template that displays the number of visits.

If you have **WebSaw** running just head over to http://localhost:8000/hello_world_fixture ad you will see our all new hello_world_fixture app.

If you refresh your browser a few times you should see the counter increasing. If not please retrace your 
steps in the tutorial and see where you have gone wrong.

We could equally well access the ctxd.session object and increment it directly in our **hello_world** action 
but now **ANY** action using our **ctxd** that requires a count of the visits can access our **Visits** fixture or not
as the case may be.

And that just about wraps up our **Getting Started ** tutorials apart from a brief recap.

So far we have seen how the three main layers of **WebSaw** in action.
    
    * **Fixture**
    * **Context**
    * **Application**

We have seen the different methodologies we can use to render our output and we have created a simple custom 
fixture that we can extend to log all visits to a db or log files or wherever we want.

** Congratulations ** you have completed the first part of the journey to becomming a proficient web application developer using 
**WebSaw**
 
 In the next set of tutorials we move away from our hello_world app and look more at more usefull 'real-life' type apps which will demonstrate even more 
 of **WebSaw's** awesome functionality.
