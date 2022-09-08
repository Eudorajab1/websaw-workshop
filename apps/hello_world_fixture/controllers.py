from websaw import DefaultApp, DefaultContext
import ombott
from websaw.core import Fixture
from . import templates as ut

ombott.default_app().setup(dict(debug=True))

class Visited(Fixture):
    def take_on(self, ctxd: 'Context'):
        self.data.session = ctxd.session
        self.data.session['counter'] = ctxd.session.get('counter', 0) + 1

    def get_visits(self):
        return self.data.session['counter']


class Context(DefaultContext):
    visited = Visited()

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

@app.route('index')
@app.use(ut.index)
def hello_world(ctx: Context):
    visited = ctx.visited.get_visits()
    return dict(msg='Hello Websaw World', visits=visited)