import sys, os, cgi, urllib, re, logging

from flask import redirect, request

form = cgi.FieldStorage()

class CASClient(object):

   def __init__(self, url='https://fed.princeton.edu/cas/'):
      self.cas_url = url

   def Authenticate(self):
      # If the request contains a login ticket, try to validate it
      if request.args.has_key('ticket'):
         netid = self.Validate(request.args['ticket'])
         if netid != None:
            return netid
     # No valid ticket; redirect the browser to the login page to get one
      login_url = self.cas_url + 'login' \
         + '?service=' + urllib.quote(self.ServiceURL())
      return redirect(login_url)

   def Validate(self, ticket):
      val_url = self.cas_url + "validate" + \
         '?service=' + urllib.quote(self.ServiceURL()) + \
         '&ticket=' + urllib.quote(ticket)
      #val_url = self.cas_url + "serviceValidate" + \
      #   '?service=' + urllib.quote(self.ServiceURL()) + \
      #   '&ticket=' + urllib.quote(ticket)  # new
      r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      if len(r) == 2 and re.match("yes", r[0]) != None:
         return r[1].strip()
      return None

   def ServiceURL(self):
      return request.base_url

# https://fed.princeton.edu/cas/
#  validate?ticket=ST-3555-McPZ4NKfx6S0EhnCEkHc
#  &service=https://www.applyweb.com/proto/auth/cas/princeton

def main():
  print "CASClient does not run standalone"

if __name__ == '__main__':
  main()
