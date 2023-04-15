import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

from pandas.api.types import (
    is_datetime64_any_dtype,
    is_object_dtype,
)

st.set_page_config(page_title='Cuisine Trends', page_icon='🍴', layout="wide", initial_sidebar_state="expanded")

# Load and cache the data
@st.cache_data
def load_data():
    df = pd.read_csv('raw_data.csv', header=0)
    return df

# Determine cuisine type based on keyword
def get_cuisine_type(name):
    cuisine_types = []

    if any(keyword.lower() in name.lower() for keyword in ["Roll", "Kung", "Sushi", "Curry", "Thai", "Fried Rice", "Tom Kha", "Dumplings", "Pho", "Potstickers", "Pad See", "tofu", 'bharta', 'mein', 'rangoons']):
        cuisine_types.append("Asian")

    if any(keyword.lower() in name.lower() for keyword in ["Egg Roll", "Kung", "Spring Roll", "Chinese", "Chow", "Drunken", "Fried Rice", "Mongolian", "Orange Chicken", 'lo mein', 'rangoons', 'honey walnut', 'wonton']):
        cuisine_types.append("Chinese")

    if any(keyword.lower() in name.lower() for keyword in ["pizza", "Calzone", "Pasta", "Ravioli", "Spaghetti", "Penne", "Lasagna", "Gnocchi", "Fettuc", "Alfredo", "tortellini", 'cacio', 'cannoli', 'linguin', 'burrata', 'italian', 'tagliat', 'meatball', 'farfalle', 'calamari']):
        cuisine_types.append("Italian")

    if any(keyword.lower() in name.lower() for keyword in ["Pasta", "Spaghetti", "Penne", "Lasagna", "Gnocchi", "Ravioli", "Fettuc", "Alfredo", 'farfalle', 'linguin', 'cacio']):
        cuisine_types.append("Pasta")

    if any(keyword.lower() in name.lower() for keyword in ["Curry", "Naan", "Paneer", "Saag", "Samosa", "Aloo", "Tikka", "Masala", "Vindaloo", "basmati", 'bharta', 'daal', 'jasmine', 'biryani', 'gulub', 'dal', 'korma', 'pakora']):
        cuisine_types.append("Indian")

    if "pizza" in name.lower():
        cuisine_types.append("Pizza")

    if "burrito" in name.lower():
        cuisine_types.append("Burritos")

    if "poke" in name.lower():
        cuisine_types.append("Poke")

    if "taco" in name.lower():
        cuisine_types.append("Tacos")

    if "soup" in name.lower():
         cuisine_types.append("Soup")

    if "vegan" in name.lower():
        cuisine_types.append("Vegan")

    if any(keyword.lower() in name.lower() for keyword in ["carne", "pollo", "carnitas", "quesadilla", "verde", "taco", "burrito", 'nachos', 'refried', 'fajita']):
        cuisine_types.append("Mexican")
        
    if any(keyword.lower() in name.lower() for keyword in ["Hummus", "Shawarma", "Greek", "Pita", "Gyro", "Kabob", 'kebob', "Falafel", "Mediterranean", 'babaganoush']):
        cuisine_types.append("Mediterranean")

    if any(keyword.lower() in name.lower() for keyword in ["Burger", "Slider", "Steak", "Fried Chicken", "Hot Dog", "Brat", "Cheesesteak", "Grilled Cheese", "Club", "BLT", "Melt", "BBQ", 'ribs', "Sandwich", 'mac', 'brisket', 'baked potato', 'smashmouth', 'reuben', 'baked beans', 'dog']):
        cuisine_types.append("American")

    if any(keyword.lower() in name.lower() for keyword in ["Roll", "Ramen", "Sushi", "Tempura", "Gyoza", "Musubi", "Edamame", "Miso", 'nigiri', 'sashimi', 'shishito']):
        cuisine_types.append("Japanese")

    if any(keyword.lower() in name.lower() for keyword in ["Breakfast", "Egg", "Hash", "Bagel", "Waffle", "Toast", "Pancakes", 'omelette', 'bacon', 'donut', 'sausage', 'croissant']):
        cuisine_types.append("Breakfast")

    if any(keyword.lower() in name.lower() for keyword in ["Chicken", "Wing", "Tenders", "Nuggets"]):
        cuisine_types.append("Chicken")

    if any(keyword.lower() in name.lower() for keyword in ['fries', "Bread", "Tots", "Rings", "Chips", "Sticks", "Coleslaw", "Knots", "Side", "White Rice", "Extra", "Edamame", "Guacamole", "Salsa", "Dip", "Hash Browns", "Chips", "Soy Sauce", 'baked potato', 'babaganoush', 'wasabi', 'greens', 'rice', 'funyun', 'baked beans']):
        cuisine_types.append("Sides")

    if any(keyword.lower() in name.lower() for keyword in ["Juice", "Coke", "Soda", "Agua", "Water", "Ale", "Lemonade", "Sprite", "Pepsi", "Bottle", "Horchata", "Lassi", "Coffee", "Tea", "Latte", "Boba", 'san pellegrino', 'smoothie', 'cappu', 'limona']):
        cuisine_types.append("Drinks")

    if any(keyword.lower() in name.lower() for keyword in ["Coffee", "Tea", "Latte", "Boba", 'cappu', 'espresso']):
        cuisine_types.append("Coffee and Tea")

    if any(keyword.lower() in name.lower() for keyword in ["Combo", "Plate", "Dinner", "Meal", "build"]):
        cuisine_types.append("Combo Specials")

    if any(keyword.lower() in name.lower() for keyword in ["Burger", "Slider", 'smashmouth']):
        cuisine_types.append("Burgers")

    if any(keyword.lower() in name.lower() for keyword in ["Acai", "Salad", "Healthy", "Fruit", "Fresh"]):
        cuisine_types.append("Healthy")

    if any(keyword.lower() in name.lower() for keyword in ["Cake", "Ice Cream", "Sundae", "Cookie", "Tiramisu", "Chocolate", 'oreo', 'cannoli', 'brownie', 'fudge', 'reese']):
        cuisine_types.append("Dessert")

        # Return the list of cuisine types
    return cuisine_types if len(cuisine_types) > 0 else ["Unknown"]

