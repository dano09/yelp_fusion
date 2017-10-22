import pandas as pd
import numpy as np
import json
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def create_csv():
    """
    Cleans JSON Yelp data and converts it into CSV file with relevant features
    """
    f = open('yelp_dataset/business.json', 'r')
    df = pd.DataFrame(columns=['business_id', 'name', 'neighborhood', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'stars', 'review_count'])
    row = -1

    # Each line is a business represented by JSON
    for line in f:
        row += 1
        json_string = line

        # Attempt to convert JSON string to dictionary
        try:
            json_obj = json.loads(json_string)

            # Focuses on Las Vegas Yelp Data
            if json_obj['city'] == 'Las Vegas':

                # Remove unnecessary key/values
                json_obj.pop('is_open')
                json_obj.pop('attributes')
                json_obj.pop('hours')

                # Create Pandas DataFrame from JSON dictonary
                for key in json_obj.keys():
                    df.loc[row, key] = json_obj[key]

        except ValueError:
            print('JSON could not be parsed')

    # Save as CSV file
    df.to_csv('las_vegas.csv', index=False)


def get_bus_categories():
    """
    Get every type of business category and save as text file
    """
    categories = set()
    f = open('yelp_dataset/business.json', 'r')
    for line in f:
        json_string = line
        try:
            # Look through JSON file and add business categories to the set
            json_obj = json.loads(json_string)

            # Focuses on Las Vegas Yelp Data
            if json_obj['city'] == 'Las Vegas':
                cats = json_obj['categories']

                # Some businesses have several categories
                for c in cats:
                    # Only add unique categories
                    if c not in categories:
                        categories.add(c)

        except ValueError:
            print('JSON could not be parsed')

    # Create file of categories
    cat_file = open('categories.txt', 'w')
    for c in categories:
        cat_file.write("%s\n" % c)


def get_largest_category_count():
    """
    Determines the maximum number of categories that Las Vegas Yelp data contains.
    The value calculated here is used to determine the number of columns used in
    create_cat_dataframe()
    """
    category_count = 0
    f = open('yelp_dataset/business.json', 'r')
    for line in f:
        json_string = line
        try:
            json_obj = json.loads(json_string)
            if json_obj['city'] == 'Las Vegas':
                cat_size = len(json_obj['categories'])

                # Keep the largest count of categories
                if cat_size > category_count:
                    category_count = cat_size

        except ValueError:
            print('JSON could not be parsed')

    print('HIGHEST NUMBER OF CATEGORIES IS: {}'.format(category_count))



def create_cat_dataframe():
    """
    Creates a CSV file that contains that categories for each business
    """
    # 24 columns was determined by get_largest_category_count()
    category_df = pd.DataFrame(columns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6',
                                        'c7', 'c8', 'c9', 'c10', 'c11', 'c12',
                                        'c13', 'c14', 'c15', 'c16', 'c17', 'c18',
                                        'c19', 'c20', 'c21', 'c22', 'c23', 'c24'])

    f = open('yelp_dataset/business.json', 'r')
    for line in f:
        json_string = line

        # Attempt to convert JSON string to dictionary
        try:
            json_obj = json.loads(json_string)

            # Focuses on Las Vegas Yelp Data
            if json_obj['city'] == 'Las Vegas':

                # Get list of categories for the business
                cats = json_obj['categories']

                # Gets the business ID to reference other business data
                bus_id = json_obj['business_id']

                # incrementally add categories to the dataframe
                for i, c in enumerate(cats):
                    column_name = 'c' + str(i + 1)
                    category_df.loc[bus_id, column_name] = c


        except ValueError:
            print('JSON could not be parsed')

    # Save the dataframe as .CSV file
    category_df.index.name = 'business_id'
    category_df.to_csv('business_categories.csv')

if __name__ == '__main__':

    create_csv()
    get_bus_categories()
    get_largest_category_count()
    create_cat_dataframe()
