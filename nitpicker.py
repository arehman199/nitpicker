#!/usr/bin/python3
import urllib.request


def main():

    # Load the list of typos from the English Wikipedia
    webUrl = urllib.request.urlopen("\
https://en.wikipedia.org/w/index.php?title=Wikipedia:AutoWikiBrowser/\
Typos&action=raw")

    print("result code: ", str(webUrl.getcode()))
    print("charset: ", webUrl.headers.get_param("charset"))
    print()

    text = webUrl.read().decode('utf-8')
    print(text)

if __name__ == "__main__":
    main()

print("END")