# Make sure a list is returned
def extract_cuisine_types(cuisine_type_str):
    if cuisine_type_str is None or cuisine_type_str == "":
        return []
    return cuisine_type_str

### CUISINE TRENDS BY DAY/DATE ###

df = load_data()

with st.sidebar.expander('👇  How to use this chart', expanded=False):
    st.write("This chart allows you to view cuisine trends and top items by the day of the week or by a specific date.")
    st.write(" Once you have made your date/day and cuisine selections, click the View Top Items by Hour checkbox to see the top items for a selected hour.")
    st.write("Your selections for day/date and cuisine type(s) will apply to both the trend chart and the top items chart and can be updated at any time.")

st.sidebar.subheader('View Cuisine Trends')

# Create new column for cuisine type
df["cuisine_label"] = df["name"].apply(get_cuisine_type)

# Extract the cuisine types so that everything is in a list format
df["cuisine_types"] = df["cuisine_label"].apply(extract_cuisine_types)

# Make copy of unexploded dataframe for use in top items section to avoid double-counting
df_unexploded = df.copy()

# Create new rows for items with more than one cuisine type
df = df.explode("cuisine_types")

# Define cuisine types and colors
cuisine_colors = {
    'Mexican': '#AA222D', # auburn red
    'Japanese': '#C3D898', # tea green
    'American': '#090C9B', # duke blue
    'Italian': '#FFF370', # maise yellow
    'Chinese': '#DA4450', # amaranth
    'Asian': '#FFC170', # earth yellow
    'Indian': '#6A66A3', # ultra violet
    'Mediterranean': '#0D6E6A', # caribbean current 
    'Vegan': '#A7D111', # yellow green
    'Healthy': '#FC6DAB', # hot pink
    'Breakfast': '#EC8209', # tangerine
    'Drinks': '#73C2BE', # tiffany blue
    'Dessert': '#853894', # eminence
    'Combo Meals': '#F7ECE1', # linen
    'Pasta': '#DBBBF5', # lavender
    'Burritos': '#DA95A2', # puce pink
    'Poke': '#EF2D56', # crayola red
    'Pizza': '#B8336A', # raspberry
    'Chicken': '#F3C98B', # sunset orange
    'Soup': '#314272', # Marian Blue
    'Tacos': '#FF9F1C', # orange peel
    'Burgers': '#9C0D38', # claret
    'Coffee and Tea': '#625141', # umber
    'Sides': '#F87666', # bittersweet orange
    'Unknown': '#FDFFFC' # baby powder white
    
}

# Convert columns to datetime where necessary
for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

# Create list of cuisine types
cuisine_list = df['cuisine_types'].sort_values().unique().tolist()

# Define filters
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
selected_filter = st.sidebar.radio('Select a Date or a Day of the Week', ['Day of Week', 'Date'], horizontal=True)
if selected_filter == 'Date':
    selected_date = st.sidebar.date_input("Select a date", value=df['date'].min(), min_value=df['date'].min(), max_value=df['date'].max())
    filtered_data = df.loc[df['date'] == str(selected_date)]
    unex_filtered_data = df_unexploded.loc[df_unexploded['date'] == str(selected_date)]  # for top items
else:
    selected_day = st.sidebar.selectbox('Select a day of the week', days)
    filtered_data = df.loc[df['date'].apply(lambda x: pd.Timestamp(x).day_name()) == selected_day]
    day_count = filtered_data.date.unique().size    # to calculate mean across days
    unex_filtered_data = df_unexploded.loc[df_unexploded['date'].apply(lambda x: pd.Timestamp(x).day_name()) == selected_day]  # for top items

selected_cuisine_types = st.sidebar.multiselect('Select cuisine types', options=cuisine_list, default='Breakfast')

