from websaw import DefaultApp, DefaultContext
import ombott

from ..mixins import myinfo

from . import templates as ut

ombott.default_app().setup(dict(debug=True))

class Context(myinfo.Context, DefaultContext):
    ...

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

# use mixin(s)
app.mixin(myinfo.app)

@app.route('index')
@app.use(ut.index)
def hello_world(ctx: Context):
    return dict(msg='Hello Websaw World')