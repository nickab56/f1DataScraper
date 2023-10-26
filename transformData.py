import pandas as pd

# Initialize a mapping to store unique driver data
driver_mapping = {}
team_mapping = {}

# List of CSV files and their corresponding race types
csv_files = [
    ('formula1_results_race_2023.csv', 'Race'),
    ('formula1_results_qual_2023.csv', 'Qualifying'),
    ('formula1_results_practice1_2023.csv', 'Practice 1'),
    ('formula1_results_practice2_2023.csv', 'Practice 2'),
    ('formula1_results_practice3_2023.csv', 'Practice 3'),
    ('formula1_results_sprint_2023.csv', 'Sprint'),
    ('formula1_results_sprint_qual_2023.csv', 'Sprint Qualifying')
    # Add more CSV files with their respective race types here
]

# Create an empty list to store the individual DataFrames
dfs = []

# Iterate through each CSV file and process it
for file_name, race_type in csv_files:
    # Load data from the CSV file
    race_result_data = pd.read_csv(file_name)

    # Create a DataFrame from the loaded data
    df = pd.DataFrame(race_result_data)

    # Create a 'Race Type' column with the corresponding race type
    df['Race Type'] = race_type

    # Create a combined 'Driver' column with First Name, Last Name, and Racer Number
    df['Driver'] = df['First Name'] + ' ' + df['Last Name'] + ' (' + df['Racer Number'].astype(str) + ')'

    # Iterate through each row and update the driver_mapping
    for index, row in df.iterrows():
        driver_name = row['Driver']
        if driver_name not in driver_mapping:
            # If the driver is not in the mapping, add it with a unique ID
            driver_mapping[driver_name] = {
                'Driver ID': len(driver_mapping),
                'First Name': row['First Name'],
                'Last Name': row['Last Name'],
                'Racer Number': row['Racer Number'],
                'Team': row['Team']
            }

    # Iterate through each row and update the team_mapping
    for index, row in df.iterrows():
        team_name = row['Team']
        if team_name not in team_mapping:
            # If the team is not in the mapping, add it with a unique ID
            team_mapping[team_name] = {
                'Team ID': len(team_mapping),
                'Team Name': team_name
            }

    # Append the DataFrame to the list
    dfs.append(df)

# Concatenate all individual DataFrames into one big DataFrame
big_df = pd.concat(dfs, ignore_index=True)

# Create a Team DataFrame from the team_mapping
team_df = pd.DataFrame(list(team_mapping.values()))

# Create a Driver DataFrame from the driver_mapping
driver_df = pd.DataFrame(list(driver_mapping.values()))

# Map driver team names to Team IDs in the driver_df
driver_df['Team'] = driver_df['Team'].map(lambda team_name: team_mapping[team_name]['Team ID'])

# Save both DataFrames to CSV
# big_df.to_csv('formula1_combined_results_2023.csv', index=False)
driver_df.to_csv('formula1_driver_data_2023.csv', index=False)
# team_df.to_csv('formula1_team_data_2023.csv', index=False)


#######################################################

#%%
#national id creation

# import pandas as pd

# # List of nationalities in alphabetical order
# nationalities = [
#     'Australia', 'Canada', 'China', 'Denmark', 'Finland', 'France', 'Germany',
#     'Italy', 'Japan', 'Mexico', 'Monaco', 'New Zealand', 'Spain', 'Switzerland',
#     'Thailand', 'United Kingdom', 'United States'
# ]

# # Create a DataFrame to map nationalities to national IDs
# nationality_df = pd.DataFrame({'NationalID': range(1, len(nationalities) + 1), 'Nationality': nationalities})

# # Save the DataFrame to a CSV file
# nationality_df.to_csv('nationality_mapping.csv', index=False)

##########################################################################

#%%
# Event Id creation

# # event id creation
# import pandas as pd

# # Load data from the "practice1_2023.csv" file
# practice1_data = pd.read_csv('formula1_results_practice1_2023.csv')

# # Extract all unique race names from the "Race Name" column
# unique_race_names = practice1_data['Race Name'].unique()

# # Create a mapping of unique race names to unique event IDs
# event_to_id = {event: event_id for event_id, event in enumerate(unique_race_names, 1)}

# # Create an "events" DataFrame with "Event ID" and "Event Name" columns
# events_df = pd.DataFrame({'Event Name': unique_race_names})
# events_df['Event Name'] = events_df['Event Name'].str.replace('-', ' ').str.title()
# events_df['Event ID'] = range(1, len(events_df) + 1)

