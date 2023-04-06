"""Old AI cleaning code"""

#
# Clean the pathnames
#

if False:
    consecutive_err = 0
    while True:
        consecutive_err += 1
        try:
            run_path_cleaning()
            consecutive_err = 0
        except StopIteration:
            print("Done")
            break
        except Exception as e:
            print(e)

        if consecutive_err > 3:
            print("Too many errors")
            break

if False:
    # Turn the database into a dataset, so we can save it in the package, for caching in future builds.
    # This is not currently loaded yet.
    with shelve.open('census_paths') as db:
        paths_df = pd.DataFrame(db.values())

    paths_df.head()

if False:
    with shelve.open('open') as db:
        print(len(db))
        pdf = pd.DataFrame(db.values()).rename(
            columns={
                "unique_id": "table_id",
                "path": "filtered_path",
                "name": "path_name",
            }
        )

        mdf = add_rest_str(tdf, cdf)

        # mdf = mdf.merge(pdf, on=["table_id", "filtered_path"], how="left").copy()

        mdf["rest_description"] = mdf.apply(make_restricted_description, axis=1)

        mdf["col_desc"] = mdf.stripped_title + " for " + mdf.rest_description

        metadata_df = mdf.rename(columns={'uid': 'column_id'})

    metadata_df.head()