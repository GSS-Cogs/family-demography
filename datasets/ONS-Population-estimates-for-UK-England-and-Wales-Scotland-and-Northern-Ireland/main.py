import pandas as pd
from gssutils import *
from csvcubed.models.cube.qb.catalog import CatalogMetadata


df = pd.read_csv(
    "MYEB3_summary_components_of_change_series_UK_(2020_geog21).csv")

df.drop(
    (df.iloc[:, 3:]).columns[~(df.iloc[:, 3:]).columns.str.contains('population', case=False)], inplace=True, axis=1
)

df.rename(columns={'ladcode21': 'LA Code', 'laname21': 'Local Authority',
          'country': 'Country Code'}, inplace=True)

df = pd.melt(df, id_vars=['LA Code', 'Local Authority',
             'Country Code'], var_name='Year', value_name='Value')
df['Year'] = df['Year'].str.replace('population_', '').astype(int)


df.drop(columns=['Country Code'], inplace=True)

df.to_csv('observations.csv', index=False)
