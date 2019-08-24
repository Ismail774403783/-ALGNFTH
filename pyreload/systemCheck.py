from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
import subprocess
import sys

#from module import InitHomeDir

#very ugly prints, but at least it works with python 3

def main():
    print("#####   System Information   #####\n")
    print(("Platform:", sys.platform))
    print(("Operating System:", os.name))
    print(("Python:", sys.version.replace("\n", "")+ "\n"))

    try:
        import pycurl
        print(("pycurl:", pycurl.version))
    except:
        print(("pycurl:", "missing"))

    try:
        import Cryptodome
        print(("py-cryptodome:", Cryptodome.__version__))
    except:
        print(("py-cryptodome:", "missing"))

    try:
        import OpenSSL
        print(("OpenSSL:", OpenSSL.version.__version__))
    except:
        print(("OpenSSL:", "missing"))

    try:
        from PIL import Image
        print(("image library:", Image.VERSION))
    except:
        try:
            import Image
            print(("image library:", Image.VERSION))
        except:
            print(("image library:", "missing"))

    from module.common import JsEngine
    js = "available" if JsEngine.ENGINE else "missing"
    print(("JS engine", js))

    print("\n\n#####   System Status   #####")
    print("\n##  pyLoadCore  ##")

    core_err = []
    core_info = []

    if sys.version_info < (2, 7):
        core_err.append("Your Python version is too old. Please use at least Python 2.7")

    try:
        import pycurl
    except:
        core_err.append("Please install py-curl to use pyLoad.")

    try:
        from pycurl import AUTOREFERER
    except:
        core_err.append("Your py-curl version is to old, please upgrade!")

    try:
        from PIL import Image
    except:
        try:
            import Image
        except:
            core_err.append("Please install py-imaging/pil/pillow to use Hoster, which uses captchas.")

    pipe = subprocess.PIPE
    try:
        p = subprocess.call(["tesseract"], stdout=pipe, stderr=pipe)
    except:
        core_err.append("Please install tesseract to use Hoster, which uses captchas.")

    try:
        import OpenSSL
    except:
        core_info.append("Install OpenSSL if you want to create a secure connection to the core.")

    if not js:
        print("no JavaScript engine found")
        print("You will need this for some Click'N'Load links. Install Spidermonkey, ossp-js, pyv8 or rhino")

    if core_err:
        print("The system check has detected some errors:\n")
        for err in core_err:
            print(err)
    else:
        print("No Problems detected, pyLoadCore should work fine.")

    if core_info:
        print("\nPossible improvements for pyload:\n")
        for line in core_info:
            print(line)

    print("\n##  Webinterface  ##")

    web_err = []
    web_info = []

    try:
        import flup
    except:
        web_info.append("Install Flup to use FastCGI or optional webservers.")

    if web_err:
        print("The system check has detected some errors:\n")
        for err in web_err:
            print(err)
    else:
        print("No Problems detected, Webinterface should work fine.")

    if web_info:
        print("\nPossible improvements for webinterface:\n")
        for line in web_info:
            print(line)

if __name__ == "__main__":
    main()
