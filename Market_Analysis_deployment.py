import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns 
from PIL import Image # Import the Image module
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import PIL.Image

#data cleaning

def wrangle(file):
    
    # Import dataset
    df = pd.read_csv(file)
    
    # Drop 'index' and 'column1' column
    columns = ["index", "Column1"]
    
    # Cast 'Year' as type str
    df["Year"] = df["Year"].astype("string").str.split('.', expand=True)[0]
    
    # Change 'date' type from object to date
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Define age groups
    age_groups = {(0, 18): "0-18",(19, 30): "19-30",(31, 40): "31-40",(41, 50): "41-50",(51, 60): "51-60",(61, 70): "61-70",(71, float("inf")): "71 & above"}

    # Create a new column for age groups
    df['Age Group'] = df['Customer Age'].apply(lambda x: next((v for k, v in age_groups.items() if k[0] <= x <= k[1]), None))
    
    # Calculate Margin
    df["Margin"] = df["Revenue"] - df["Cost"]
    
    # Rename the Month Variable
    #df["Month"].replace({"January":"Jan", "February":"Feb", "March":"Mar", "April"}, inplace=True)
    #[, , , "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Change 'age' data type
    #df["Customer Age"] = df["Customer Age"].astype(str).str.split('.', expand=True)[0]
    
    # Drop coulmns
    df.drop(columns=columns, inplace=True)
    
    # Drop null values
    df.dropna(inplace=True)
    
    return df

df = wrangle("D:/My_Project/Market Analysis and Revenue Optimization/SalesForCourse_quizz_table/SalesForCourse_quizz_table.csv")




st.markdown("<h1 style='text-align: center; color:blue;'>Market Analysis and Revenue Optimization</h1>", unsafe_allow_html=True)

# Load the image from file
image = Image.open('D:/My_Project/Market Analysis and Revenue Optimization/SalesForCourse_quizz_table/amazondatanalysis-1024x497.jpg')

# Display the image
st.image(image, caption='Optional image caption', use_column_width=True)

st.markdown("<h3 style='text-align: left;'>Goals: </h3>", unsafe_allow_html=True)

st.write('* Analyzing customer demographics by countries and states to better target future marketing campaigns.')
st.write('* Tracking changes in customers’ spending habits over time for different product categories.')
st.write('* Identifying which product categories have the highest average revenue per sale to help prioritize resources for those products or services')


st.markdown("<h2 style='text-align: left;color:red'>-Distribution of the Demographic Data </h2>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: left;'>*What's the relationship between customers age and choice of product and sales? How does customer age impact product preferences and sales? </h6>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: left;'>Customers Age Distribution </h4>", unsafe_allow_html=True)


# Create age order
age_order = ["0-18", "19-30", "31-40", "41-50", "51-60", "61-70", "71 & above"]

# Create a sorting column
df['Sorte'] = df['Age Group'].map({age_group: index for index, age_group in enumerate(age_order)})

# Sort the DataFrame based on the sorting column
df_sorte = df.sort_values('Sorte')

# Plot a histogram of the customers age using plotly express
fig1 = px.histogram(df_sorte, x="Age Group", color_discrete_sequence=["lightgreen"], category_orders={'Age Group': age_order})
fig1.update_layout(bargap=0.3, title_text="Distribution of Customer Age", xaxis_title_text="Customer Age", yaxis_title_text="Count")

# Display the histogram in Streamlit
st.plotly_chart(fig1)


st.markdown("<h4 style='text-align: left;'>Distribution of Customers Gender </h4>", unsafe_allow_html=True)

# Bar plot of `Customers Gender`
fig2 = px.bar(df, x=df["Customer Gender"].value_counts().index, y=df["Customer Gender"].value_counts())
fig2.update_layout(
    bargap=0.8,
    xaxis_title="Gender",
    yaxis_title="Count",
    title="Customers Gender"
)
st.plotly_chart(fig2)

st.write('*The graph shows the number of male and female customers. It could be deduced that the number of male customers is slightly higher than female. The total number of male customers is 17805 (i.e. 0.51%)')


st.markdown("<h4 style='text-align: left;'>Distribution of Customers by Country </h4>", unsafe_allow_html=True)

