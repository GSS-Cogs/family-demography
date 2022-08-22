import pandas as pd
from gssutils import *
# from csvcubed.models.cube.qb.catalog import CatalogMetadata

df = pd.read_csv(
    "MYEB2_detailed_components_of_change_series_EW_(2020_geog21).csv")
df.drop(
    (df.iloc[:, 5:]).columns[~(df.iloc[:, 5:]).columns.str.contains('population', case=False)], inplace=True, axis=1
)

df.rename(columns={'ladcode21': 'Local Authority Code', 'laname21': 'Local Authority',
          'country': 'Country', 'age': 'Age', 'sex': 'Sex'}, inplace=True)
df['Sex'] = df['Sex'].astype(int).astype(str)

df = df.replace(
    {
        'Sex': {'1': 'Male', '2': 'Female'},
        'Country': {'E': 'England', 'W': 'Wales'}
    }
)

df = pd.melt(df, id_vars=['Local Authority Code', 'Local Authority',
             'Country', 'Age', 'Sex'], 
             var_name='Year', 
             value_name='Count')
df['Year'] = df['Year'].str.replace('population_', '').astype(int)
df = df.drop_duplicates()

df.to_csv('observations.csv', index=False)
# catalog_metadata = CatalogMetadata(
#     title="Population breakdown estimates for UK, England and Wales, Scotland and Northern Ireland",
#     description="Population breakdown estimates."
# )
# catalog_metadata.to_json_file('catalog-metadata.json')