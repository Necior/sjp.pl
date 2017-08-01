#!/usr/bin/env python3

import urllib.request
import sys
from bs4 import BeautifulSoup

version = 0.01


def print_usage_info():
    helpMsg = """Usage:
    sjp.py <word>
    sjp.py (-h | --help | /?)
    sjp.py (-v | --version)"""
    print(helpMsg)


def print_version_info():
    versionMsg = "sjp.py " + str(version)
    print(versionMsg)


def get_definition(word):
    url = 'http://sjp.pl/' + urllib.parse.quote(word)
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.URLError:
        print("[Error] Can't connect to the service")
        sys.exit(2)

    soup = BeautifulSoup(html)

    # checks if definition is in dictionary:
    if soup.find_all('span', style="color: #e00;"):
        print("[Error] \"" + word + "\" not found")
        sys.exit(1)

    # definition is in dictionary, continue:
    ex = soup.find_all('p',
                       style="margin-top: .5em; "
                             "font-size: medium; "
                             "max-width: 32em; ")
    ex = ex[0]
    return ex.contents[0::2]  # returns a list of lines of definition


def main():
    if len(sys.argv) <= 1:
        print_usage_info()
        sys.exit()
    if sys.argv[1] in ("-h", "--help", "/?"):
        print_usage_info()
        sys.exit()
    elif sys.argv[1] in ("-v", "--version"):
        print_version_info()
        sys.exit()
    else:
        print('\n'.join(get_definition(sys.argv[1])))


if __name__ == "__main__":
    main()