# # Save the "events" DataFrame to a CSV file
# events_df.to_csv('events.csv', index=False)

########################################################################

# # practice table creation.
# =============================================================================
# import pandas as pd
# 
# # Load driver data from the CSV file
# driver_data = pd.read_csv('formula1_driver_data_2023.csv')
# 
# # Create a mapping from driver names to driver IDs
# driver_name_to_id = {f"{row['First Name']} {row['Last Name']}": row['Driver ID'] for index, row in driver_data.iterrows()}
# 
# # Load data from the practice CSV files
# practice1_data = pd.read_csv('formula1_results_practice1_2023.csv')
# practice2_data = pd.read_csv('formula1_results_practice2_2023.csv')
# practice3_data = pd.read_csv('formula1_results_practice3_2023.csv')
# 
# # Extract all unique race names from the practice 1 data
# unique_race_names = practice1_data['Race Name'].unique()
# 
# # Create an "events" DataFrame to map event names to event IDs
# events_df = pd.DataFrame({'Event Name': unique_race_names})
# events_df['Event Name'] = events_df['Event Name'].str.replace('-', ' ').str.title()
# events_df['Event ID'] = range(1, len(events_df) + 1)
# 
# # Create a list to store practice DataFrames
# practice_dfs = []
# 
# # Define a list of practice data and their corresponding types
# practice_data = [practice1_data, practice2_data, practice3_data]
# 
# # Initialize a counter for Practice IDs
# practice_id_counter = 1
# 
# # Iterate through the practice data and types
# for idx, data in enumerate(practice_data, start=1):
#     
#     # Remove spaces and standardize the case in 'Race Name' column in the 'data' DataFrame
#     data['Race Name'] = data['Race Name'].str.replace('-', ' ').str.title()
#     
#     # Add a 'Practice Type' column with values 1, 2, or 3
#     data['Practice Type'] = idx
#     
#     # Create a "Driver" column to match driver names with driver IDs
#     data['Driver'] = data['First Name'] + ' ' + data['Last Name']
#     data['Driver ID'] = data['Driver'].map(driver_name_to_id)
# 
#     # Merge practice data with the "events" DataFrame to get the event IDs
#     practice_data = data.merge(events_df, left_on='Race Name', right_on='Event Name')
#     
#     # Create a unique "Practice ID" for each entry
#     practice_data['Practice ID'] = range(practice_id_counter, practice_id_counter + len(practice_data))
#     
#     # Update the Practice ID counter
#     practice_id_counter += len(practice_data)
#     
#     # Reorder the columns for the "Practice" DataFrame
#     practice_data = practice_data[['Practice ID', 'Practice Type', 'Driver ID', 'Event ID', 'Position', 'Time', 'Laps Completed']]
#     
#     # Append the practice DataFrame to the list
#     practice_dfs.append(practice_data)
# 
# # Concatenate all practice DataFrames into one big DataFrame
# practice_df = pd.concat(practice_dfs, ignore_index=True)
# 
# # Save the "Practice" DataFrame to a CSV file
# practice_df.to_csv('practice_data.csv', index=False)
# =============================================================================

######################################################################

