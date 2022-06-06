get_ipython().system('pip install openpyxl ')

import pandas as pd
import numpy as np
mask_usage = 'Mask Use by County Data.xlsx'
if mask_usage.endswith('.xlsx'):
    data = pd.read_excel(mask_usage)
else:
    print("Wrong file type! Use xlsx file type instead.")
mask_usage_data = pd.DataFrame(data)
county_names = pd.read_csv(r'County Names.csv')
county_names_data = pd.DataFrame(county_names)
mask_usage_data = pd.merge(mask_usage_data, county_names_data)


counties = mask_usage_data["COUNTYFP"].tolist()
for x in range(len(counties)):
    counties[x] = str(counties[x])
    if len(counties[x]) == 4:
        counties[x] = "0" + counties[x]
mask_usage_data["COUNTYFP"] = counties        
        




#Part III Function

 state_codes = {
        'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
        'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
        'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
        'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
        'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
        'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
        'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
        'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
        'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
    }

def states_with_most_and_least_mask_usage(state_codes):
    """ Outputs which states wear their masks the most & which states wears it the least given the county codes
    Arguments:
        state_codes: a dictionary that maps the abbreviation of each state to the first two digits of the COUNTYFP code
    Returns:
        which state wears mask the most frequently and which state wears it the least 
    """
   
    mask_usage_never = {}
    mask_usage_always = {}
    for i in range(len(mask_usage_data)):
        code = mask_usage_data.iloc[i,0]
        state_code = str(code)
        state_code = state_code[:2]
        if state_code not in mask_usage_never.keys():
            mask_usage_never[state_code] = [mask_usage_data.iloc[i, 1]]
            mask_usage_always[state_code] = [mask_usage_data.iloc[i, 5]]
        else:
            mask_usage_never[state_code].append([mask_usage_data.iloc[i, 1]])
            mask_usage_always[state_code].append([mask_usage_data.iloc[i, 5]])
    
    never_averages = []
    for key in mask_usage_never.keys():
        sum = 0
        for x in range(len(mask_usage_never[key])):
            sum += mask_usage_never[key][x]
        never_averages.append([key,sum/len(mask_usage_never[key])])
    
    always_averages = []
    for key in mask_usage_always.keys():
        sum = 0
        for x in range(len(mask_usage_always[key])):
            sum += mask_usage_always[key][x]
        always_averages.append([key, sum/len(mask_usage_always[key])])

    key_always, val_always = max(always_averages,key=lambda x:x[1])
    key_never, val_never = max(never_averages,key=lambda x:x[1])
    state_with_most = ""
    state_with_least = ""
    
    for key, val in state_codes.items():
        if val == str(key_always):
            state_with_most = key
        elif val == str(key_never):
            state_with_least = key
    print("State with the most mask usage: ", state_with_most)
    print("State with the least mask usage: ",state_with_least)



# Part IV, North vs South:


northern_counties = [int('06001'), int('06003'), int('06005'), int('6007'), int('06009'), int('06011'),int('06013'), 
                    int('06015'), int('06017'),int('06019'),int('06021'),int('06023'), int('06033'),
                     int('06035'),int('06039'),int('06041'),int('06043'),int('06045'),int('06047'),int('06049'),int('06055'),int('06057'),int('06061'),int('06063'),int('06067'),int('06075'),int('06077'),
                     int('06079'), int('06081'), int('06085'),int('06087'),int('06089'),int('06091'),int('06093'),int('06095'),int('06097'),int('06099'),int('06101'),int('06103'),int('06105'),int('06109'),
                     int('06113'),int('06115')]
southern_counties = [int('06025'), int('06027'), int('06029'), int('06031'), int('06037'),int('06051'),int('06053'),int('06059'),int('06065'),int('06069'),int('06071'),int('06073'),int('06083'),
                    int('06107'),int('06111')]


def north_vs_south(mask_usage_data, southern_counties, northern_counties):
    """ Outputs which region of California between Norcal and Socal wear the mask most often 
    Arguments:
        mask_usage_data: a dictionary containing the mask usage data 
        southern_counties: a list containing the COUNTYFP codes of Southern California
        northern_counties: a list containing the COUNTYFP codes of Northern California
    Returns:
        Which of Northern California vs Southern California wears their mask more frequently, tie otherwise 
    """
    northern_counties_scores = []
    southern_counties_scores = []
    numRows = len(mask_usage_data['COUNTYFP'])
    
    for x in range(numRows):
        if int(mask_usage_data['COUNTYFP'][x]) in northern_counties:
            northern_counties_scores.append(mask_usage_data['ALWAYS'][x])
        elif int(mask_usage_data['COUNTYFP'][x]) in southern_counties:
            southern_counties_scores.append(mask_usage_data['ALWAYS'][x])
    
    
    sum_northern_always_frequencies = 0
    sum_southern_always_frequencies = 0
    for x in range(len(northern_counties_scores)):
        sum_northern_always_frequencies += northern_counties_scores[x]
    for x in range(len(southern_counties_scores)):
        sum_southern_always_frequencies += southern_counties_scores[x]
    
    
    average_northern_score = sum_northern_always_frequencies/len(northern_counties_scores)
    average_southern_score = sum_southern_always_frequencies/len(southern_counties_scores)
    if average_northern_score > average_southern_score:
        return "Northern California wore their mask the most in 2020!"
    elif average_northern_score < average_southern_score:
        return "Southern California wore their mask the most in 2020!"
    else:
        return "It's a tie!"

   


