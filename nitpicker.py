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

    excludeDirs = set([".git"])
    excludeFiles = ('.eps', '.gif', '.png', '.jpg')

    filelist = list()
    if os.path.exists(argv[1]):
        if os.path.isfile(argv[1]):
            if not os.path.islink(argv[1]):
                filelist.append(argv[1])
        elif os.path.isdir(argv[1]):
            for root, dirs, files in os.walk(argv[1], topdown=True):
                dirs[:] = [d for d in dirs if d not in excludeDirs]
                for file in files:
                    if not file.endswith(excludeFiles):
                        filelist.append(os.path.join(root, file))
    filelist.sort()

    print("Following files will be searched for typos:")
    for file in filelist:
        print(file)
    print()

    for file in filelist:
        print("Examining file{}".format(file))

        fh = open(file, 'r')
        try:
            stext = fh.read()
        except UnicodeDecodeError as e:
            print("Read error: {}".format(e))
            print()
            fh.close()
            continue
        else:
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
