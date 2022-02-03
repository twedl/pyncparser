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
    last_valid_tag = None

    # wow this is pretty ugly
    for line in text:
        line_result = tag_re.search(line).groupdict()

        current_tag = line_result["tag"]

        if current_tag is not None:
            last_valid_tag = current_tag

        if current_tag in single_tags_set:
            current_element[current_tag] = line_result["content"]
        elif current_tag in end_tags_dict:
            tag_stack.append((parent_element, end_tags_dict[current_tag])) # add end_tag to stack
            new_element = {}
            parent_element = current_element
            current_element[current_tag] = new_element 
            current_element = new_element
        elif current_tag == tag_stack[-1][1]:
            parent_element, _ = tag_stack.pop()
            current_element = parent_element
        elif current_tag is None:
            if not current_element:
                current_element = [line]
                parent_element[last_valid_tag] = current_element # changing reference to current element here. need reference to current element instead
            else:
                current_element.append(line)

    print(json.dumps(nc_doc, sort_keys = False, indent = 4))


if __name__ == "__main__":
    main()

