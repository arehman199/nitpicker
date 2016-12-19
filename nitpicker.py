#!/usr/bin/python3
import urllib.request
import regex
import sys


def main(argv):

    # Load the list of typos from the English Wikipedia
    webUrl = urllib.request.urlopen("\
https://en.wikipedia.org/w/index.php?title=Wikipedia:AutoWikiBrowser/\
Typos&action=raw")

    print("result code: ", str(webUrl.getcode()))
    print("charset: ", webUrl.headers.get_param("charset"))
    print()

    htmlText = webUrl.read().decode('utf-8')
    # print(text)

    typoRegex = regex.compile("\
<(?:Typo)?\\s+(?:word=\"(.*?)\"\\s+)?find=\"(.*?)\"\\s+replace=\"(.*?)\
\"\\s*/?>")

    rules = regex.findall(typoRegex, htmlText)

    fh = open(argv[1], 'r')
    stext = fh.read()
    fh.close()

    for rule in rules:
        ruleRegex = regex.compile(rule[1])
        for index, line in enumerate(stext.splitlines()):
            if regex.search(ruleRegex, line):
                print("{}:{}:".format(argv[1], index + 1))
                print("line =", line)
                print("Rule Name = ", rule[0])
                print("Rule Regex = ", rule[1])
                print("Rule Substitution = ", rule[2])
                print()

if __name__ == "__main__":
    main(sys.argv[0:])

print("END")
