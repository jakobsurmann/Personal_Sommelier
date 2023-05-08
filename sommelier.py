#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import necessary libraries
import pandas as pd
import openpyxl
import streamlit as st
import random
from PIL import Image

# Data loading and cleaning
wine = pd.read_csv('wines.csv', on_bad_lines='skip')
wine = wine.dropna(subset=['price'])
wine = wine.dropna(subset=['country'])
wine = wine.dropna(subset=['variety'])

# Data check
print(wine["price"].isnull().sum())
print(wine['country'].isnull().sum())
print(wine['variety'].isnull().sum())

# Importing and adding picture to website
image = Image.open('sommelier_v2.png')
st.image(image, width = 300, use_column_width="auto")

# Title for the app
st.title("Wine recommendation")

# Description
st.write("Hello, I am your personal Sommelier. I can give you random wine recommendations, or recommendations based on your personal preferences.")
st.write("Option A: Click the button below to get a random wine recommendation:")



# Random wine recommendation

# Define random function
def wine_random():
    wine_random = wine[(wine["points"] >= 91)]
    wine_random_sample = wine_random.sample(n=5)

    index_list_random = []
    i = 1
    for x in range(len(wine_random_sample)):
        index_list_random.append(i)
        i += 1
    recom_random_index = pd.Series(index_list_random, dtype="int64")
    wine_random_sample.set_index(recom_random_index, inplace=True)

    return wine_random_sample[["title", "variety", "winery", "points"]].head(5)

# Create button to display random wine recommendation

if st.button("Random recommendation"):
    # Recommendation output
    st.write(f"Your random wine is: ")
    st.write(wine_random())

# Recommendation based on price
st.write('Option B: I can also give you recommendations based on your Euro price range:')

# Create an expandable field
with st.beta_expander("Option B: Recommendations based on your Euro price range"):
    col1, col2 = st.beta_columns(2)
    # Input fields for Min and Max prices
    min_price_input = col1.text_input('Min').replace(',', '.')
    max_price_input = col2.text_input('Max').replace(',', '.')

    # Give desired output based on Min and Max price
    if min_price_input and max_price_input:
        min_price = float(min_price_input)
        max_price = float(max_price_input)
        wine_price_filtered = wine[wine['price'].between(min_price, max_price)]
        recom10 = wine_price_filtered[wine_price_filtered['points'] > 91]
        if len(recom10) >= 1:
            sample_size = min(len(recom10), 5)
            recom11 = recom10.sample(n=sample_size)
            recom12 = recom11.sort_values(by="points", ascending=False)
            index_list_12 = []
            i = 1
            for x in range(len(recom12)):
                index_list_12.append(i)
                i += 1
            recom12_index = pd.Series(index_list_12, dtype="int64")
            recom12.set_index(recom12_index, inplace=True)
            recom13 = recom12[["title", "variety", "winery", "price", "points"]]
            st.write('Here are recommendations in your desired price range')
            st.write(recom13)
        elif max_price < min_price:
            st.write('Your maximum price is below your minimum price. Please adjust your price range!')
        else: 
            st.write('Sorry we do not have wines in that price range')
            
# Blank line
st.write('')

# Recommendation based on country
st.write('Option C: You are looking for a wine from a specific country? Please choose your desired country:')

# Create expandable field
with st.beta_expander("Option C: Recommendations based on country"):
    unique_countries = sorted(wine['country'].unique())
    selected_country = st.selectbox('Choose a country:', unique_countries)
    wine_country_filtered = wine[wine['country'] == selected_country]
    # Give desired output for country
    if not wine_country_filtered.empty:
        recom14 = wine_country_filtered[wine_country_filtered['points'] > 87]
        sample_size = min(len(recom14), 5)
        recom15 = recom14.sample(n=sample_size)
        recom15 = recom15.sort_values(by='points', ascending = False)
        index_list_12 = []
        i = 1
        for x in range(len(recom15)):
            index_list_12.append(i)
            i += 1
        recom15_index = pd.Series(index_list_12, dtype="int64")
        recom15.set_index(recom15_index, inplace = True)
        recom16 = recom15[["title", "variety", "winery", "price", "points"]]
        st.write('Here are some wine recommendations from the selected country:')
        st.write(recom16)
    else:
        st.write('Sorry, we do not have wines from that country.')
        
