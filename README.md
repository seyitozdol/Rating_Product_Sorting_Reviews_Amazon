## Rating Product Sorting Reviews Amazon
 An analysis of Amazon's product ratings and review sorting, addressing challenges in accurate rating calculation and review ranking for enhanced e-commerce experiences.

![image](https://images.moneycontrol.com/static-mcnews/2023/03/amazon-shut-down-featured--580x435.png)


 **************************
## Business Problem:
One of the most critical issues in e-commerce is the accurate calculation of post-sale ratings given to products. The solution to this problem means more customer satisfaction for the e-commerce site, prominence of the product for the sellers, and a hassle-free shopping experience for the buyers. Another significant problem is the proper ranking of reviews given to products. Highlighting misleading reviews will directly affect the sale of the product, leading to both financial losses and customer loss. By solving these two primary problems, the e-commerce site and sellers will increase their sales, while customers will complete their purchasing journey seamlessly.
 **************************

 **************************
## Dataset Story:
 This dataset containing Amazon product data encompasses various product categories along with multiple metadata. The electronic category's product with the most reviews has user scores and comments.
 **************************

 **************************
## VARIABLES


| **Variable Name**   |**Description**                              |
| ------------------- |---------------------------------------------|
| reviewerID          | User ID                                     |
| asin                | Product ID                                  |
| reviewerName        | Username                                    |
| helpful             | Degree of helpfulness rating                |
| reviewText          | Review                                      |
| overall             | Product rating                              |
| summary             | Review summary                              |
| unixReviewTime      | Review time                                 |
| reviewTime          | Raw review time                             |
| day_diff            | Number of days since the review             |
| helpful_yes         | Number of times the review was found helpful |
| total_vote          | Number of votes given to the review         |


## Project Tasks
**Task** 1: Calculate the Average Rating based on current reviews and compare it with the existing average rating.
 - Step 1: Calculate the average score of the product.
 - Step 2: Calculate the weighted average score based on the date.
 - Step 3: Compare and interpret the average of each time frame in weighted scoring.

**Task** 2: Determine 20 reviews to be displayed on the product detail page for the product.

- Step 1: Generate the helpful_no variable.

- Step 2: Calculate score_pos_neg_diff, score_average_rating, and wilson_lower_bound scores and add them to the data.

- Step 3: Determine the 20 reviews and interpret the results.