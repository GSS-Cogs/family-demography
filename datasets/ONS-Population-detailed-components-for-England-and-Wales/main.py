import pandas as pd
from gssutils import *
# from csvcubed.models.cube.qb.catalog import CatalogMetadata

# here's AF intro to the project https://onswebsite.slack.com/archives/CPC5ADPNC/p1659428231740559
# the ONS published dataset can be found here https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland
# AF wants to use the new qube-config.json method. it's documentation is here:  https://gss-cogs.github.io/csvcubed-docs/external/guides/configuration/qube-config/
# codelist for ladcode21 (e.g. E00000001) is currently on climate change repo https://github.com/GSS-Cogs/family-climate-change/tree/master/reference/codelists. It will probably me moved to general reference codelist in the future.
# download and transform the detailed version of the csv first, then append the suitable columns from the summary csv. Andrew will make a hiearchy later on. 

df = pd.read_csv(
    "MYEB2_detailed_components_of_change_series_EW_(2020_geog21).csv")


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
#     title="Population breakdown estimates for England and Wales",
#     description="Population breakdown estimates."
# )
# catalog_metadata.to_json_file('catalog-metadata.json')