import os
from websaw import DefaultApp, DefaultContext, Reloader
from . import templates as ut
pjoin = os.path.join

class Context(DefaultContext):
    ...
    
ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

@app.route('myinfo')
@app.use(ut.index)
def info_app(ctx: Context):
    def rep(v):
        if isinstance(v, list):
            return [rep(_) for _ in v]
        if isinstance(v, str):
            return v
        return repr(v)

    ret = {
        k: rep(v) for k, v in ctx.app_data.__dict__.items()
    }
    ret['env'] = ctx.env
    return dict(msg=ret)
