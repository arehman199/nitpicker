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

    typoRegex = "\
<(?:Typo)?\\s+(?:word=\"(.*?)\"\\s+)?find=\"(.*?)\"\\s+replace=\"(.*?)\
\"\\s*/?>"

    rules = regex.findall(typoRegex, htmlText)

    excludeDirs = set([".git"])
    excludeFiles = ('.eps', '.gif', '.png', '.jpg', '.svg')

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

    typoCount = 0

    for file in filelist:
        print("Examining file {}".format(file))

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
            for index, line in enumerate(stext.splitlines()):
                for rule in rules:
                    rule_name = rule[0]
                    rule_regex = rule[1]
                    rule_subst = rule[2]
                    matchobj = regex.search(rule[1], line)
                    if matchobj:
                        typoCount = typoCount + 1

                        # construct fixed line
                        fixed = rule_subst
                        for i in range(1, rule_subst.count("$") + 1):
                            if(matchobj.group(i) != None):
                                fixed = fixed.replace("${}".format(i),
                                                      matchobj.group(i))
                            else:
                                fixed = fixed.replace("${}".format(i), "")

                        print("{}:{}".format(file, index + 1))
                        print("-", line, sep="")
                        print("+", line.replace(matchobj.group(), fixed),
                              sep="")
                        print("       Match:", matchobj.group())
                        print(" Replacement:", fixed)
                        print("        Rule:", rule_name)
                        print("       Regex:", rule_regex)
                        print("Substitution:", rule_subst)
                        print()

    print("typoCount = {}".format(typoCount))

if __name__ == "__main__":
    main(sys.argv[0:])