#%%
# race data
""" import pandas as pd

# Load driver data from the CSV file
driver_data = pd.read_csv('formula1_driver_data_2023.csv')

# Create a mapping from driver names to driver IDs
driver_name_to_id = {f"{row['First Name']} {row['Last Name']}": row['Driver ID'] for index, row in driver_data.iterrows()}

# Load data from the race CSV files
race_data_1 = pd.read_csv('formula1_results_race_2023.csv')
race_data_2 = pd.read_csv('formula1_results_sprint_2023.csv')

# Extract all unique event names from the race data
unique_event_names_1 = race_data_1['Race Name'].unique()
unique_event_names_2 = race_data_2['Race Name'].unique()

# Create an "events" DataFrame to map event names to event IDs
events_df = pd.DataFrame({'Event Name': unique_event_names_1})
events_df['Event Name'] = events_df['Event Name'].str.replace('-', ' ').str.title()
events_df['Event ID'] = range(1, len(events_df) + 1)

# Create a list to store race DataFrames
race_dfs = []

# Define a list of race data and their corresponding types
race_data = [race_data_1, race_data_2]

# Initialize a counter for Race IDs
race_id_counter = 1

# Iterate through the race data and types
for idx, data in enumerate(race_data, start=1):
    
    # Remove spaces and standardize the case in 'Race Name' column in the 'data' DataFrame
    data['Race Name'] = data['Race Name'].str.replace('-', ' ').str.title()
    
    # Create a "Race Type" column with values 1 or 2
    data['Race Type'] = idx
    
    # Create a "Driver" column to match driver names with driver IDs
    data['Driver'] = data['First Name'] + ' ' + data['Last Name']
    data['Driver ID'] = data['Driver'].map(driver_name_to_id)

    # Merge race data with the "events" DataFrame to get the event IDs
    race_data = data.merge(events_df, left_on='Race Name', right_on='Event Name')
    
    # Create a unique "Race ID" for each entry (same as Practice ID)
    race_data['Race ID'] = range(race_id_counter, race_id_counter + len(race_data))
    
    # Update the Race ID counter
    race_id_counter += len(race_data)
    
    # Reorder the columns for the "Race" DataFrame
    race_data = race_data[['Race ID', 'Race Type', 'Driver ID', 'Event ID', 'Position', 'Time', 'Laps Completed', 'Points']]
    
    # Append the race DataFrame to the list
    race_dfs.append(race_data)

# Concatenate all race DataFrames into one big DataFrame
race_df = pd.concat(race_dfs, ignore_index=True)

# Save the "Race" DataFrame to a CSV file
race_df.to_csv('race_data.csv', index=False) """

##################################################################
# Qual Data
#%%
""" import pandas as pd

# Load driver data from the CSV file
driver_data = pd.read_csv('formula1_driver_data_2023.csv')

# Create a mapping from driver names to driver IDs
driver_name_to_id = {f"{row['First Name']} {row['Last Name']}": row['Driver ID'] for index, row in driver_data.iterrows()}

# Load data from the qualifying CSV files
qualifying_data_race = pd.read_csv('formula1_results_qual_2023.csv')
qualifying_data_sprint = pd.read_csv('formula1_results_sprint_qual_2023.csv')

# Extract all unique event names from the qualifying data
unique_event_names_race = qualifying_data_race['Race Name'].unique()
unique_event_names_sprint = qualifying_data_sprint['Race Name'].unique()

# Create an "events" DataFrame to map event names to event IDs
events_df = pd.DataFrame({'Event Name': unique_event_names_race})
events_df['Event Name'] = events_df['Event Name'].str.replace('-', ' ').str.title()
events_df['Event ID'] = range(1, len(events_df) + 1)

# Create a list to store qualifying DataFrames
qualifying_dfs = []

# Define a list of qualifying data and their corresponding types
qualifying_data = [qualifying_data_race, qualifying_data_sprint]

# Initialize a counter for Qualifying IDs
qualifying_id_counter = 1

# Iterate through the qualifying data and types
for idx, data in enumerate(qualifying_data, start=1):
    
    # Remove spaces and standardize the case in 'Race Name' column in the 'data' DataFrame
    data['Race Name'] = data['Race Name'].str.replace('-', ' ').str.title()
    
    # Create a "Qualifying Type" column with values 1 or 2
    data['Qualifying Type'] = idx
    
    # Create a "Driver" column to match driver names with driver IDs
    data['Driver'] = data['First Name'] + ' ' + data['Last Name']
    data['Driver ID'] = data['Driver'].map(driver_name_to_id)

    # Merge qualifying data with the "events" DataFrame to get the event IDs
    qualifying_data = data.merge(events_df, left_on='Race Name', right_on='Event Name')
    
    # Create a unique "Qualifying ID" for each entry
    qualifying_data['Qualifying ID'] = range(qualifying_id_counter, qualifying_id_counter + len(qualifying_data))
    
    # Update the Qualifying ID counter
    qualifying_id_counter += len(qualifying_data)
    
    # Reorder the columns for the "Qualifying" DataFrame
    qualifying_data = qualifying_data[['Qualifying ID', 'Qualifying Type', 'Driver ID', 'Event ID', 'Position', 'Laps Completed', 'Q1', 'Q2', 'Q3']]
    
    # Append the qualifying DataFrame to the list
    qualifying_dfs.append(qualifying_data)

# Concatenate all qualifying DataFrames into one big DataFrame
qualifying_df = pd.concat(qualifying_dfs, ignore_index=True)

# Save the "Qualifying" DataFrame to a CSV file
qualifying_df.to_csv('qualifying_data.csv', index=False) """

