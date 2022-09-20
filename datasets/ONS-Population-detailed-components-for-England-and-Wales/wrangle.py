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
        df = df.replace(
            {"Sex": {1: "Male", 2: "Female"}, "Country": {"E": "England", "W": "Wales"}}
        )
        df.to_csv(obs_prefix + "_" + "observations.csv", index=False)


if __name__ == "__main__":
    wrangle()
