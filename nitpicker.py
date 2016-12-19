#!/usr/bin/python3
import urllib.request
import regex
import sys
import os


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

    filelist = list()
    if os.path.exists(argv[1]):
        if os.path.isfile(argv[1]):
            if not os.path.islink(argv[1]):
                filelist.append(argv[1])
        elif os.path.isdir(argv[1]):
            for root, subs, files in os.walk(argv[1], topdown=True):
                for file in files:
                    filelist.append(os.path.join(root, file))
    filelist.sort()

    print("Following files will be searched for typos:")
    for file in filelist:
        print(file)
    print()

    for file in filelist:
        print("Examining file{}".format(file))
        fh = open(file, 'r')
        stext = fh.read()
        fh.close()

        for rule in rules:
            ruleRegex = regex.compile(rule[1])
            for index, line in enumerate(stext.splitlines()):
                if regex.search(ruleRegex, line):
                    print("{}:{}:".format(file, index + 1))
                    print("Text:", line)
                    print("Rule Name =", rule[0])
                    print("Rule Regex =", rule[1])
                    print("Rule Substitution =", rule[2])
                    print()

if __name__ == "__main__":
    main(sys.argv[0:])

print("END")
