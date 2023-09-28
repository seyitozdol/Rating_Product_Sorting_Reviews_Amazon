# **************************
# Business Problem:
# One of the most critical issues in e-commerce is the accurate calculation of post-sale ratings given to products.
# The solution to this problem means more customer satisfaction for the e-commerce site, prominence of the product for the sellers, and a hassle-free shopping experience for the buyers.
# Another significant problem is the proper ranking of reviews given to products. Highlighting misleading reviews will directly affect the sale of the product, leading to both financial losses and customer loss.
# By solving these two primary problems, the e-commerce site and sellers will increase their sales, while customers will complete their purchasing journey seamlessly.
# **************************

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
# Task 1: Data Prepration
# Task 2: Creation of the CLTV Data Structure
# Task 3: Establishment of BG/NBD and Gamma-Gamma Models and Calculation of CLTV
# Task 4: Segmentation Based on CLTV Value


import datetime as dt
import numpy as np
import pandas as pd
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 500)
# pd.set_option('display_max_rows',None)
pd.set_option('display.float_format',lambda x : '%.5f' % x)

df_ = pd.read_csv('amazon_review.csv')
df = df_.copy()

#*****************************
# Task 1: Data Prepration
#*****************************

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

def outlier_thresholds(dataframe, variable):
    '''
        Sets the boundaries of outliers.
    Parameters
    ----------
    dataframe :DataFrame
    variable : int

    Returns
    -------
    low_limit : The low limit of data
    up_limit : The up limit of data
    '''
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    '''
        The function that necessary to suppress outliers
    Parameters
    ----------
    dataframe: DataFrame
    variable : int

    Returns
    -------
    '''
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit,0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit,0)


columns = [i for i in df.columns if df[i].dtype != "O"]

for col in columns:
    replace_with_thresholds(df, col)

#*********************************************
# Task 2: Creation of the CLTV Data Structure
#*********************************************

df["tot_ord_num"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]

df["tot_customer_value"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

date_columns = [i for i in df.columns if "date" in i.lower()]
df[date_columns] = df[date_columns].apply(pd.to_datetime)

df["last_order_date"].max()
#  '2021-05-30'
last_date = dt.datetime(2021,5,30)
today_date = dt.datetime(2021, 6, 2)

cltv_df = pd.DataFrame({"customer_id": df["master_id"],
             "recency_cltv_weekly": ((df["last_order_date"] - df["first_order_date"]).dt.days)/7,
             "T_weekly": ((today_date - df["first_order_date"]).astype('timedelta64[D]'))/7,
             "frequency": df["tot_ord_num"],
             "monetary_cltv_avg": df["tot_customer_value"] / df["tot_ord_num"]})


#*********************************************************************************
# Task 3: Establishment of BG/NBD and Gamma-Gamma Models and Calculation of CLTV
#*********************************************************************************

# STEP 1 : Fit the BG/NBD Model

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
       cltv_df['recency_cltv_weekly'],
       cltv_df['T_weekly'])

cltv_df["exp_sales_3_month"] = bgf.conditional_expected_number_of_purchases_up_to_time(4*3,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency_cltv_weekly'],
                                                        cltv_df['T_weekly'])

cltv_df["exp_sales_6_month"] = bgf.predict(4*6,
                                       cltv_df['frequency'],
                                       cltv_df['recency_cltv_weekly'],
                                       cltv_df['T_weekly'])

# STEP 2 : Fit the Gamma Gamma Model
ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

cltv_df["exp_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency_cltv_weekly'],
                                       cltv_df['T_weekly'],
                                       cltv_df['monetary_cltv_avg'],
                                       time=6,
                                       freq="W",
                                       discount_rate=0.01)

cltv_df["cltv"] = cltv
cltv_df.sort_values("cltv",ascending=False)[:10]

#*********************************************
# Task 4: Segmentation Based on CLTV Value
#*********************************************

cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])


cltv_df.groupby("cltv_segment").agg({"count","mean","sum"})

#              recency_cltv_weekly                     T_weekly                    frequency                   monetary_cltv_avg                     exp_sales_3_month                  exp_sales_6_month                  exp_average_profit                          cltv
#                             mean count          sum      mean count          sum      mean count         sum              mean count           sum              mean count        sum              mean count        sum               mean count           sum      mean count           sum
# cltv_segment
# D                      138.72425  4987 691817.85714 161.97141  4987 807751.42857   3.74093  4987 18656.00000          92.38507  4987  460724.32698           0.40452  4987 2017.35046           0.80904  4987 4034.70091           97.79566  4987  487706.94067  79.45112  4987  396222.75123
# C                      100.80173  4986 502597.42857 120.79726  4986 602295.14286   4.35780  4986 21728.00000         126.95077  4986  632976.55825           0.49045  4986 2445.39334           0.98090  4986 4890.78668          133.23154  4986  664292.46104 131.79758  4986  657142.73509
# B                       81.95705  4986 408637.85714 100.59805  4986 501581.85714   4.74007  4986 23634.00000         158.50378  4986  790299.84401           0.54990  4986 2741.77839           1.09979  4986 5483.55679          165.64402  4986  825901.06379 183.88841  4986  916867.59852
# A                       59.56223  4986 296977.28571  75.08255  4986 374361.57143   4.98355  4986 24848.00000         218.70167  4986 1090446.52566           0.64156  4986 3198.82105           1.28312  4986 6397.64210          228.34154  4986 1138510.92410 292.31831  4986 1457499.10773




