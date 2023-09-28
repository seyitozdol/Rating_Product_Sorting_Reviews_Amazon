# ****** Business Problem: *******************************************
# One of the most critical issues in e-commerce is the accurate calculation of post-sale ratings given to products.
# The solution to this problem means more customer satisfaction for the e-commerce site, prominence of the product for the sellers, and a hassle-free shopping experience for the buyers.
# Another significant problem is the proper ranking of reviews given to products. Highlighting misleading reviews will directly affect the sale of the product, leading to both financial losses and customer loss.
# By solving these two primary problems, the e-commerce site and sellers will increase their sales, while customers will complete their purchasing journey seamlessly.
# ********************************************************************

# **************************
# Dataset Story:
# This dataset containing Amazon product data encompasses various product categories along with multiple metadata. The electronic category's product with the most reviews has user scores and comments.
# **************************

# **************************
# VARIABLES
# reviewerID:               User ID
# asin:                     Product ID
# reviewerName:             Username
# helpful:                  Degree of helpfulness rating
# reviewText:               Review
# overall:                  Product rating
# summary:                  Review summary
# unixReviewTime:           Review time
# reviewTime:               Raw review time
# day_diff:                 Number of days since the review
# helpful_yes:              Number of times the review was found helpful
# total_vote:               Number of votes given to the review
# **************************

# **************************
# Project Tasks
# Task 1: Calculate the Average Rating based on current reviews and compare it with the existing average rating.
#  - Step 1: Calculate the average score of the product.
#  - Step 2: Calculate the weighted average score based on the date.
#  - Step 3: Compare and interpret the average of each time frame in weighted scoring.

# Task 2: Determine 20 reviews to be displayed on the product detail page for the product.

# - Step 1: Generate the helpful_no variable.#
# - Step 2: Calculate score_pos_neg_diff, score_average_rating, and wilson_lower_bound scores and add them to the data.
# - Step 3: Determine the 20 reviews and interpret the results.
# **************************

import datetime as dt
import numpy as np
import pandas as pd
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 500)
# pd.set_option('display_max_rows',None)
pd.set_option('display.float_format',lambda x : '%.5f' % x)

df_ = pd.read_csv(r'C:\Users\zygom\OneDrive\Belgeler\GitHub\Rating_Product_Sorting_Reviews_Amazon\amazon_review.csv')
#df_ = pd.read_csv(amazon_review.csv')
df = df_.copy()

# A function is used for missing value analysis
def analyze_missing_values(df):
    na_cols = df.columns[df.isna().any()].tolist()
    total_missing = df[na_cols].isna().sum().sort_values(ascending=False)
    percentage_missing = ((df[na_cols].isna().sum() / df.shape[0]) * 100).sort_values(ascending=False)
    missing_data = pd.DataFrame({'Missing Count': total_missing, 'Percentage (%)': np.round(percentage_missing, 2)})
    return missing_data

# to get an initial understanding of the data's structure, its content, and if there are any missing values that need to be addressed.
def sum_df(dataframe, head=6):
    print("~~~~~~~~~~|-HEAD-|~~~~~~~~~~ ")
    print(dataframe.head(head))
    print("~~~~~~~~~~|-TAIL-|~~~~~~~~~~ ")
    print(dataframe.tail(head))
    print("~~~~~~~~~~|-TYPES-|~~~~~~~~~~ ")
    print(dataframe.dtypes)
    print("~~~~~~~~~~|-SHAPE-|~~~~~~~~~~ ")
    print(dataframe.shape)
    print("~~~~~~~~~~|-NUMBER OF UNIQUE-|~~~~~~~~~~ ")
    print(dataframe.nunique())
    print("~~~~~~~~~~|-NA-|~~~~~~~~~~ ")
    print(dataframe.isnull().sum())
    print("~~~~~~~~~~|-QUANTILES-|~~~~~~~~~~ ")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("~~~~~~~~~~|-NUMERIC COLUMNS-|~~~~~~~~~~ ")
    print([i for i in dataframe.columns if dataframe[i].dtype != "O"])
    print("~~~~~~~~~~|-MISSING VALUE ANALYSIS-|~~~~~~~~~~ ")
    print(analyze_missing_values(dataframe))

sum_df(df)


# **************************************************************************************************************
# Task 1: Calculate the Average Rating based on current reviews and compare it with the existing average rating.
# **************************************************************************************************************

#  - Step 1: Calculate the average score of the product.
#  - Step 2: Calculate the weighted average score based on the date.
#  - Step 3: Compare and interpret the average of each time frame in weighted scoring.

# *******************************************************************************************************
# Task 2: Determine 20 reviews to be displayed on the product detail page for the product.
# *******************************************************************************************************

# - Step 1: Generate the helpful_no variable.#
# - Step 2: Calculate score_pos_neg_diff, score_average_rating, and wilson_lower_bound scores and add them to the data.
# - Step 3: Determine the 20 reviews and interpret the results.