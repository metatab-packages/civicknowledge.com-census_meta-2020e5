
from tqdm.auto import tqdm
from pathlib import Path
import json
import os
import pandas as pd


# Link the metadata columns to specific topics
factor_cols = {
    'age': 'people/age',
    'sex': 'people/sex',
    'race': 'people/race',
    'poverty_status': 'people/ses/gross_income/poverty',
    'has_income': 'people/ses/gross_income',
    'employed': 'people/employment',
    'ft_employed': 'people/employment',
    'marital_status': 'people/family/marriage',
    'family': 'people/family',
    'household': 'people/living_arrangement/households',
    'grand_pc': 'people/family/children',
    'opposite_sex': 'people/sexuality',
    'group_quarters': 'people/living_arrangement/group quarters',
    'housing': 'housing',
    'tenure': 'housing/tenure',
    'citizen': 'people/citizenship_status',
    'foreign_born': 'people/nativity',
    'military': 'people/military_status',
}

# create a path name in the cache directory for saving a JSON file. THe function takes an id number to use
# in the file name.
def cache_path(topics_dir, id):
    from slugify import slugify

    if not topics_dir.exists():
        topics_dir.mkdir(parents=True)

    if isinstance(id, str):
        id = slugify(id)

    return topics_dir.joinpath(f'{id}.json')

def check_topics(tc):
    # Check that all of the topics actually exist
    for k,v in factor_cols.items():
        tc.topics[v]

def compile_topics(topics_dir, df):

    rows = []
    for idx, r in tqdm(list(df.iterrows())):

        if r.bare_title not in ('Or',):

            fn = cache_path(topics_dir, r.bare_title)

            if fn.exists():
                with fn.open() as f:
                    d = json.load(f)
                    topics = d['topics']
            else:
                topics = []

            for k,v in factor_cols.items():
                if r[k] != 'all':
                    topics.append(v)


            for t in topics:
                rows.append({
                    'column_id': r['column_id'],
                    'topic': t
                })


    topics_df = pd.DataFrame(rows)

    return topics_df




def find_topics(topics_dir,tc, df):
    """Determine what topics apply to the questions.  """
    import json

    for idx, r in tqdm(list(df.iterrows())):

        if r.bare_title in ('Or',):
            continue

        fn = cache_path(topics_dir, r.bare_title)

        if fn.exists():
            continue

        d = r.to_dict()

        try:
            t = tc.search_refine(r.bare_title)
        except AttributeError: # maybe a float or a nan
            continue
        except Exception as e:
            print(e, f" title='{r.bare_title}' ")
            continue

        d['topics'] = t.path.to_list()

        with fn.open('w') as f:
            json.dump(d, f)