from websaw import DefaultApp, DefaultContext
import ombott

from . import templates as ut

ombott.default_app().setup(dict(debug=True))
class Context(DefaultContext):
    ...

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

@app.route('index')
@app.use(ut.index)
def hello_world(ctx: Context):
    return dict(msg='Hello Websaw World')