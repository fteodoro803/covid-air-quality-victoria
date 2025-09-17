# CODE FOR READING IN THE SUBURB-POSTCODE CONVERSION FILE
import pandas as pd

sub_post = pd.read_csv(r"datasets/AustralianPostcodes.csv")
sub_post = sub_post.loc[:, ["postcode", "locality", "state"]]

# Preprocessing for Consistency
sub_post.columns = ['postcode', 'suburb', 'state']  # preprocessing, for consistency, suburb=locality
sub_post['suburb'] = sub_post['suburb'].str.lower()  # lowercasing

# Separates the Victorian postcodes
sub_post = sub_post[sub_post["state"] == "VIC"]
sub_post = sub_post[sub_post['postcode'] <= 3999]  # Victorian LVR postcodes are in these ranges

# Removes State, not needed anymore
sub_post = sub_post[['postcode', 'suburb']]

# Adding Discrepancies in Dataset (location-postcode), which are found in others. Refer to End of file (1)
sub_post.loc[len(sub_post) + 1] = [3000] + ['melbourne cbd']
sub_post.loc[len(sub_post) + 1] = [3220] + ['geelong south']
sub_post.loc[len(sub_post) + 1] = [3840] + ['morwell south']

print(sub_post.head(5))

sub_post.to_csv('processedSuburbPostcodeData.csv', index=False)  # Saving Database for Visualisation

"""
    1. Manual addition of the postcodes was done because the code could not find matches due to the following:
        - there was no Melbourne CBD in Postcode Database
        - Geelong South in one was South Geelong in another
        - Morwell South doesn't exist in the Postcode Database
        - All Postcodes were found on Google
"""
