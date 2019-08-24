# -*- coding: utf-8 -*-
###############################################################################
# Please Find a Job
###############################################################################
)))How can I do it? I was trying to enter some specified link (with urllib), but to do it, I need to log in.
I have this source from the site)))

<form id="login-form" action="auth/login" method="post">
    <div>
    <!--label for="rememberme">Remember me</label><input type="checkbox" class="remember" checked="checked" name="remember me" /-->
    <label for="email" id="email-label" class="no-js">Email</label>
    <input id="email-email" type="text" name="handle" value="" autocomplete="off" />
    <label for="combination" id="combo-label" class="no-js">Combination</label>
    <input id="password-clear" type="text" value="Combination" autocomplete="off" />
    <input id="password-password" type="password" name="password" value="" autocomplete="off" />
    <input id="sumbitLogin" class="signin" type="submit" value="Sign In" />

(((Maybe you want to use twill (it's based on mechanize). It's quite easy to use and should be able to do what you want.It will look like the following:)))

from twill.commands import *
go('http://mysite.org')

fv("1", "email-email", "blabla.com")
fv("1", "password-clear", "testpass")

submit('0')

(((Let me try to make it simple, suppose URL of the site is www.example.com and you need to sign up by filling username and password, so we go to the login page say http://www.example.com/login.php now and view it's source code and search for the action URL it will be in form tag something like

 <form name="loginform" method="post" action="userinfo.php">

now take userinfo.php to make absolute URL which will be 'http://example.com/userinfo.php', now run a simple python script

import requests
url = 'http://example.com/userinfo.php'
values = {'username': 'user',
          'password': 'pass'}

r = requests.post(url, data=values)
print r.content

---------------------------------------------------
))))#This URL will be the URL that your login form points to with the "action" tag.
POST-LOGIN-URL = 'https://my.freecycle.org/login'
#This URL is the page you actually want to pull down with requests.
REQUEST-URL = 'https://my.freecycle.org/home/posts')))))

payload = {
    ‘username’: ‘your_username’,
    'pass’: ‘your_password'
}


with requests.Session() as session:
    post = session.post(POST-LOGIN-URL, data=payload)
    r = session.get(REQUEST-URL)
    print(r.text)   #or whatever else you want to do with the request data!














