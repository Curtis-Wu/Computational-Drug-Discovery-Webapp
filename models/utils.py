import pandas as pd
from chembl_webresource_client import new_client

def target_search(drug):
    target = new_client.target
    target_query = target.search('acetylcholinesterase')
    targets = pd.DataFrame.from_dict(target_query)
    return targets


if __name__ == '__main__':
    # df = target_search('acetylcholinesterase')
    # df.head()
    target1 = new_client.target
    target_query = target1.search('acetylcholinesterase')
    targets = pd.DataFrame.from_dict(target_query)
    targets