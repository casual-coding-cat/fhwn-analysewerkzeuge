import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from processor import Data

data_class = Data()
data = data_class.get_data()

def do_analysis():
    #items purchased
    print(data['Item Purchased'].unique())

    #review with discount
    data_with_discount  = data.where((data['Discount Applied']=='Yes') | (data['Promo Code Used']=='Yes')).dropna()
    review_with_discount = data_with_discount['Review Rating'].mean()
    print("mean review when discount or promo code applied: " +str(review_with_discount))

    #review without discount
    data_without_discount  = data.where((data['Discount Applied']!='Yes') & (data['Promo Code Used']!='Yes')).dropna()
    review_without_discount = data_without_discount['Review Rating'].mean()
    print("mean review when no code applied: " +str(review_without_discount))

    #gender distribution
    print(data['Gender'].value_counts(normalize = True))

    #most popular colors of each season
    top_colors_per_season = data.groupby('Season')['Color'].value_counts().groupby(level=0).head(3).reset_index(name='Count')
    print(top_colors_per_season)

    #purchase amount for free shipping
    data_free_shipping  = data.where(data['Shipping Type']=='Free Shipping').dropna()
    purchase_amount = data_free_shipping['Purchase Amount (USD)'].mean()
    print("mean purchase amount with free shipping: " +str(purchase_amount))

    #purchase amount no free shipping
    data_no_free_shipping  = data.where(data['Shipping Type']!='Free Shipping').dropna()
    purchase_amount = data_no_free_shipping['Purchase Amount (USD)'].mean()
    print("mean purchase amount without free shipping: " +str(purchase_amount))