# Blank Line
st.write('')

# Option D: Individual Search
st.write('Option D: If you are looking for a more individual search, click on the following button to get filters for price, country and variety:')

# Create expandable field
with st.beta_expander("Option D: Individual Choice"):
    st.write('Please choose your desired filters:')
    
    # Input fields for min and max price
    col1, col2 = st.beta_columns(2)
    min_price_input = col1.text_input('Min Price', key='min_price_input_individual').replace(',', '.')
    max_price_input = col2.text_input('Max Price', key='max_price_input_individual').replace(',', '.')
 
    
    # Filter countries based on selected variety and price range
    top_wines = wine[wine['points'] > 91]
    unique_varieties = sorted(top_wines['variety'].unique())
    if min_price_input and max_price_input:
        min_price = float(min_price_input)
        max_price = float(max_price_input)
        wine_filtered = wine[(wine['price'].between(min_price, max_price)) &
                             (wine['points'] > 91)]
        unique_filtered_varieties = sorted(wine_filtered['variety'].unique())
      
    # Dropdown menu for variety
    selected_variety = st.selectbox('Choose a variety:', unique_filtered_varieties, key = 'selected_country_individual')
        
    # Filter countries based on selected variety and price range
    if min_price_input and max_price_input:
        min_price = float(min_price_input)
        max_price = float(max_price_input)
        wine_filtered = wine[(wine['price'].between(min_price, max_price)) &
                             (wine['variety'] == selected_variety) &
                             (wine['points'] > 91)]
        unique_filtered_countries = sorted(wine_filtered['country'].unique())
    else:
        unique_filtered_countries = unique_countries
    
    # Dropdown menu for country
    selected_country = st.selectbox('Choose a country:', unique_filtered_countries, key='selected_country_individual')
    
    # Button to show recommendations
    if st.button('Show Recommendations', key='individual_choice_button'):
        if min_price_input and max_price_input:
            min_price = float(min_price_input)
            max_price = float(max_price_input)

            wine_filtered = wine[(wine['price'].between(min_price, max_price)) & 
                                 (wine['country'] == selected_country) &
                                 (wine['variety'] == selected_variety)]

            recom_wine = wine_filtered[wine_filtered['points'] > 91]

            if not recom_wine.empty:
                sample_size = min(len(recom_wine), 5)
                recom_wine_sample = recom_wine.sample(n=sample_size)
                recom_wine_sample = recom_wine_sample.sort_values(by='points', ascending=False)

                index_list = []
                i = 1
                for x in range(len(recom_wine_sample)):
                    index_list.append(i)
                    i += 1

                recom_wine_sample_index = pd.Series(index_list, dtype="int64")
                recom_wine_sample.set_index(recom_wine_sample_index, inplace=True)

                recom_wine_results = recom_wine_sample[["title", "variety", "winery", "price", "points"]]

                st.write('Here are some wine recommendations based on your chosen filters:')
                st.write(recom_wine_results)
            else:
                st.write('Sorry, we do not have wines that match your selected filters.')
st.write('')
st.write('Option E: Search for wines by entering text:')
with st.beta_expander("Option E: Search by wine name"):
    search_query = st.text_input('Enter a wine name or keyword:')
    if search_query:
        wine_search_results = wine[wine['title'].str.contains(search_query, case=False)]
        if not wine_search_results.empty:
            wine_titles = wine_search_results['title'].tolist()
            selected_wine_title = st.selectbox('Select a wine:', wine_titles)
            selected_wine = wine_search_results[wine_search_results['title'] == selected_wine_title]
            display_wine = selected_wine[["title", "points", "price"]]
            st.write(display_wine)
        else:
            st.write('No wines found with the given search query.')

