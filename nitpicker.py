#!/usr/bin/python3
import urllib.request
import regex


def main():

    # Load the list of typos from the English Wikipedia
    webUrl = urllib.request.urlopen("\
https://en.wikipedia.org/w/index.php?title=Wikipedia:AutoWikiBrowser/\
Typos&action=raw")

    print("result code: ", str(webUrl.getcode()))
    print("charset: ", webUrl.headers.get_param("charset"))
    print()

    text = webUrl.read().decode('utf-8')
    # print(text)

    typoRegex = regex.compile("\
<(?:Typo)?\\s+(?:word=\"(.*?)\"\\s+)?find=\"(.*?)\"\\s+replace=\"(.*?)\
\"\\s*/?>")

    rules = regex.findall(typoRegex, text)
    for rule in rules:
        print("Rule Name = ", rule[0])
        print("Rule Regex = ", rule[1])
        print("Rule Substitution = ", rule[2])
        print()

if __name__ == "__main__":
    main()

print("END")
