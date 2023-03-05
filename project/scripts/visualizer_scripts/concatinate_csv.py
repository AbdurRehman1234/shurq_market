import glob
import pandas as pd
import os
from time import sleep

def csv_concate(path_csv):
    # list all csv files only
    csv_files = glob.glob(os.path.join(path_csv, '*.{}'.format('csv')))
    
    print("---------------------------------------")
    print("Concatinating the files to on dataframe\nand inserting Brand and Country Columns from file name...")
    print("---------------------------------------")

    df_list = []
    for file in csv_files:
        # getting the brand, asin and country names from the file name
        file_name = file.split("inputs_visualizer")[-1].replace("\\",
                                                "").replace("/", "").replace(
                                                    ".csv", "")
        (brand, asin,
         country) = (file_name.split("_")[0].strip(), file_name.split("_")[1].strip(),
                     file_name.split("_")[-1].strip())

        # reading csv
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            print(f"{file_name} is empty or can't be read.")
            continue

        # making new columns like brand, asin, country in dataframe and assigning the names from the file name
        df[["Brand", "ASIN", "Country"]] = [brand, asin, country]

        # appending modified dataframe to the list
        df_list.append(df)

    # concatincating all the dfs to one df
    df_concat = pd.concat([df for df in df_list], axis=0, ignore_index=True)
    # deleting files after concatenation
    print("Deleting the files")
    sleep(5)
    for file in csv_files:
        os.remove(file)
    return df_concat
