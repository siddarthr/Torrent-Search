import webapp2

import feedparser

import logging

import urllib

from webapp2_extras import jinja2

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
        
# Class MainHandler now subclasses BaseHandler instead of webapp2
class MainHandler(BaseHandler):
    
    # here we handle the results of the form
    def post(self):

        # this retrieves the contents of the search term 
        terms = self.request.get('search_term')

        # and converts it to a safe format for use in a url 
        terms = urllib.quote(terms)

        # NOTE: we are now repeating (almost verbatim) things from 
        # the get method. It would be better to create and call a helper method
        # that retrieves and constructs the feed given search terms.
        # This is left as an exercise to the reader. 

        # now we construct the url for the yahoo pipe created in our tutorial
        # (you will want to replace this with your own url), using the search 
        # terms provided by the user in the form
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=7c97fe1f432078bb6c3dbbf34d9671c0&_render=rss&textinput=" + terms )
        
        # this sets up feed as a list of dictionaries containing information 
        feed = [{"link": item.link, "title":item.title} for item in feed["items"]]

        # this sets up the context with the user's search terms and the search
        # results in feed
        context = {"feed": feed, "search": terms}

        # this sends the context and the file to render to jinja2
        self.render_response('index.html', **context)
        
        
         # This method should return the html to be displayed
    def get(self):
    	feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=7c97fe1f432078bb6c3dbbf34d9671c0&_render=rss&textinput=beethoven")
    	
    	feed = [{"link": item.link, "title":item.title} for item in feed["items"]]
        
                 # this will eventually contain information about the RSS feed
        context = {"feed" : feed, "search" : "beethoven"}

                  # here we call render_response instead of self.response.write.
        self.render_response('index.html', **context)

app = webapp2.WSGIApplication([('/.*', MainHandler)], debug=True)
