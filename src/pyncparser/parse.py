# function that parses a thing
# not anywhere near a real package yet
# still work just on a script

# open tags v. start-end tags
# start-end tags, easy
# open tags, easy as long as you know what they are.
# print the manual and check. cross-check with rust parser

# manual: lists all tags, differentiates between tags and end-tags
# submission header tag elements, document header tag elements, 
# document header and text tags
# lists information and format for each tag
# in that information, has "END TAG", either the end tag or "NA"
# so that's something, just need machine readable format for this thing

# none of these worked. either patch up the sgml=>xml on the fly, or write my
# own parser? which one's easier? which one's faster?

# from lxml import etree
import os
import pandas as pd
# from io import StringIO, BytesIO
# ugh idk what happening

def main():

    # parser = etree.XMLParser(load_dtd = True)
    # parser.resolvers.add(DTDResolver())

    with open("src/pyncparser/test/data/9999999997-22-000253.nc", mode = "rt") as f:
    # with open("test/data/9999999997-22-000253.nc", mode = "rt") as f:
        text = f.read()
    
    cc = pd.read_csv("pds-tags.csv")
    print(cc.head())
    print(cc.transpose())
    
    # with open("copy-edgar-pds.dtd", mode = "rt") as g:
    # # with open("test/data/9999999997-22-000253.nc", mode = "rt") as f:
    #     dtd = g.read()

    # text = '<!DOCTYPE note SYSTEM "edgar-pds.dtd">\n' + text
    # text = dtd + text

    # print(text[:100])
    # tree = etree.parse("src/pyncparser/pds.txt", parser)
    # tree = etree.parse(StringIO(text), parser)
    # tree = etree.parse(StringIO(text), parser)
    # print(tree)

    # j = parse(text)
    # print(j)

    # strategies: try to read it myself, or just try to smash the DTD into lxml?

if __name__ == "__main__":
    main()

