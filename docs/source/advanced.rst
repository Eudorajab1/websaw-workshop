
.. _advanced:

==================
Advanced Tutorials
==================

3.1 : UPYTL In Depth
--------------------

This is a follow on from the introduction to **UPXTL** in the **Getting Started** section where we will explore 
in more detail various areas of functionality

But for now lets head over to our working app directory and create a file called *components.py* and paste the following code.
::
    ## components.py ##

    from upytl import (
        Component, Slot, SlotTemplate, UPYTL, html as h
    )
    
    # flake8: noqa E226

    # Let's define some custom reusable components

    class HTMLPage(Component):
        props = dict(
            footer_class='page-footer',
            page_title="This page has no title :(, but it's fixable - just `HTMLPage(page_title='awesome')`"
        )
        template = {
            h.Html(): {
                h.Head():{
                    h.Title(): '[[page_title]]',
                    h.Meta(charset=b'utf-8'):'',
                },
                h.Body():{
                    Slot(SlotName=b'nav'):{h.Div(): '[there is no default nav]'},
                    Slot(SlotName=b'content'):{h.Div(): '[there is no default content]'},
                    Slot(SlotName=b'footer'):{
                        h.Div(
                            Class='{footer_class}',
                            Style={'margin':'30px', 'font-family':'monospace', 'font-size':'20px'}
                        ): {
                            h.Text(): 'Created using ',
                            h.A(href={'URL()'}): 'UPYTL',
                        }
                    },
                },
            },
        }

    class Field(Component):
        props = dict(
            name='[no name]',
            value='',
            type='text',
            options=[],
        )

        template = {
            h.Label(If='type=="text"'):{
                h.Text():'[[name]]',
                h.Input(name='{name}', value='{value}'):''
            },
            h.Label(Elif='type=="select"'):{
                h.Text():'[[name]]',
                h.Select(name='{name}'):{
                    h.Option(For='opt in options', value='{opt[value]}', selected={'opt["value"]==value'}):
                        '[[ opt.get("name", opt["value"]) ]]'
                },
            },
        }

    class Form(Component):
        props = dict(
            fields=None
        )
        template = {
            h.Form(If='fields', action='#'):{
                h.Div(For='fld in fields', Style={'margin':'15px'}):{
                    Field(
                        name='{fld[name]}',  type={'fld.get("type", "text")'},
                        value={'fld.get("value", "")'},
                        options={'fld.get("options", None)'},
                    ):'',
                },
                h.Button(type='submit'): 'Submit'
            },
            h.Div(Else=''): 'Sorry, no fields were passed to this form'
        }

.. important::
    While this may seem like a lot of code all the above components DO ship with **UPYTL** and can be used
    * out-of-the-box * .  

So lets take a look at whats happening here.

    * First of all we import all the required base classes from **UPYTL** which we will use to create our own components. 
    * Using these base classes we then create our **Page** component which is roughly equivalent to our 'layout_app.html'.
    * We then create a 'text type field' component to illustrate functionality
    * And finally we define our custom **Form** component.

Before we go too much further lets take a look at what we are working with. For those of you familiar with 
**Vue.js** you will already understand the concepts of **Slots** and **Props** but for those who are not lets take a look 
at what these are.

In very broad terms we can consider **Slots** as the means of passing data between **Components** while **props** are
essentially the means for getting data from the *application* into the component. There if obviously a lot more to it than 
that but unfortunately that is beyond the scope of this document.

Each **Compent** typically has a dictionay of **props** and a **template** dictionary which effectivey styles the compnent
and does any special processing for the compnent.

Lets take a look at our **Field** component in more detail:
::
    class Field(Component):
        props = dict(
            name='[no name]',
            value='',
            type='text',
            options=[],
        )

        template = {
            h.Label(If='type=="text"'):{
                h.Text():'[[name]]',
                h.Input(name='{name}', value='{value}'):''
            },
            h.Label(Elif='type=="select"'):{
                h.Text():'[[name]]',
                h.Select(name='{name}'):{
                    h.Option(For='opt in options', value='{opt[value]}', selected={'opt["value"]==value'}):
                        '[[ opt.get("name", opt["value"]) ]]'
                },
            },
        }

Starting with the **props** you can see we are expecting to receive the following from the app.

    * name='[no name]'
    * value=''
    * type='text'
    * options=[]

all of which have been intialised with default values.

Looking at our **template** section we start to see the power of our component.

The first thing to notice is that the h.Label() is conditional based on the 'type' property passed in from the app.

So if its a 'text' field we generate a text div and an input div. If it is a 'select' field we generate additional divs.