# Bar plot of `Customers Country
fig3 = px.bar(df, x=df["Country"].value_counts().index, y=df["Country"].value_counts())
fig3.update_layout(
    bargap=0.5,
    xaxis_title="Country",
    yaxis_title="Count",
    title="Distribution of Customers by Country"
)
st.plotly_chart(fig3)

st.write('*The plot shows that more than half of the customers are from the United States with a percentage of 52%.')
st.write('#  18076/34566 = 0.522941  😛')


st.markdown("<h4 style='text-align: left;'>Distribution of Customers by State </h4>", unsafe_allow_html=True)

fig4 = px.histogram(df, x="State", color_discrete_sequence=["lightgreen"])
fig4.update_layout(
    bargap=0.2,
    title="Distribution of Customers by State",
    xaxis_title="State",
    yaxis_title="Count"
)
st.plotly_chart(fig4)

st.write('*Most of the customers stay in California, England, and Washington. 30% of the customers stay in California, 18% in England, and 15% in Washington. Take note that their customers are widespread.')


st.markdown("<h4 style='text-align: left;'>Get the product category counts </h4>", unsafe_allow_html=True)

product_category_counts = df["Product Category"].value_counts().to_frame()
st.dataframe(product_category_counts)



# Group the data frame by 'Age Group'
group_df = df.groupby("Age Group")["Product Category"].value_counts(normalize=True).rename("Count").to_frame().reset_index()

# Pivot the data
pivot_df = group_df.pivot("Age Group", "Product Category")

# Create heat map
heatmap = sns.heatmap(pivot_df, annot=False, cmap="YlGnBu", cbar=True)

# Get the Figure object from the heatmap
figure = heatmap.figure

# Display the heatmap in Streamlit
st.pyplot(figure)

st.write('*The heatmap shows the popularity of each Product Category among each Age Group. The row and column represent the age group and product category respectively. The color intensity signifies the level of preference for each product category. Based on the heatmap, customers of all age group buy more of accessories than other products in the Product Category.')



st.markdown("<h4 style='text-align: left;'>What is the Subcategory Preferences by Age Group? </h4>", unsafe_allow_html=True)

# Group data frame by 'Age Group'
group_df = df.groupby("Age Group")["Sub Category"].value_counts(normalize=True).rename("Count").to_frame().reset_index()
group_df.head()

# Create bar chart 
fig4 = px.bar(
    group_df,
    x="Sub Category",
    y= "Count",
    color = "Age Group", 
    barmode = "group",
    orientation="v",
    title="Products Preference by Age Group"
)

# Set axis labels
fig4.update_layout(xaxis_title="Sub Category", yaxis_title="Count")

st.plotly_chart(fig4)


st.write('''*The above bar chart is used to visualize how different age groups favored the subcategories. Only 31.8% of age group 19-30 purchase tires and tubes, 29.5% of customers in age group 31-40 favored tires and tubes (it has the lowest ratio in tires and tubes), 55.4% of customers age group 71 & above prefers tires and tubes (This group has the highest percentage in tires and tube).

For bottles and cages, the product is purchased mostly by customers in age group '51-60' (about 15.9% of the age group purchased it), the product is also commonly purchased by age group '41-50' (with a percentage of 15.7), and age group '19-30' (around 15.4%). The product is hardly purchased by customers that are 71 and above. Generally, bottles and cages are not so popular among all age groups.

The percentage of customers buying helmets is generally low and the percentages across all age groups are close.

In general, tires and tubes are favored by all age group while bike racks, bike stands, and vest are the least popular across all age group.''')



st.markdown("<h4 style='text-align: left;'>Compare the average unit price and quantity purchased by different age groups </h4>", unsafe_allow_html=True)
df_avg = df.groupby("Age Group").agg({"Unit Price":"mean", "Quantity":"mean"}).reset_index()
st.dataframe(df_avg)

st.markdown("<h4 style='text-align: left;'>Distribution of Age by Price </h4>", unsafe_allow_html=True)

fig5 = px.bar(df_avg, x='Age Group', y='Unit Price', color='Age Group',
             labels={'Age Group': 'Age Group', 'Unit Price': 'Average Unit Price'},
             title='Comparison of Average Unit Price by Age Group')
