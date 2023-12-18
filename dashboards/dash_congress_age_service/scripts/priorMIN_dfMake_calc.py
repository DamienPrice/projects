import sys
sys.path.append('..')  # Add the parent directory to the Python path

import pandas as pd
from config import MIN_CONGRESS, MAX_CONGRESS


# check to see if the new df doesn't have MIN
def check_condition(df, year_max): #return true if there are any bioguide_id sets that don't include year_max and are less than year_max
    for bioguide_id, group_df in df.groupby('bioguide_id'):
        if all(group_df['congress'] < year_max) and year_max not in group_df['congress'].values:
            return True
    return False

# make df without set of members serving before lowest congress in df
def remove_min_df_make(df):
    # get t/f list of all ids that have congress = MIN
    filtered_df_MIN = df[df['congress'] == MIN_CONGRESS]

    # remove all ids from df that have congress = MIN
    df_noMIN = df[~(df['bioguide_id'].isin(filtered_df_MIN['bioguide_id']))]

    # get t/f list of all ids that have congress = MIN+1 of the df with no MIN
    filtered_df_MINplus1 = df_noMIN[df_noMIN['congress'] == MIN_CONGRESS+1]

    # make new df with all rows of ids that have MIN+1 but not MIN. df_MINplus1_noMIN : df with all rows of ids having MIN+1 as first congress
    df_MINplus1_noMIN = df_noMIN[df_noMIN['bioguide_id'].isin(filtered_df_MINplus1['bioguide_id'])]

    # Find the longest serving that began in MIN+1
    most_common_bioguide_id = df_MINplus1_noMIN['bioguide_id'].value_counts().idxmax()

    # make df of longest serving starting from MIN+1, then get the last year served
    df_longest_from_MINplus1 = df_MINplus1_noMIN[df_MINplus1_noMIN['bioguide_id'] == most_common_bioguide_id]
    year_max = df_longest_from_MINplus1.max()['congress']

    # with the final year of longest serving starting from MIN+1, year_max, make t/f list of all ids from df_noMIN that have year_max
    filtered_df_having_max_noMIN = df_noMIN[df_noMIN['congress'] == year_max]

    # make df with all rows of ids that contain year_max and no 66 and 67 smallest but not necessary. i.e. all rows of ids who served in 70 and didn't begin service prior to 67.
    df_year_max = df_noMIN[df_noMIN['bioguide_id'].isin(filtered_df_having_max_noMIN['bioguide_id'])]

    # add all the rest of ids that don't contain year max and are greater than year max.
    additional_criteria = (df_noMIN['congress'] >= year_max+1) & ~df_noMIN['bioguide_id'].isin(df_year_max['bioguide_id'])
    additional_rows = df_noMIN[additional_criteria]
    df_final_noMIN = pd.concat([df_year_max, additional_rows])

    # checking that the df doesn't contain prior MIN members
    result = check_condition(df_final_noMIN, year_max)

    df_final_noMIN.to_csv('../data/congress_data_noMIN.csv', index=False)
    
    print('CSV noMIN created.')
    print('There are ids with MIN: ', result)

    return df_final_noMIN, year_max

# calculate mean service of all members for each congress, starts from lowest possible (year_max)
def calc_mean_service(df_final_noMIN, year_max):
    terms_served_means = []

    for c in range(year_max,MAX_CONGRESS):
        # get t/f list of all ids that have congress = c
        filtered_df_c = df_final_noMIN[df_final_noMIN['congress'] == c]

        # make new df with all rows of ids that have y
        df_c_plus = df_final_noMIN[df_final_noMIN['bioguide_id'].isin(filtered_df_c['bioguide_id'])]

        # remove all rows of >y
        df_c_noPlus = df_c_plus[df_c_plus['congress'] <= c]

        # get mean of the years served up to congress c
        terms_served_mean_c = df_c_noPlus['bioguide_id'].value_counts().mean()
        pair = (2*c+1787, terms_served_mean_c) # year, mean
        terms_served_means.append(pair)

    df_mean_terms_served = pd.DataFrame(terms_served_means, columns=['Year', 'Terms Served Mean'])

    # create csv of the terms served data
    df_mean_terms_served.to_csv('../data/congress_mean_service.csv', index=False)

    print('CSV with mean service created.')

    return


def main():
    df = pd.read_csv('../data/congress_data.csv')
    
    # create df,csv without prior MIN serving
    df_final_noMIN, year_max = remove_min_df_make(df)

    #  csv with mean service
    calc_mean_service(df_final_noMIN, year_max)


###########################################
##          main
if __name__ == '__main__':
    main()
