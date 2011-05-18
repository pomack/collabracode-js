#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch


class MainHandler(webapp.RequestHandler):
    def process(self):
        self.response.set_status(200)
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Max-Age'] = '60'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET,POST,HEAD,LIST,DELETE,PUT'
        self.response.out.write('Go to rss.json to retrieve http://scripting.com/rss.json accessible from any browser using XHR')
    
    def get(self):
        self.process()
    
    def head(self):
        self.process()
    
    def post(self):
        self.process()
    



class MendeleyProxyHandler(webapp.RequestHandler):
    def process(self):
        headers = dict([o for o in self.request.headers.items()])
        for k in ['Content-Length', 'Host', 'Cookie']:
            if k in headers:
                del headers[k]
        headers['Connection'] = 'Close'
        method = self.request.method
        payload = req.body if method in ('POST', 'PUT') else None
        url = u'http://api.mendeley.com/' + self.request.path_qs.split('/',2)[-1]
        result = urlfetch.fetch(url=url, payload=payload, method=method, headers=headers, deadline=10, validate_certificate=False)
        self.response.set_status(result.status_code)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Max-Age'] = '60'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET,POST,HEAD,LIST,DELETE,PUT'
        for o in result.headers.items():
            o = ('-'.join([h.lower().capitalize() for h in o[0].split('-')]), o[1])
            if o[0] in ('Set-Cookie', 'Date'):
                continue
            self.response.headers[o[0]] = o[1]
        self.response.out.write(result.content)
    
    def get(self):
        self.process()
    
    def head(self):
        self.process()
    
    def put(self):
        self.process()
    
    def list(self):
        self.process()
    
    def delete(self):
        self.process()
    
    def post(self):
        self.process()
    

        

class RssJsonHandler(webapp.RequestHandler):
    def process(self):
        result = urlfetch.fetch("http://scripting.com/rss.json")
        self.response.set_status(result.status_code)
        self.response.content_type = 'application/json; charset=utf-8'
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Max-Age'] = '60'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET'
        self.response.out.write(result.content)
    
    def get(self):
        self.process()
    
    def head(self):
        self.process()


def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/rss.json', RssJsonHandler),
        (r'/mendeley_proxy/.+', MendeleyProxyHandler),
      ],
      debug=True
    )
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
