import pandas as pd
import re
import json
import logging

tag_re = re.compile(r"^(?P<tag><.*>)?(?P<content>.*)?$")

# def double_check_csv():
#     dtypes = {
#         'data_element': str,
#         'tag': str,
#         'description': str,
#         'length': str,
#         'end_tag': str,
#         'characteristic': str,
#         'limits': str,
#         'format': str
#     }
#     tags = pd.read_csv("pds-tags-pd.csv", dtype = dtypes)
#     tags = tags.apply(lambda x: x.str.strip())
#     tags.to_csv("pds-tags-pd1.csv", index = False)

def format_tag_csv(fname):
    dtypes = {
        'data_element': str,
        'tag': str,
        'description': str,
        'length': str,
        'end_tag': str,
        'characteristic': str,
        'limits': str,
        'format': str
    }
    tags = pd.read_csv(fname, dtype = dtypes)
    tags = tags.apply(lambda x: x.str.strip())
    return tags[["tag", "end_tag"]]


    
def main():

    # later, use gzip file instead
    with open("src/pyncparser/test/data/9999999997-22-000253.nc", mode = "rt") as f:
        text = f.read()
    
    tags = format_tag_csv("pds-tags-pd.csv")

    # alright, now what
    # try to parse something. read lines, read bytes, etc.
    # what's my logic? 

    # stack.
    # need dictionary from those tags;
    # end_tag_dict = [{"<ISSUER>": "</ISSUER>", ... ]
    # tag must be beginning of line?
    # if tag isn't in end_tag_dict, stick rest of line into dict/json/object like "{tag}: {line}"
    # if tag is in end_tag_dict, need to parse until you see end tag, then put in "{tag}: 

    single_tags_set = set(tags[tags["end_tag"].isna()]["tag"])
    end_tags_df = tags[tags["end_tag"].notna()]
    end_tags_dict = dict(zip(end_tags_df.tag, end_tags_df.end_tag))
    # print(single_tags_set)
    # print(end_tags_dict)

    text = text.splitlines()
    # print(text)

    # alright, how tf this works
    tag_stack = []
    nc_doc = {}
    current_element = nc_doc
    parent_element = None
    for line in text:
        line_result = tag_re.search(line).groupdict()
        print(line_result)

        if line_result["tag"] in single_tags_set:
            print(f"{line_result['tag']} in single")
            current_element[line_result["tag"]] = line_result["content"]
        elif line_result["tag"] in end_tags_dict:
            print(f"{line_result['tag']} in end tag dict")
            # shouldn't be any content, really.
            if line_result["content"] != "":
                logging.warning(f"idk what's going on here: {line_result}, maybe corrupt")
                # also check if it doesn't match end tag
            # add line_result to current_element
            tag_stack.append((parent_element, end_tags_dict[line_result["tag"]])) # add end_tag to stack
            new_element = {}
            parent_element = current_element
            current_element[line_result["tag"]] = new_element 
            current_element = new_element
        elif line_result["tag"] == tag_stack[-1][1]:
            print("did we get here") # yes, apparently
            parent_element, _ = tag_stack.pop()
            # try to go up one element? need to go up another one?
            # this ends the current element, but if there's two or more end tags in a row, we need to keep going up
            # so keep a stack of parent references along with the other stack thing?
            current_element = parent_element
        else:
            print(f"curr: {current_element}, line: {line}")
            print(tag_stack)
            # this should match tag_stack[0]
            # so no tag, just push this to the next line? add it to...something?
            # alright, still no text, that's alright
            # no tag
            if not current_element:
                current_element = line
            else:
                current_element = current_element + line
            # and catch some errors here

    print(json.dumps(nc_doc, sort_keys = False, indent = 4))


if __name__ == "__main__":
    main()