st.plotly_chart(fig5)

st.write('*The diagram represents the average unit price of the goods purchased by different age group. The customers between the age of 31-40 tend to buy higher priced goods compared to other age groups. The customers with the least purchasing power are within the age group 0-18 and 71 & above.')


st.markdown("<h4 style='text-align: left;'>Distribution of Age by Quantity </h4>", unsafe_allow_html=True)

fig6 = px.bar(df_avg, x='Age Group', y='Quantity', barmode='group')
st.plotly_chart(fig6)

st.write('''*On average, age group 41-50, 0-18, and 19-30 purchased more quantity though the quantity purchased by all age groups is approximately the same.

The two bar plots roughly show that age group 31-40 and 41-50 have the highest purchasing power in this particular market.''')

st.markdown("<h4 style='text-align: left;'>Distribution of Revenue by Age Group </h4>", unsafe_allow_html=True)

st.write('Lets examine the total revenue generated by different age group')

# Group revenue by age group and year
rev_by_age = df.groupby("Customer Age")['Revenue'].sum().reset_index()

# Create a Plotly.Express figure
fig7 = px.scatter(rev_by_age, x="Customer Age", y="Revenue",title="Total Revenue by Age")

# Show the figure
st.plotly_chart(fig7)

st.write('*The scatter plot shows the total revenue generated by different age group. Customers between the ages of 28-35 generate the highest revenue while customers between the ages of 65 and 89 contribute the least revenue.')



st.markdown("<h4 style='text-align: left;'>Examine the total revenue generated by different age group in 2015 and 2016 </h4>", unsafe_allow_html=True)

# Group revenue by age group and year
revenue_by_age = df.groupby(["Age Group", "Year"])['Revenue'].sum().reset_index()

# Create a Plotly.Express figure
fig8 = px.line(revenue_by_age, x="Age Group", y="Revenue", color="Year", title="Total Revenue Generated by Age Groups")

# Show the figure
st.plotly_chart(fig8)

st.write('''*The line plot shows the total revenue generated by different age group in 2015 and 2016. In 2015, age group 19-30 generated the highest level of revenue followed by age group 31-40. The age group 31-40 generated the highest revenue in 2016, followed by age group 19-30. Also, notice that there's a drop in the total revenue by age group 19-30. Customers between the age of 0-18 and 71 & above have a low revenue and it's almost the same for the two years.''')

st.markdown("<h4 style='text-align: left;'>How does customers interact with products based on age and gender?</h4>", unsafe_allow_html=True)

st.write("Using bar chart visualize the likely relationship between age, gender, and choice of product")

# Group the data by age and gender
df_group = df.groupby(["Age Group", "Customer Gender"])["Product Category"].value_counts(normalize=True).rename("Count").to_frame().reset_index()

# Calculate the proportions of purchases by age, gender, and category
pivot_df = df_group.pivot_table(index="Age Group", columns=["Customer Gender", "Product Category"], values="Count")

# Create the bar chart
fig9, ax = plt.subplots(figsize=(10, 10))
pivot_df.plot(kind='bar', rot=0, ax=ax)

ax.set_xlabel('Age Group')
ax.set_ylabel('Proportion of Purchases')
ax.set_title('Product Preferences by Age and Gender')

ax.legend(title='Gender', bbox_to_anchor=(1, 1))

st.pyplot(fig9)

st.write('*In age group 0-18, the percentage of male purchasing accessories and clothing is slightly higher than female, more female tend to buy bikes than male. In age group 19-30, the same male and female customers appear to prefer clothing and bike, the fraction of female customers that prefers accessories is a bit higher than male. In age group 31-40, more male prefer accessories, the proportion of female that go for bikes is higher, and male has a higher preference in clothing.')


st.markdown("<h4 style='text-align: left;'>Profitability Assessment</h4>", unsafe_allow_html=True)

st.write('*To obtain the Mean Margin, the dataframe is grouped using both the Product Category and Sub Category and aggregated using mean. The products are sorted in descending order based on the mean margin and the top 5 products with the highest average marginal value are selected.')


