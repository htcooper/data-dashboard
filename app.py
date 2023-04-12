import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

from pandas.api.types import (
    is_datetime64_any_dtype,
    is_object_dtype,
)

# Load the data
@st.cache_data
def load_data():
    # Read in csv
    df = pd.read_csv('raw_data.csv', header=0)
    return df

# Define cuisine types and item types
cuisine_types = {
    'Mexican': ['burrito', 'taco', 'quesadilla', 'pollo', 'carnitas', 'verde', 'rojo', 'carne'],
    'Japanese': ['sushi', 'ramen', 'udon', 'tempura', 'gyoza', 'poke', 'musubi', 'roll', 'miso', 'edamame'],
    'Chinese': ['egg roll', 'kung', 'spring roll', 'chinese', 'chow', 'drunken', 'fried rice', 'mongolian', 'orange chicken'],
    'American': ['burger', 'fries', 'hot dog', 'grilled cheese', 'mac', 'club', 'blt', 'melt', 'bbq', 'ribs', 'brisket', 'chips', 'fried chicken', 'wings', 'tenders'],
    'Asian': ['roll', 'kung', 'curry', 'thai', 'fried rice', 'tom kha', 'tom yum', 'dumpling', 'pho', 'potsticker', 'pad see'],
    'Italian': ['pizza', 'calzone', 'pasta', 'ravioli', 'spaghetti', 'penne', 'fettu', 'gnocchi', 'alfredo'],
    'Indian': ['curry', 'naan', 'saag', 'samosa', 'aloo', 'tikka', 'masala', 'vindaloo'],
    'Vegan': ['vegan'],
    'Mediterranean': ['hummus', 'kabob', 'shawarma', 'falafel', 'pita', 'gyro', 'mediterranean'],
    'Healthy': ['salad', 'healthy'],
    'Breakfast': ['breakfast burrito', 'breakfast', 'egg', 'hash', 'bagel', 'waffle', 'toast', 'pancakes'],
    'Drinks': ['coke', 'soda', 'boba', 'agua', 'water', 'ale', 'lemonade', 'sprite', 'pepsi', 'juice', 'bottle', 'horchata', 'lassi', 'latte', 'tea', 'coffee'],
    'Dessert': ['cake', 'ice cream', 'sundae', 'cookie', 'tiramisu', 'torte', 'tart'],
    'Combo Meals': ['combo', 'plate', 'dinner', 'meal']


}

item_types = {
    'burrito': 'burrito',
    'pizza': 'pizza',
    'chips': 'side',
    'burger': 'burgers',
    'fries': 'side',
    'chicken': 'chicken',
    
}

# Determine cuisine type and item type for each row
def get_cuisine_type_and_item_type(name):
    cuisine_type = None
    item_type = None
    
    for ct, its in cuisine_types.items():
        for it in its:
            if it in name.lower():
                cuisine_type = ct
                item_type = item_types.get(it)
                break
        if cuisine_type:
            break
    
    return cuisine_type, item_type



### START ###

df = load_data()

st.sidebar.subheader('View Cuisine Trends')

# Create new columns for cuisine type and item type
df[['cuisine_type', 'item_type']] = df['name'].apply(get_cuisine_type_and_item_type).apply(pd.Series)

# Preview data
# print(df.head())

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
    'Combo Meals': '#F7ECE1' # linen
    
}

# Define item types and colors
item_colors = {
     'burrito': '#4daf4a',
     'drinks': '#377eb8',
     # add more
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

# Define filters
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
selected_filter = st.sidebar.radio('Select a Date or a Day of the Week', ['Date', 'Day of Week'])
if selected_filter == 'Date':
    selected_date = st.sidebar.date_input("Select a date", value=df['date'].min(), min_value=df['date'].min(), max_value=df['date'].max())
    filtered_data = df.loc[df['date'] == str(selected_date)]
else:
    selected_day = st.sidebar.selectbox('Select a day of the week', days)
    filtered_data = df.loc[df['date'].apply(lambda x: pd.Timestamp(x).day_name()) == selected_day]

selected_cuisine_types = st.sidebar.multiselect('Select cuisine types', options=cuisine_types)

# Create copy of data for cuisine type filter
ct_filtered_data = filtered_data.copy()

# Filter data based on the selected filters
ct_filtered_data = filtered_data.loc[filtered_data['cuisine_type'].isin(selected_cuisine_types)]

# Aggregate data by cuisine type and hour of day
agg_data = ct_filtered_data.groupby(['cuisine_type', 'hour']).agg({'requested_orders': 'sum'}).reset_index()

# Create plot
ct_fig = px.line(agg_data, x='hour', y='requested_orders', color='cuisine_type', color_discrete_map=cuisine_colors, markers=True)

# Update layout of plot
if selected_filter == 'Date':
    title = f'Cuisine Trends for {selected_date}'
else:
    title = f'Cuisine Trends for {selected_day}s'
ct_fig.update_layout(
    title=title,
    xaxis_title='Hour of Day',
    yaxis_title='Total Requested Orders',
    legend_title='Cuisine Type',
    width=800,
    height=500,
    margin=dict(l=50, r=50, t=50, b=50),
    hovermode='x'
)
# Display  plot
st.plotly_chart(ct_fig)

## Show top items by time of day and day of week

def show_top_items():
    # Group the data by time of day and item name
    grouped_df = ct_filtered_data.groupby(['hour', 'name'], as_index=False).agg({'requested_orders': 'sum'})
    hour = st.sidebar.selectbox("Select hour of day", range(24))
    
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

    selected_top_number = st.sidebar.radio('Select Number of Top Items to View', [5, 10])
    
    # Choose number of top items to view
    if selected_top_number == 5:
        top_items = grouped_df.groupby('hour', as_index=False).apply(lambda x: x.nlargest(5, 'requested_orders'))
        
    else:
        top_items = grouped_df.groupby('hour', as_index=False).apply(lambda x: x.nlargest(10, 'requested_orders'))

    data = top_items[top_items['hour'] == hour]
    fig_hour = go.Figure(data=[go.Bar(x=data['name'], y=data['requested_orders'], marker_color='orange')])  
    fig_hour.update_layout(title=f'Top {selected_top_number} items for Hour {hour} ({hour_name[hour]})', xaxis_title='Item', yaxis_title='Requested Orders')
    st.plotly_chart(fig_hour, use_container_width=True)


# Allow user to choose whether to drill down on top items
if st.sidebar.checkbox('View Top Items by Hour', False):
    show_top_items()


