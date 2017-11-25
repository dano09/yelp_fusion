import pandas as pd
from tqdm import tqdm
import json
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_business_ids(category, category_file):
    """
    Reads in the business categories file and creates a set of unique business ids
    based on the category parameter
    param: category - gets business ids for the chosen category
    param: category_file - String providing the name of the file
    :return: Set of business id's
    """
    category_df = pd.read_csv(category_file)
    business_indicies = set()
    for i in range(1, 24):
        try:
            business_list = category_df.index[category_df["c" + str(i)] == category].tolist()
            for b in business_list:
                business_indicies.add(b)
        except TypeError:
            break

    business_ids = []
    for b in business_indicies:
        business_ids.append(category_df.iloc[b]['business_id'])

    return(set(business_ids))


def create_csv(business_ids, city, topic):
    """
    Cleans JSON Yelp data and converts it into CSV file with relevant features
    """
    f = open('yelp_dataset/review.json', 'r')

    # used to determine total lines for making progress bar
    # num_lines = sum(1 for line in f)
    # num_lines = 4736897

    # Each line is a business represented by JSON
    df_list = []
    for line in tqdm(f, total=4736897):
        json_string = line

        # Attempt to convert JSON string to dictionary
        try:
            json_obj = json.loads(json_string)

            # Only take reviews for Las Vegas
            if json_obj['business_id'] in business_ids:
                df = pd.DataFrame(json_obj, index=[0])
                df_list.append(df)

        except ValueError:
            print('JSON could not be parsed')

    reviews_df = pd.concat(df_list)

    # Save as CSV file
    reviews_df.to_csv(city + '_' + topic + '_reviews.csv', index=False)


if __name__ == '__main__':

    # Three main parameters:
    # 1) The file containing the city, topics, and its business ids
    #city_category_file_name = 'las_vegas/las_vegas_business_categories.csv'
    city_category_file_name = 'pittsburgh/Pittsburgh_business_categories.csv'

    # 2) The topic for retrieving the reviews. [Too generalized topics are very slow and produce a lot of data]
    topic = 'Burgers'

    # 3) The name of the city
    city = 'Pittsburgh'

    business_ids = get_business_ids(topic, city_category_file_name)

    # Restaurants
    create_csv(business_ids, city, topic)