# Lets group and calculate mean margin
avg_margin_by_product = (df.groupby(["Product Category", "Sub Category"])["Margin"]
                          .mean()
                          .sort_values(ascending=False)
                          .to_frame()
                          .reset_index()
                         )
st.write('Lets print the top 5 product which had a better margin')
st.dataframe(avg_margin_by_product.head(5))
st.write('Lets print the bottom 5 product which had a worse margin')
st.dataframe(avg_margin_by_product.tail(5))


st.write('Create horizontal bar chart')
fig11 = px.bar(
    avg_margin_by_product.sort_values(by="Margin", ascending=False),
    x="Margin",
    y="Sub Category",
    #color = "Product Category",
    orientation="h",
    title="Mean Margin by Sub Category"
)
# Set axis labels
fig11.update_layout(xaxis_title="Product Margin", yaxis_title="Sub Category")
st.plotly_chart(fig11)


st.write('*The graph represents products that have the highest average margins. These products also indicate better profitability for the company. Based on the information above, Bike Racks has the highest profitability.')


st.markdown("<h4 style='text-align: left;'>What is the Revenue Trend?</h4>", unsafe_allow_html=True)

# Sort df by date
df_sort = df.sort_values("Date")

# Plot the revenue trend
fig12, ax = plt.subplots(figsize=(10,8))
sns.lineplot(x="Date", y="Revenue", data=df_sort, marker="o")
ax.set_xlabel("Date")
ax.set_ylabel("Revenue")
ax.set_title("Revenue Trends Over Time")

# Display the plot in Streamlit
st.pyplot(fig12)

st.write('''*The plot shows the trend in revenue over time. There's a general downward trend in the graph, starting from the second quarter of the first year. The revenue was high between 2015-01 and 2015-05 but declined towards the end of 2015-06. In july 2016, we can notice a great reduction in revenue. These changes may be caused due to a number of factors. There's a need to identify potential areas for revenue optimization and explore strategies to boost growth. Generally, the graph shows that the business has been performing poorly over time.''')



st.markdown("<h4 style='text-align: left;'>Monthly Revenue Generated By Year</h4>", unsafe_allow_html=True)


#Filter data frame by year
year1 = df[df["Year"]=="2015"]
year2 = df[df["Year"]=="2016"]
# Create a month order list and reindex
months_order = ['January', 'February', 'March', 'April',  'May', 'June', 'July', 'August',
       'September', 'October', 'November', 'December']
# Group data by month 
monthly_rev2015 = (year1.groupby('Month')['Revenue'].sum()/1e6).reindex(months_order).reset_index()
monthly_rev2016 = (year2.groupby('Month')['Revenue'].sum()/1e6).reindex(months_order).reset_index()
# Plot a lineplot to make comparison
fig13, ax = plt.subplots(figsize=(10,8))
sns.lineplot(x="Month", y="Revenue", data=monthly_rev2015, marker="d", label="2015")
sns.lineplot(x="Month", y="Revenue", data=monthly_rev2016, marker="d", label="2016")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (in millions)")
ax.set_title("Revenue Trend for 2015 and 2016")
ax.legend(loc='upper left')
st.pyplot(fig13)


st.write('''*The line plot represents the revenue generated by the organization over the months. In the 2015 revenue chart, we could see that the organization started experiencing a substantial increase in revenue from July and had their peak in December. Based on the data, the organization had a significant decrease in revenue in July 2016.

Note: Revenue is the total amount of money a company earns from the sales of goods and services, that is, inflow of cash or other assets from the comapny's primary operations''')



st.markdown("<h4 style='text-align: left;'>Compare Different Markets by Unit Price and Revenue</h4>", unsafe_allow_html=True)

st.write('Average Revenue Generated by Market')

# Create a Pie Chart
labels = ['France', 'Germany', 'United Kingdom', 'United States']
sizes = df.groupby("Country")["Revenue"].mean()
colors = ["lightblue", "gray", "saddlebrown", "rosybrown"]
# pull is given as a fraction of the pie radius
fig14 = go.Figure(data=[go.Pie(labels=labels, values=sizes ,pull=[0, 0.2, 0, 0])])
# Display the pie chart in Streamlit
st.plotly_chart(fig14)


