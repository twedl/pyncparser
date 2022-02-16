import pandas as pd
import re
import json
import logging

tag_re = re.compile(r"^(?P<tag><.*>)?(?P<content>.*)?$")

def get_tags(fname):
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
    return tags[["tag", "end_tag"]]

def parse(fname):
    # parse text or parse filename?
    with open(fname, mode = "rt") as f:
        text = f.read()
    tags = get_tags("pds-tags-pd.csv")

    single_tags_set = set(tags[tags["end_tag"].isna()]["tag"])
    end_tags_df = tags[tags["end_tag"].notna()]
    end_tags_dict = dict(zip(end_tags_df.tag, end_tags_df.end_tag))

    text = text.splitlines()

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

        # if current_tag in current_element already?
        # need to swap from current_element[current_tag] = "old content"
        # to current_element[current] = ["old content", "new content"]

        if current_tag in current_element: 

            # change from:
            # submission: {document: {...doc1...}}
            # to:
            # submission: {document: [{...doc1...}, {...doc2...}]} 
            current_element[current_tag] = [current_element[current_tag]]
            current_element = current_element[current_tag]

            if current_tag in single_tags_set:
                current_element.append(line_result["content"])
            elif current_tag in end_tags_dict:
                # what's the parent element here? same stuff, but...adding to a list.
                tag_stack.append((parent_element, end_tags_dict[current_tag])) # add end_tag to stack
                new_element = {}
                # parent_element = current_element
                current_element.append(new_element)
                # current_element[current_tag] = new_element 
                current_element = new_element
            elif current_tag == tag_stack[-1][1]: # still doing this? yes.
                # but need to pop two back? no.
                parent_element, _ = tag_stack.pop()
                current_element = parent_element
            elif current_tag is None:
                if not current_element:
                    current_element = [line]
                    parent_element[last_valid_tag] = current_element # changing reference to current element here. need reference to current element instead
                else:
                    current_element.append(line)

        else:
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

    # before writing, add filename = "999...253.nc" to object at top-level
    print(json.dumps(nc_doc, sort_keys = False, indent = 4))

    
def main():

    # later, use gzip file instead
    # with open("src/pyncparser/test/data/9999999997-22-000253.nc", mode = "rt") as f:
    #     text = f.read()
    fname = "src/pyncparser/test/data/test-multiple-documents.nc"
    

    parse(fname)

if __name__ == "__main__":
    main()

