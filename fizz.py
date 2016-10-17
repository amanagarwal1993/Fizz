import webapp2
import os, sys
import jinja2
from google.appengine.ext import ndb

template_dir = os.path.dirname(os.path.abspath(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#html = '''
#    <form method="post">
#    <input name="n">
#    <input type="submit">
#    </form>
#'''

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render_stuff(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class Number(ndb.Model):
    n = ndb.IntegerProperty(required = True)
    time = ndb.DateTimeProperty(auto_now_add = True)
    
class MainPage(Handler):
    # def render_main(self, results=""):
        
    def get(self):
        self.render_stuff("fizzbuzz.html")
        
    def post(self):
        n = int(self.request.get('n', 0))
        
        number = Number(n=n)
        number.put()
        q = ndb.gql("SELECT * FROM Number ORDER BY time desc")
        results = q.fetch(100)
        
        self.render_stuff("fizzbuzz.html", results = results)

app = webapp2.WSGIApplication(
    [('/', MainPage)]
    , debug = True)