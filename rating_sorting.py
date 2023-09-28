# #################################################################################################################
# #                                             Business Problem                                                  #
# #################################################################################################################

# One of the most critical issues in e-commerce is the accurate calculation of post-sale ratings given to products.
# The solution to this problem means more customer satisfaction for the e-commerce site, prominence of the product for the sellers,
# and a hassle-free shopping experience for the buyers.

# Another significant problem is the proper ranking of reviews given to products. Highlighting misleading reviews will directly affect the sale of the product,
# leading to both financial losses and customer loss. By solving these two primary problems, the e-commerce site and sellers will increase their sales,
# while customers will complete their purchasing journey seamlessly.


# #################################################################################################################
# #                                             Dataset Story                                                     #
# #################################################################################################################
#
# This dataset containing Amazon product data encompasses various product categories along with multiple metadata.
# The electronic category's product with the most reviews has user scores and comments.


# #################################################################################################################
# #                                              VARIABLES                                                        #
# #################################################################################################################

# reviewerID                : User ID
# asin                      : Product ID
# reviewerName              : Username
# helpful                   : Degree of helpfulness rating
# reviewText                : Review
# overall                   : Product rating
# summary                   : Review summary
# unixReviewTime            : Review time
# reviewTime                : Raw review time
# day_diff                  : Number of days since the review
# helpful_yes               : Number of times the review was found helpful
# total_vote                : Number of votes given to the review

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
import warnings
warnings.filterwarnings('ignore')
import math
from math import sqrt


pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 500)
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


# ###############################################################################################################
# Task 1: Calculate the Average Rating based on current reviews and compare it with the existing average rating.
# ###############################################################################################################


#  - Step 1: Calculate the average score of the product.

df['overall'].mean()


#  - Step 2: Calculate the weighted average score based on the date.


df.loc[df["day_diff"] <= df["day_diff"].quantile(0.25),"overall"].mean()
# 4.69579

df.loc[(df["day_diff"] > df["day_diff"].quantile(0.25)) & (df["day_diff"] <= df["day_diff"].quantile(0.50)) ,"overall"].mean()
# 4.63614

df.loc[(df["day_diff"] > df["day_diff"].quantile(0.50)) & (df["day_diff"] <= df["day_diff"].quantile(0.75)) ,"overall"].mean()
# 4.57166

df.loc[df["day_diff"] > df["day_diff"].quantile(0.75),"overall"].mean()
# 4.44625

#defining a function of time based weighted average
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.25),"overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.25)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.50)) ,"overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.50)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.75)) ,"overall"].mean() * w3 / 100 + \
           dataframe.loc[dataframe["day_diff"] > dataframe["day_diff"].quantile(0.75),"overall"].mean() * w4 / 100

time_based_weighted_average(df, w1=28, w2=26, w3=24, w4=22)
# 4.595593165128118

#  - Step 3: Compare and interpret the average of each time frame in weighted scoring.

df['overall'].mean()
# 4.587589013224822
time_based_weighted_average(df, w1=30, w2=26, w3=24, w4=20)
# 4.600583941300071



# ###############################################################################################################
# Task 2: Determine 20 reviews to be displayed on the product detail page for the product.
# ###############################################################################################################

# - Step 1: Generate the helpful_no variable.

df['helpful_no'] = df['total_vote'] - df['helpful_yes']


df = df[["reviewerName", "overall", "summary", "helpful_yes", "helpful_no", "total_vote", "reviewTime"]]
df.head(10)

#                                        reviewerName  overall                                            summary  helpful_yes  helpful_no  total_vote  reviewTime
# 0                                               NaN  4.00000                                         Four Stars            0           0           0  2014-07-23
# 1                                              0mie  5.00000                                      MOAR SPACE!!!            0           0           0  2013-10-25
# 2                                               1K3  4.00000                          nothing to really say....            0           0           0  2012-12-23
# 3                                               1m2  5.00000             Great buy at this price!!!  *** UPDATE            0           0           0  2013-11-21
# 4                                      2&amp;1/2Men  5.00000                                   best deal around            0           0           0  2013-07-13
# 5                                           2Cents!  5.00000                        Not a lot to really be said            0           0           0  2013-04-29
# 6                                        2K1Toaster  5.00000                                         Works well            0           0           0  2013-10-19
# 7  35-year Technology Consumer "8-tracks to 802.11"  5.00000  32 GB for less than two sawbucks...what's not ...            0           0           0  2014-10-07
# 8                                         4evryoung  5.00000                                      Loads of room            1           0           1  2014-03-24
# 9                                          53rdcard  5.00000                                        works great            0           0           0  2013-11-10


# - Step 2: Calculate score_pos_neg_diff, score_average_rating, and wilson_lower_bound scores and add them to the data.

def wilson_lower_bound(up, down, confidence=0.95):
    """
   Calculate Wilson Lower Bound Score

   - The lower bound of the confidence interval calculated for the Bernoulli parameter p is accepted as the WLB score.
   - The score to be calculated is used for product ranking.
   - Note:
   If scores are between 1-5, those between 1-3 are marked negative, and 4-5 are marked positive, making it suitable for Bernoulli.
   This also introduces some problems. Therefore, it's necessary to do a Bayesian average rating.

   Parameters
   ----------
   up: int
       up count
   down: int
       down count
   confidence: float
       confidence

   Returns
   -------
   wilson score: float

"""
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

# Define score_pos_neg_diff, score_average_rating and wilson_lower_bound functions
def score_pos_neg_diff(up, down):
    return up - down

def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)

# Calculate new scores by these functions

df["score_pos_neg_diff"] = df.apply(lambda x: score_pos_neg_diff(x["helpful_yes"], x["helpful_no"]), axis=1)
df.sort_values("score_pos_neg_diff", ascending=False).head(20)

df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)
df.sort_values("score_average_rating", ascending=False).head(20)

df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)



# - Step 3: Determine the 20 reviews and interpret the results.

# Sorting the first 20 comments by "wilson_lower_bound"
df.sort_values("wilson_lower_bound", ascending=False).head(20)