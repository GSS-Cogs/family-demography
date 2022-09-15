#%%
import pandas as pd
import sys
# from gssutils import *
# from csvcubed.models.cube.qb.catalog import CatalogMetadata

# here's AF intro to the project https://onswebsite.slack.com/archives/CPC5ADPNC/p1659428231740559
# the ONS published dataset can be found here https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland
# AF wants to use the new qube-config.json method. it's documentation is here:  https://gss-cogs.github.io/csvcubed-docs/external/guides/configuration/qube-config/
# codelist for ladcode21 (e.g. E00000001) is currently on climate change repo https://github.com/GSS-Cogs/family-climate-change/tree/master/reference/codelists. It will probably me moved to general reference codelist in the future.
# download and transform the detailed version of the csv first, then append the suitable columns from the summary csv. Andrew will make a hiearchy later on. 
# purpose is we want to see the boarder changed from geog20 to geog21. with lower layer super output area (LSOA) boundaries we're able to retreive the original data


# expected results:
# ladcode21,year,measure,value
# E06000001,2002,population,90152
# E0600s0001,2002,births,1017

# put all the files entered into command line in a list
def main():
    csv_files = list(sys.argv[1:])
    
    print()
    print("You are unpivoting these files:")
    for csv_file in csv_files:
        print("- " + csv_file)

    
    for csv_file in csv_files:
  
        #grab year from string to name the observation file later
        obs_prefix = csv_file.split("(")[1][:11]

        suffix_for_la_columns = obs_prefix[-2:]

        print()
        print("Currently transforming file: " + csv_file)

  
        df = pd.read_csv(csv_file)
        # unpivot period
        df = pd.wide_to_long(df = df.drop(['laname' + suffix_for_la_columns,'country'],axis=1), 
                        stubnames=['population','other_adjust','unattrib','special_change','international_net',
                        'international_out','international_in','internal_net','internal_out','internal_in',
                        'deaths','births'
                        ], 
                        i=['ladcode' + suffix_for_la_columns, 'age', 'sex'], 
                        j='Period',
                        sep='_').reset_index()

        # unpivot measure type
        df = pd.melt(df, id_vars=['ladcode' + suffix_for_la_columns, 'age', 'sex', 'Period'], 
                    var_name='Measure Type', 
                    value_name='Value')

        # Post Processing
        df.rename(columns={'ladcode' + suffix_for_la_columns: 'Local Authority Code', 'age': 'Age', 'sex': 'Sex'}, inplace=True)
        df = df.replace(
            {
                'Sex': {1: 'Male', 2: 'Female'},
                'Country': {'E': 'England', 'W': 'Wales'}
            }
        )
        df.to_csv(obs_prefix + '_' + 'observations.csv', index=False)
        print("Finished. See output file: " + obs_prefix + "_observations.csv")


# #______________________________________________________________________________________________________
# # did this first so keeping a back up for now

# ## here's the version where i did it in a function
# def unpivot_geog_data(csv_files: List(str)):
#     for csv_file in csv_files:

#         #grab year from string to name the observation file later
#         obs_prefix = csv_file.split("(")[1][:11]
        
#         df = pd.read_csv(csv_file)

#         # unpivot period
#         df = pd.wide_to_long(df = df.drop(['laname21','country'],axis=1), 
#                         stubnames=['population','other_adjust','unattrib','special_change','international_net',
#                         'international_out','international_in','internal_net','internal_out','internal_in',
#                         'deaths','births'
#                         ], 
#                         i=['ladcode21', 'age', 'sex'], 
#                         j='Period',
#                         sep='_').reset_index()

#         #%%
#         # unpivot measure type
#         df = pd.melt(df, id_vars=['ladcode21', 'age', 'sex', 'Period'], 
#                     var_name='Measure Type', 
#                     value_name='Value')

#         #%%
#         # Post Processing

#         df.rename(columns={'ladcode21': 'Local Authority Code', 'age': 'Age', 'sex': 'Sex'}, inplace=True)

#         df = df.replace(
#             {
#                 'Sex': {1: 'Male', 2: 'Female'},
#                 'Country': {'E': 'England', 'W': 'Wales'}
#             }
#         )
#         print(df.head())

#         df.to_csv(obs_prefix + '_' + 'observations.csv', index=False)


# # df = pd.read_csv(
# #     "MYEB2_detailed_components_of_change_series_EW_(2020_geog21).csv")
# # #%%
# # # unpivot period
# # df = pd.wide_to_long(df = df.drop(['laname21','country'],axis=1), 
# #                 stubnames=['population','other_adjust','unattrib','special_change','international_n
# #                 'international_out','international_in','internal_net','internal_out','internal_in',
# #                 'deaths','births'
# #                 ], 
# #                 i=['ladcode21', 'age', 'sex'], 
# #                 j='Period',
# #                 sep='_').reset_index()
# # #%%
# # # unpivot measure type
# # df = pd.melt(df, id_vars=['ladcode21', 'age', 'sex', 'Period'], 
# #             var_name='Measure Type', 
# #             value_name='Value')
# # #%%
# # # Post Processing
# # df.rename(columns={'ladcode21': 'Local Authority Code', 'age': 'Age', 'sex': 'Sex'}, inplace=True)
# # df = df.replace(
# #     {
# #         'Sex': {1: 'Male', 2: 'Female'},
# #         'Country': {'E': 'England', 'W': 'Wales'}
# #     }

# # #%%
# # # TODO continue from here. check data type of each column first

# # # df['Sex'] = df['Sex'].astype(int).astype(str)

# # # df = df.drop_duplicates()


# # df.to_csv('2021_observations.csv', index=False)
# # # catalog_metadata = CatalogMetadata(
# # #     title="Population breakdown estimates for England and Wales",
# # #     description="Population breakdown estimates."
# # # )
# # # catalog_metadata.to_json_file('catalog-metadata.json')
# # # %%

if __name__ == "__main__":
    main()