# Filter data based on selected cuisine types
ct_filtered_data = filtered_data.loc[filtered_data['cuisine_types'].isin(selected_cuisine_types)]
filtered_unex_df = unex_filtered_data[unex_filtered_data['cuisine_types'].apply(lambda x: any(cuisine in x for cuisine in selected_cuisine_types))] # for top items

# if date is selected, show sum of orders, if day of week is selected, show mean
if selected_filter == 'Date':
    agg_data = ct_filtered_data.groupby(['cuisine_types', 'hour']).agg({'requested_orders': 'sum'}).reset_index()
    ct_fig = px.line(agg_data, x='hour', y='requested_orders', color='cuisine_types', color_discrete_map=cuisine_colors, markers=True)
    
else:
    #agg_data_1 = ct_filtered_data.groupby(['hour', 'cuisine_types']).agg({'requested_orders': 'sum'}).reset_index()
    #print(agg_data_1)
    agg_data = ct_filtered_data.groupby(['cuisine_types', 'hour']).apply(lambda x: x['requested_orders'].sum()/day_count).reset_index()
    #print(agg_data)
    agg_data.rename(columns={0: 'requested orders'}, inplace=True)
    #print(agg_data)
    ct_fig = px.line(agg_data, x='hour', y='requested orders', color='cuisine_types', color_discrete_map=cuisine_colors, markers=True)

# Create plot
#ct_fig = px.line(agg_data, x='hour', y=0, color='cuisine_types', color_discrete_map=cuisine_colors, markers=True)

# Update layout of plot
if selected_filter == 'Date':
    title = f'Cuisine Trends for {selected_date} (Sum)*'
    yaxis_title='Requested Orders (Sum)'
else:
    title = f'Cuisine Trends for {selected_day}s (Mean)*'
    yaxis_title='Requested Orders (Mean)'

ct_fig.update_layout(
    title=title,
    xaxis_title='Hour of Day',
    yaxis_title=yaxis_title,
    legend_title='Cuisine Type Legend',
    autosize=True,
    hovermode='x',
    legend=dict(
    orientation="h",
    yanchor="top",
    y=-.35,
    xanchor="right",
    x=1,
    bordercolor="white",
    borderwidth=.5
    )   
)

# Display  plot
st.plotly_chart(ct_fig, use_container_width=True)

### TOP ITEMS BY HOUR OF DAY ###

def show_top_items():
    
    # Repeat filtering with unexploded data
    if selected_filter == 'Date':
        hourly_items = filtered_unex_df.groupby(['name', 'hour'])['requested_orders'].sum().reset_index()
        yaxis_title='Requested Orders (Sum)'
    else:
        hourly_items = filtered_unex_df.groupby(['name', 'hour']).apply(lambda x: x['requested_orders'].sum()/day_count).reset_index()
        hourly_items.rename(columns={0: 'requested_orders'}, inplace=True)
        yaxis_title='Requested Orders (Mean)'

    hour = st.sidebar.selectbox("Select hour of day", range(24))
    
    # For people who have trouble with military time
    hour_name = {
        0: 'Midnight',
        1: '1 am',
        2: '2 am',
        3: '3 am',
        4: '4 am',
        5: '5 am',
        6: '6 am',
        7: '7 am',
        8: '8 am',
        9: '9 am',
        10: '10 am',
        11: '11 am',
        12: 'Noon',
        13: '1 pm',
        14: '2 pm',
        15: '3 pm',
        16: '4 pm',
        17: '5 pm',
        18: '6 pm',
        19: '7 pm',
        20: '8 pm',
        21: '9 pm',
        22: '10 pm',
        23: '11 pm'
    }

    # Choose how many top items to view
    selected_top_number = st.sidebar.radio('Select Number of Top Items to View', [5, 10, 15], horizontal=True)
    
    if selected_top_number == 5:
        top_items = hourly_items.groupby('hour', as_index=False).apply(lambda x: x.nlargest(5, 'requested_orders'))

    elif selected_top_number == 10:
        top_items = hourly_items.groupby('hour', as_index=False).apply(lambda x: x.nlargest(10, 'requested_orders'))  
        
    else:
        top_items = hourly_items.groupby('hour', as_index=False).apply(lambda x: x.nlargest(15, 'requested_orders'))

    data = top_items[top_items['hour'] == hour]
    fig_hour = go.Figure(data=[go.Bar(x=data['name'], y=data['requested_orders'], marker_color='#c929b6')])  
    fig_hour.update_layout(title=f'Top {selected_top_number} items for Hour {hour} ({hour_name[hour]})*', xaxis_title='Item Name', yaxis_title=yaxis_title)
    st.plotly_chart(fig_hour, use_container_width=True)
    st.write("\* Note that if a date is selected, the chart will display the sum of requested orders. If the day of week is selected, the chart will display the mean/average of orders on that day of the week.")


# Allow user to choose whether to drill down on top items
if st.sidebar.checkbox('View Top Items by Hour', False):
    show_top_items()


