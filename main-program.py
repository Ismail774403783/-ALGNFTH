
###############################################################################
# Hello World (http://pythonfiddle.com/pig-latin-translator-for-python/)
###############################################################################

print "Login Script"

import getpass

CorrectUsername = "Test"
CorrectPassword = "TestPW" 

loop = 'true'
while (loop == 'true'):

    username = raw_input("Please enter your username: ")

    if (username == CorrectUsername):
        loop1 = 'true'
        while (loop1 == 'true'):
            password = getpass.getpass("Please enter your password: ")
            if (password == CorrectPassword):
                print "Logged in successfully as " + username
                loop = 'false'
                loop1 = 'false'
            else:
                print "Password incorrect!"

    else:
        print "Username incorrect!"



with open('Usernames.txt', 'r') as f:
    data = f.readlines()
    #print data

for line in data:
    words = line.split() 
----------------------------------------------------------------
CorrectUsername = "ChrisHay"
CorrectPassword = "ChrisHayPassword"

loop = 'true'
while (loop == 'true'):
    username = raw_input("Please enter your username: ")
    if (username == CorrectUsername):
    	password = raw_input("Please enter your password: ")
        if (password == CorrectPassword):
            print "Logged in successfully as " + username
            loop = 'false'
        else:
            print "Password incorrect!"
    else:
        print "Username incorrect!"




















