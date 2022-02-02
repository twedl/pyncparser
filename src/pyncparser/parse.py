import pandas as pd

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
    return tags[["tag", "end_tag"]]

    
def main():

    with open("src/pyncparser/test/data/9999999997-22-000253.nc", mode = "rt") as f:
        text = f.read()
    
    tags = format_tag_csv("pds-tags-pd.csv")

    # now go through that thing and check them all


if __name__ == "__main__":
    main()

