from typing import Tuple
import pandas as pd
import click
from pathlib import Path


@click.command()
@click.argument("csv_files", type=click.Path(exists=True, dir_okay=False, path_type=Path), nargs=-1)
def wrangle(csv_files: Tuple[Path]) -> None:

    for csv_file in csv_files:

        # grab year from string to name the observation file later
        obs_prefix = csv_file.name.split("(")[1][:11]

        suffix_for_la_columns = obs_prefix[-2:]

        df = pd.read_csv(csv_file)

        # seems to be a typo in the column header as 2020 has lacode20 and 2021 has ladcode21 (note the extra d)
        if suffix_for_la_columns == "20":
            la_code_column_name = "lacode"
        elif suffix_for_la_columns == "21":
            la_code_column_name = "ladcode"
        # unpivot period
        df = pd.wide_to_long(
            df=df.drop(["laname" + suffix_for_la_columns, "country"], axis=1),
            stubnames=[
                "population",
                #"other_adjust",
                #"unattrib",
                #"special_change",
                "natchange",
                "other_change",
                "international_net",
                "international_out",
                "international_in",
                "internal_net",
                "internal_out",
                "internal_in",
                "deaths",
                "births",
            ],
            i=[la_code_column_name + suffix_for_la_columns], # was ladcode. is it a typo? TODO 
             #"age",
             #"sex"],
            j="Period",
            sep="_",
        ).reset_index()

        # unpivot measure type
        df = pd.melt(
            df,
            id_vars=[la_code_column_name + suffix_for_la_columns, "Period"],
            var_name="Measure Type",
            value_name="Value",
        )

        # Post Processing
        df.rename(
            columns={
                la_code_column_name + suffix_for_la_columns: "Local Authority Code"
            },
            inplace=True,
        )

        # handle NAs that were created because there were blank values
        df = df.dropna()

        # change Value datatype to int to match config file
        df = df.astype({
                'Value': "int"
                }
        )

        # remove rows with 0s in Value column, that were created due to the previous transformation steps treating all columns as if they have the same number of years
        df = df[df["Value"] != 0]


        df = df.replace(
            {"Country": {"E": "England", "W": "Wales"}}
        )
        df.to_csv(str(csv_file.parent.absolute()) + "/" + obs_prefix + "_" + "observations.csv", index=False)
#%%

if __name__ == "__main__":
    wrangle()

# %%
