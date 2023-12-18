import pandas as pd
from config import Q1_VAL,Q2_VAL,DEMS_CODE,REPS_CODE,COLUMNS

# removes all columns not needed
def df_strip(df): 
    df = df[COLUMNS]
    return df

# dictionary of all groups dfs
def df_groups_make(df):
    df_groups = {'All': df,
                 'House': df[df['chamber'] == 'House'],
                 'Senate': df[df['chamber'] == 'Senate'],
                 'Dems': df[df['party_code'] == DEMS_CODE], # 100 is dems
                 'Reps': df[df['party_code'] == REPS_CODE], # 200 is reps
                 }
    return df_groups

# df of mean ages of all groups
def df_age_make(df_groups):
    # mean age of each group for each congress
    df_age_dict = {k: v.groupby(['year', 'congress'])['age_years'].mean().reset_index() for k, v in df_groups.items()}

    # Combine into a single DataFrame for plotting
    df_age = pd.concat(
        [df.assign(group=key) for key, df in df_age_dict.items()],
        ignore_index=True
    )
    return df_age, df_age_dict

# counts of lengths of service
def df_count_dict_make(df_groups):
    df_count_dict = {k: v['bioguide_id'].value_counts().reset_index() for k, v in df_groups.items()}
    return df_count_dict

# calculate interquartile range for each congress
# function to calculate IQR
def calculate_iqr(group):
    q1 = group['age_years'].quantile(Q1_VAL)
    q3 = group['age_years'].quantile(Q2_VAL)
    return q3 - q1
# function to make df_iqr
def df_iqr_make(df):
    df_iqr = df.groupby('year').apply(calculate_iqr).reset_index(name='iqr')
    return df_iqr


# calculate some values associated with service
#mean length of service for all congress all time, and total members of all congress all time
def service_values(df):
    bioguide_id_counts = df['bioguide_id'].value_counts().reset_index(name='count')
    mean_service = bioguide_id_counts['count'].mean()
    total_members = len(bioguide_id_counts)
    return mean_service, total_members