st.markdown("<p>Average Unit Price of Product by Market</p>", unsafe_allow_html=True)


price_group = df.groupby(["Country", "Product Category"])["Unit Price"].mean().reset_index()

# Creating the bar chart using Seaborn
fig15, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Country", y="Unit Price", hue="Product Category", data=price_group)

# Adding labels and title to the chart
plt.xlabel("Country")
plt.ylabel("Mean Unit Price")
plt.title("Comparison of Mean Unit Price by Country")
plt.legend()

# Displaying the chart in Streamlit
st.pyplot(fig15)


st.write(''' *The above chart shows the average unit price of various markets (i.e. countries) by products. In Germany, the three product categories have higher price than other countries. Though United States has the largest market share (in terms of population) the mean unit price and average revenue is lower than that of Germany.

Let's examine the likely factors influencing the price of products in Germany and United States by considering the customers' age, gender, and sub product distribution across the two markets.''')




st.markdown("<h4 style='text-align: left;'>Compare the Markets with the highest and lowest Revenue and Price</h4>", unsafe_allow_html=True)


st.write('Compare the distribution of age group  and Gender in the United States and Germany')

# Filter the data
us_age = df[df["Country"]=="United States"]["Age Group"].value_counts(normalize=True)
us_gen = df[df["Country"]=="United States"]["Customer Gender"].value_counts(normalize=True)
ger_age = df[df["Country"]=="Germany"]["Age Group"].value_counts(normalize=True)
ger_gen = df[df["Country"]=="Germany"]["Customer Gender"].value_counts(normalize=True)

# Create subplots and plot the age and gender distribution
fig16 = make_subplots(rows=2, cols=2,
                    shared_yaxes=True, 
                    subplot_titles=("US: Customer Age", "US: Customer Gender", "Germany: Customer Age", "Germany: Customer Gender"))
fig16.add_trace(go.Bar(x=us_age.index, y=us_age.values, marker=dict(color=us_age.values, coloraxis="coloraxis")), 1, 1)
fig16.add_trace(go.Bar(x=us_gen.index, y=us_gen.values, marker=dict(color=us_gen.values, coloraxis="coloraxis")), 1, 2)
fig16.add_trace(go.Bar(x=ger_age.index, y=ger_age.values, marker=dict(color=ger_age.values, coloraxis="coloraxis")),  2, 1)
fig16.add_trace(go.Bar(x=ger_gen.index, y=ger_gen.values, marker=dict(color=ger_gen.values, coloraxis="coloraxis")),  2, 2)
fig16.update_layout(coloraxis=dict(colorscale="Bluered_r"), showlegend=False)

# Displaying the chart in Streamlit
st.plotly_chart(fig16)


st.write('''The above chart shows the average unit price of various markets (i.e. countries) by products. In Germany, the three product categories have higher price than other countries. Though United States has the largest market share (in terms of population) the mean unit price and average revenue is lower than that of Germany.

Let's examine the likely factors influencing the price of products in Germany and United States by considering the customers' age, gender, and sub product distribution across the two markets.''')



st.markdown("<h4 style='text-align: left;'>Lets visualize the distribution of the sub categories by country</h4>", unsafe_allow_html=True)


# Group data by sub category
cat_by_price = df.groupby("Sub Category")["Unit Price"].mean()

# Create line plot using Seaborn
sns.set_style("darkgrid")
fig17, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=cat_by_price.index, y=cat_by_price.values, marker="d", color="g")

# Label the plot
plt.xlabel("Sub Category")
plt.ylabel("Average Unit Price")
plt.title('Average Unit Price by Sub Category')
plt.xticks(rotation=90)

# Display the plot in Streamlit
st.pyplot(fig17)



st.write('''This is a graphical representation of the average unit price of each product of the sub categories. From the graph, the first five products with the highest average unit price are; Mountain bikes, Touring bikes, Bike racks, Road bikes, and Shorts. Note that all the three products in Bikes category (under Product Category) are in the top five products with the highest price.

Also, the products with the lowest average price are; Bottles and cages, Caps, Cleaners, Socks, and Tires and tubes. Bottles and cages, cleaners, tire and tubes are all major products in Accessories (Under Product Category).''')