.. important::
    It is very important to note that the same 'Field' component can alter its output significantly depending on the 
    properties.
    This saves us the overhead of writing multiple 'Field' compnents for any field type as in the case above.

    There will be a lot more on this later in the advanced tutorials but for now note that we are barely scratching the surface.

Lets move on and take a look at our **Form** component.
::
    class Form(Component):
        props = dict(
            fields=None
        )
        template = {
            h.Form(If='fields', action='#'):{
                h.Div(For='fld in fields', Style={'margin':'15px'}):{
                    Field(
                        name='{fld[name]}',  type={'fld.get("type", "text")'},
                        value={'fld.get("value", "")'},
                        options={'fld.get("options", None)'},
                    ):'',
                },
                h.Button(type='submit'): 'Submit'
            },
            h.Div(Else=''): 'Sorry, no fields were passed to this form'
        }

As you can see our **Form** component takes as props a list of **Fields**. These are typically a list of Companents like our 
**Field** component and can be any number of fields we wish to pass into the form. Under the hood the form 
will sort out all the fields and display them based on each componenet definition as can be seen here.
::
    h.Div(For='fld in fields', Style={'margin':'15px'}):{
        Field(
            name='{fld[name]}',  type={'fld.get("type", "text")'},
            value={'fld.get("value", "")'},
            options={'fld.get("options", None)'},
        ):'',
    },

But hang on a minute! The **Form** component is inheriting the values from the **Field** component. What is that all about?

This is possibe as the **Field** component is passed in to the form as a prop

In addition you can see that we can **Style** individual secions of the **Form** in our **Form** template

Finally if no **Fields** we supplied to the **Form** component we generate the appropriate message.

So far we have seen the use of the followingn in our **template**:

    * for-loop
    * if-elif-else

Finally we will take a look at the **HTMLPage** component where it will all come together.
::
    class HTMLPage(Component):
        props = dict(
            footer_class='page-footer',
            page_title="This page has no title :(, but it's fixable - just `HTMLPage(page_title='awesome')`"
        )
        template = {
            h.Html(): {
                h.Head():{
                    h.Title(): '[[page_title]]',
                    h.Meta(charset=b'utf-8'):'',
                },
                h.Body():{
                    Slot(SlotName=b'nav'):{h.Div(): '[there is no default nav]'},
                    Slot(SlotName=b'content'):{h.Div(): '[there is no default content]'},
                    Slot(SlotName=b'footer'):{
                        h.Div(
                            Class='{footer_class}',
                            Style={'margin':'30px', 'font-family':'monospace', 'font-size':'20px'}
                        ): {
                            h.Text(): 'Created using ',
                            h.A(href={'URL()'}): 'UPYTL',
                        }
                    },
                },
            },
        }

First off we can see that it, like all componets, takes a dict of props with default values.

In our case we have two props namely the footer_class and page_tile. What this means is that every page can effectively
have a different footer_class and page_title.

Next we look at the **Body** section where we can see that we are introducing the **Slot** feature of components.

Basically this **component** is acting as a placeholder for all the components that we want on our **Page**.

You will notice that the first two **Slots** will use the styling of the slot component **temlate** whereas the footer slot adds its own styling.

Now that we have created our **custom components** lets see how they all work.

In order to do that we need to create one more file which we will use to store our custom page template.

so lets create a file called templates.py in the same directory as our componenets.py and paste in the following:
::
    ## templates.py ##

    from . components import * ## import all our components for now 

    index = {
        HTMLPage(footer_class='custom-footer', page_tile='Hello World UPYTL'):{
            SlotTemplate(Slot='content'):{
                h.Div():{
                    Form(fields={'fields'}):''
                }
            }
        }
    }

.. note ::
    We could have easily included the template in the coponents.py but for the sake of clarity it is much better to keep them seperate
    particularly as your app grows.


So whats going on here?

We are using our HTMLPage component passing in a custom-footer clas that will efectively intialise the footer-class prop in our componets and 
use the appropriate styling for the footer.

We are also passing in our custom 'page-title' for the component to use.

Finally we are using the SlotTemplate method to initilaise the page with the **Form** component.

The last thing we need to do is open up our controllers.py, import our template and tell our action to use the 'index' template as opposed to 'index.html'

so lets do that:
::
    ## controllers.py ##
    ...
    from . templates import index
    ....
    @app.use('index')


Our complete action should now look like this:
::

    @app.route('index')
    @app.use('index')
    def hello_world(ctx: Context):
        return dict(msg='Hello Websaw World')


3.2 : Simple Chat App
----------------------

Creating our server app
.......................

Under Construction

Creating our client app
.......................

Under Construction

Getting them talking 
....................

Under Construction

Adding Rooms
............

Under Construction

3.3 : Using Mixins
-------------------

Under Construction
