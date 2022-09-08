from websaw import DefaultApp, DefaultContext
import ombott

ombott.default_app().setup(dict(debug=True))
class Context(DefaultContext):
    ...

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

@app.route('index')
@app.use('index.html')

def hello_world(ctx: Context):
    return dict(msg='Hello Websaw World')