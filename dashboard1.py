import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import plotly.io as pio
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Superstore!!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Sample Superstore EDA")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# Upload and read the CSV file
f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(f1)
else:
    # Provide a default path or use the uploaded file
    os.chdir(r'C:\Users\Fast Com Raiwind\Local Sites\wpfirst\conf\nginx\includes\New folder')
    df = pd.read_csv('supermarket_sales - Sheet1.csv', encoding='ISO-8859-1')

col1, col2 = st.columns((2))
df['Date'] = pd.to_datetime(df["Date"])

StartDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", StartDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

st.sidebar.header("Choose your filter:")

City = st.sidebar.multiselect("Pick your City", df["City"].unique())
if not City:
    df2 = df.copy()
else:
    df2 = df[df["City"].isin(City)]

# Create for gender
gender = st.sidebar.multiselect("Male or Female", df2["Gender"].unique())
if not gender:
    df3 = df2.copy()
else:
    df3 = df2[df2["Gender"].isin(gender)]

product_line = st.sidebar.multiselect("Choose Product", df3["Product line"].unique())
if not product_line:
    df4 = df3.copy()
else:
    df4 = df3[df3["Product line"].isin(product_line)]

filterd_df = df4

rating_df = filterd_df.groupby(by=["Product line"], as_index=False)["Rating"].sum()

with col1:
    st.subheader("Product wise Ratings:")
    fig = px.bar(rating_df, x="Product line", y='Rating', text=['{:,.2f}'.format(x) for x in rating_df['Rating']], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Country Wise Ratings:")
    fig = px.pie(filterd_df, values="Rating", names="City", hole=0.5)
    fig.update_traces(text=filterd_df['City'], textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

gender = df.groupby('Gender', as_index=False)['gross income'].sum()
filtered_df = df

cl1, cl2 = st.columns(2)

with cl1:
    with st.expander("Gender_ViewData"):
        st.write(gender.style.background_gradient(cmap="Blues"))
        csv = gender.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Gender.csv", mime='text/csv', help='click here to download CSV file')

with cl2:
    with st.expander("City_ViewData"):
        city = filtered_df.groupby(by='City', as_index=False)['gross income'].sum()
        st.write(city.style.background_gradient(cmap="Oranges"))
        csv = city.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="City.csv", mime='text/csv', help='click here to download CSV file')

# Add the 'month_year' and 'Date' columns for time series analysis
filterd_df["month_year"] = filterd_df['Date'].dt.to_period('M').astype(str)
linechart = filterd_df.groupby(['Date', 'month_year'], as_index=False)['gross income'].sum()

st.subheader('Time series Analysis')

fig2 = px.line(linechart, x="Date", y="gross income", labels={'gross income': 'Amount'}, height=500, width=1000, template='gridon')
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View data of time series"):
    # Display the DataFrame with a gradient background
    st.write(linechart.style.background_gradient(cmap='Blues'))

    # Convert DataFrame to CSV
    csv = linechart.to_csv(index=False).encode('utf-8')

    # Provide a download button for the CSV file
    st.download_button(
        label="Download Data",
        data=csv,
        file_name="Timeseries.csv",
        mime='text/csv'
    )
st.subheader("hierarichal view of gross income using treemap")
fig3 = px.treemap(filterd_df,path=['City','Gender','Product line'],values='gross income',hover_data=['gross income'],color='Product line')
fig3.update_layout(width = 800,height = 650)
st.plotly_chart(fig3,use_cotainer_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Invoice_id wise income summary:")

with st.expander("Summary_Table"):
    # Select a sample of 5 rows with specific columns
    df_sample = df[['Invoice ID', 'City', 'Product line', 'Unit price']].head(5)
    
    # Create a table figure using Plotly
    fig = ff.create_table(df_sample)
    
    # Display the table in Streamlit
    st.plotly_chart(fig, use_container_width=True)




data1 = px.scatter(filtered_df, x='gross income', y='Product line', size='Quantity')
data1.update_layout(
    title='Relationship between Product Line and Gross Income',
    titlefont=dict(size=20),
    xaxis=dict(title='Gross Income', titlefont=dict(size=19)),
    yaxis=dict(title='Product Line', titlefont=dict(size=19))
)
st.subheader('Relationship between Product Line and Gross Income')
st.plotly_chart(data1, use_container_width=True)