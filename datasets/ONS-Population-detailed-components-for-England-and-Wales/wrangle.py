from typing import Tuple
import pandas as pd
import click
from pathlib import Path
#%%
#%%

@click.command()
@click.argument("csv_files", type=click.Path(exists=True, dir_okay=False, path_type=Path), nargs=-1)
def wrangle(csv_files: Tuple[Path]) -> None:

    for csv_file in csv_files:

        # grab year from string to name the observation file later
        obs_prefix = csv_file.name.split("(")[1][:11]

        suffix_for_la_columns = obs_prefix[-2:]

        # [want to read the columns in with a defined datatype instead of 64]
        # error when building CSV-W cubed was "ValueError: cannot safely convert passed user dtype of int64 for float64 dtyped data in column 5"

        # # bring in first row of data so we can determine datatypes
        # df = pd.read_csv(csv_file, nrows=1)
        

        # #get column name and data type in a dictionary
        # column_dict = (df.dtypes.astype(str).to_dict()) # this will convert dtypes to string

        '''
        what the dtypes look like from first read
        {
        'ladcode20': 'object',
        'laname20': 'object',
        'country': 'object',
        'age': 'int64',
        'sex': 'int64',
        'population_2001': 'int64',
        'population_2002': 'int64',
        'population_2003': 'int64',
        ...
        'other_adjust_2020': 'int64'}
        }
        '''

        # #convert values to be csvcubed suitable
        # for k,v in column_dict.items():
        #     if v == "object":
        #         column_dict[k] = "string"
        #     elif v == "int64":
        #         column_dict[k] = "Int32"
        
        #
        df = pd.read_csv(csv_file,nrows=100)

        # [Transform]
        # unpivot period
        df = pd.wide_to_long(
            df=df.drop(["laname" + suffix_for_la_columns, "country"], axis=1),
            stubnames=[
                "population",
                "other_adjust",
                "unattrib",
                "special_change",
                "international_net",
                "international_out",
                "international_in",
                "internal_net",
                "internal_out",
                "internal_in",
                "deaths",
                "births",
            ],
            i=["ladcode" + suffix_for_la_columns, "age", "sex"],
            j="Period",
            sep="_",
        ).reset_index()

        # unpivot measure type
        df = pd.melt(
            df,
            id_vars=["ladcode" + suffix_for_la_columns, "age", "sex", "Period"],
            var_name="Measure Type",
            value_name="Value",
        )

        # Post Processing
        df.rename(
            columns={
                "ladcode" + suffix_for_la_columns: "Local Authority Code",
                "age": "Age",
                "sex": "Sex",
            },
            inplace=True,
        )

        #df.info() 

        '''
        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 24000 entries, 0 to 23999
        Data columns (total 6 columns):
        #   Column                Non-Null Count  Dtype  
        ---  ------                --------------  -----  
        0   Local Authority Code  24000 non-null  object 
        1   Age                   24000 non-null  int64  
        2   Sex                   24000 non-null  int64  
        3   Period                24000 non-null  int64  
        4   Measure Type          24000 non-null  object 
        5   Value                 22000 non-null  float64
        dtypes: float64(1), int64(3), object(2)
        memory usage: 1.1+ MB
        '''

        # handle NAs that were created because some columns don't go as far back as others
        df = df.dropna()

        # change Value datatype to int to match config file
        df = df.astype({
                'Value': "int"
                }
        )

        df = df.replace(
            {"Sex": {1: "Male", 2: "Female"}, "Country": {"E": "England", "W": "Wales"}}
        )
        
        df.to_csv(str(csv_file.parent.absolute()) + "/" + obs_prefix + "_" + "observations.csv", index=False)
#%%

if __name__ == "__main__":
    wrangle()

# %%
