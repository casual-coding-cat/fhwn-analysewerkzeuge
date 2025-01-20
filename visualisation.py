import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
from tqdm.notebook import tqdm
import folium
from folium.plugins import HeatMap
from processor import Data
from unicodedata import normalize

data_class = Data()
data = data_class.get_data()

sns.set_style("darkgrid")


# Visualizations: Distribution of numerical features
plt.figure(figsize=(12, 6))
sns.histplot(data['Age'], kde=True, bins=30, color='skyblue', edgecolor='black')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Occurrences')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(data['Purchase Amount (USD)'], kde=True, bins=20, color='orange', edgecolor='black')
plt.title('Purchase Amount Distribution')
plt.xlabel('Purchase Amount (USD)')
plt.ylabel('Frequency')
plt.show()

#----------------------------------------

# Category Distribution
plt.figure(figsize=(8, 5))
data["Category"].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("rocket_r"), startangle=140)
plt.title("Category Distribution", fontsize=14)
plt.ylabel('')
plt.show()

#----------------------------------------

# Group the data by Gender and Category and calculate the relative frequency
gender_category_counts = data.groupby(['Gender', 'Category']).size().unstack()

# Convert to relative frequencies
relative_frequencies = gender_category_counts.div(gender_category_counts.sum(axis=1), axis=0) * 100

# Display the results
print(relative_frequencies)

# Visualize the results with a bar chart
relative_frequencies.plot(kind='bar', figsize=(10, 6), color=sns.color_palette("rocket_r"))
plt.title('Relative Frequency of Items Bought by Gender Across Categories')
plt.ylabel('Percentage (%)')
plt.xlabel('Gender')
plt.xticks(rotation=0)
plt.legend(title='Category')
plt.show()

#----------------------------------------

# Purchase Amount Distribution
plt.figure(figsize=(12, 4))
sns.boxplot(x=data['Purchase Amount (USD)'], palette=sns.color_palette("rocket_r"))
plt.title('Purchase Amount Distribution')
plt.xlabel('Purchase Amount (USD)')
plt.show()

#----------------------------------------

# Used Payment Method
payment_method = data['Payment Method'].value_counts(normalize=True) * 100
payment_method.plot(kind='bar', figsize=(10, 6), color=sns.color_palette("rocket_r"))
plt.title('Used Payment Method')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.show()

#----------------------------------------

# Preferred Payment Method
preferred_payment_method = data['Preferred Payment Method'].value_counts(normalize=True) * 100
preferred_payment_method.plot(kind='bar', figsize=(10, 6), color=sns.color_palette("rocket_r"))
plt.title('Preferred Payment Method')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.show()

#----------------------------------------

# Age vs. Previous Purchases
plt.figure(figsize=(10, 6))
sns.regplot(x='Age', y='Previous Purchases', data=data, color='orange', line_kws={'color': 'darkorange'})
plt.title('Age vs. Previous Purchases')
plt.show()

#----------------------------------------

# Purchases per Season
seasons = data['Season'].value_counts(normalize=True) * 100
seasons.plot(kind='bar', figsize=(10, 6), color=sns.color_palette("rocket_r"))
plt.title('Purchases per Season')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.show()

#---------------------------------------

size = data['Size'].value_counts(normalize=True) * 100
size = size.reindex(['S', 'M', 'L', 'XL'])
size.plot(kind='bar', figsize=(10, 6), color=sns.color_palette("rocket_r"))
plt.title('Size Distribution')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.show()

#----------------------------------------

# frequency of purchases vs. age

# violinplot
plt.figure(figsize=(8, 6))
sns.violinplot(x='Frequency of Purchases', y='Age', data=data, inner='quartile', palette='rocket_r', order=['Weekly', 'Bi-Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Every 3 Months', 'Annually'])
plt.title('Frequency of Purchases vs. Age', fontsize=14)
plt.xlabel('Frequency of Purchases', fontsize=12)
plt.ylabel('Age', fontsize=12)

plt.show()

# boxplot + swarmplot
plt.figure(figsize=(8, 6))
sns.boxplot(x='Frequency of Purchases', y='Age', data=data, whis=1.5, color='purple', order=['Weekly', 'Bi-Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Every 3 Months', 'Annually'])
sns.swarmplot(x='Frequency of Purchases', y='Age', data=data, color='orange', alpha=0.7, order=['Weekly', 'Bi-Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Every 3 Months', 'Annually'])
plt.title('Frequency of Purchases vs. Age', fontsize=14)
plt.xlabel('Frequency of Purchases', fontsize=12)
plt.ylabel('Age', fontsize=12)

plt.show()

#-------------------------------------------



"""heatmaps"""

# Get the list of unique locations
unique_locations = data['Location'].unique()

geolocator = Nominatim(user_agent="bytescout", timeout=None)

# function that assigns coordinates to location
def get_loc_coordinate(location):
    location = geolocator.geocode(query = location)
    return location.latitude, location.longitude

tqdm.pandas()

location_coordinates = {location: get_loc_coordinate(location) for location in unique_locations}

# number of purchases per location
location_distribution = data.groupby('Location').size().reset_index(name='purchases_per_location')

def creat_heatmap(df, name:str, normed:bool):
    if normed:
        df[name+"_normed"] = df[name]/location_distribution['purchases_per_location']
        name = name+"_normed"
    # Map the coordinates to the DataFrame
    df['lat'] = df['Location'].map(lambda loc: location_coordinates[loc][0] if loc in location_coordinates else None)
    df['long'] = df['Location'].map(lambda loc: location_coordinates[loc][1] if loc in location_coordinates else None)

    # get correct format
    lat_longs = list(map(list, zip(df["lat"],
                                   df["long"],
                                   df[name])))

    # create heat map
    map_object = folium.Map(location=[33.2588817, -86.8295337], zoom_start=4)

    HeatMap(lat_longs).add_to(map_object)

    map_object.save(name+'.html')


#purchase distribution
creat_heatmap(location_distribution, 'purchases_per_location', normed=False)

#outerwear purchases
data_outerwear = data.where(data["Category"]=="Outerwear")
outerwear_per_location = data_outerwear.groupby("Location").size().reset_index(name='outerwear_purchases')

creat_heatmap(outerwear_per_location, "outerwear_purchases", normed=False)
creat_heatmap(outerwear_per_location, "outerwear_purchases", normed=True)

#sunglass purchases
sunglass_purchases  = data.where(data["Item Purchased"]=="Sunglasses")
sunglasses_per_location = sunglass_purchases.groupby("Location").size().reset_index(name='sunglass_purchases')

creat_heatmap(sunglasses_per_location, "sunglass_purchases", normed=True)

#clothing sizes
clothing_sizes = data.where(data["Category"]=="Clothing")

size_to_number = {'S': 0, 'M':10, 'L':20, 'XL':30}
clothing_sizes['clothing_sizes'] = clothing_sizes['Size'].map(size_to_number)
clothing_sizes_per_location = clothing_sizes.groupby("Location").sum().reset_index()

creat_heatmap(clothing_sizes_per_location, "clothing_sizes", normed=True)