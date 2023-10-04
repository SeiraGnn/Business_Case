'''The following code is used for a showcase project of a fictional business case were you are asked to produce and Analytics Report comparing three different sales strategies for a company.''' 
'''It was created in a Jupyter notebook, so the results from running a cell inform the code from the next cell. I marked were the cells would start with comments.'''
'''For context on the case & code, please refer to the written report'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Data import and initial exploration
sales = pd.read_csv('product_sales.csv')

sales.info()
sales.head()

# New cell would start here:
# ---------- Data Validation ---------- 

# Week col
print('Week column range:', sales.week.min(),'-', sales.week.max(), '\n')

# Sales method
print('--- Sales method column ---')
invalid_sm = sales[~((sales['sales_method'] == 'Email')
                   | (sales['sales_method'] == 'Call')
                   | (sales['sales_method'] == 'Email + Call'))]
if invalid_sm.empty:
    print('No invalid entries found in sales_method')
else:
    print('Invalid sales_method entries:\n Index  Sales method')
    print(invalid_sm['sales_method'])

    
# Customer Id
'''Checks if the customer_id is 36 chars long and has hyphens in the correct places'''
def id_check(id):
    if (len(id) != 36):
        return True
    elif (id[8] != '-' or id[13] != '-' or id[18] != '-' or id[23] != '-'):
        return True
    else:
        return False
    
print('\n--- Customer Id column ---')
invalid_customerid = sales[sales['customer_id'].apply(id_check)]
                          
if invalid_customerid.empty:
    print('All customer IDs are 36 characters long and have hyphens in correct places')
    
else:
    print('Invalid customer IDs:\n Index   Customer ID')
    print(invalid_customerid['customer_id'])
    
# Number sold
print('\nnb_sold column range:', sales.nb_sold.min(),'-', sales.nb_sold.max(), '\n')

# Revenue
print('revenue column range:', sales.revenue.min(),'-', sales.revenue.max(), '\n')

# Years as customer
invalid_years = sales[(sales['years_as_customer'] < 0) | (sales['years_as_customer'] > 39)]

if invalid_years.empty:
    print('All values in the years_as_customer column are within acceptable range')
else:
    print('Invalid years:\n',invalid_years)

# Num of site visits
print('\nnb_site_visits col range:', sales.nb_site_visits.min(),'-', sales.nb_site_visits.max(), '\n')

# State
states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

invalid_states = sales[~sales['state'].isin(states)]

print('--- State column ---')
if invalid_states.empty:
    print('All entries in the state column match a US state')
    
else:
    print('Invalid states:\n Index   State')
    print(invalid_states['state'])
  
# New cell would start here:
# ----------  Data Cleaning ---------- 

# 3 columns need some cleaning. All other columns had no invalid entries and/or had reasonable ranges for the observations

# Corrects sales_method entries with different format
replacements =  {'em + call': 'Email + Call', 'email': 'Email'}
sales['sales_method'] = sales['sales_method'].replace(replacements)

# Drops the two invalid values for years as customer
sales = sales.drop(invalid_years.index)

# Impute mean of revenue by sales_method on missing values
mean_revenue_by_method = sales.groupby('sales_method')['revenue'].transform('median').round(2)

sales['revenue'].fillna(mean_revenue_by_method, inplace=True)

# New cell would start here:
# ---------- Exploratory Data Analysis ---------- 

# Overall spread of the revenue
plt.hist(sales['revenue'], bins=20)

plt.xlabel('Revenue')
plt.ylabel('Frequency')
plt.title('Overall revenue spread')

plt.savefig('revspread.png', dpi=100)

plt.show()

# New cell would start here:
# Distribution of revenue by sales approach. There's a lot of noise in the graph. A histogram segmented by sales approach will make it better.
email_method = sales[sales['sales_method'] == 'Email']
ec_method = sales[sales['sales_method'] == 'Email + Call']
c_method = sales[sales['sales_method'] == 'Call']

bins = int(np.sqrt(len(sales)))

plt.hist(email_method['revenue'], bins, label='Email', alpha=0.7)
plt.hist(ec_method['revenue'], bins, label='Email + Call', alpha=0.7)
plt.hist(c_method['revenue'], bins, label='Call', alpha=0.7)

#plt.ylim(0, 300)
plt.xlabel('Revenue')
plt.ylabel('Frequency')
plt.title('Distribution of revenue by sales approach')
plt.legend(loc='upper right')

plt.show()


# New cell would start here:
# Mean revenue by sales method
plt.figure()
sns.barplot(x='sales_method', y='revenue', data=sales, ci=None)

plt.xlabel('Sales method')
plt.ylabel('Mean revenue')
plt.title('Mean revenue by sales method')

plt.show()

# New cell would start here:
# Bar plot of num of customers by sales method. The histogram showed a hibher (sales) volume for the 'Email' category. Let's look at how much it really is.
dataframes = [email_method, ec_method, c_method]
labels = ['Email', 'Email + Call', 'Call']
lengths = [len(df) for df in dataframes]

sns.barplot(x=labels, y=lengths)

plt.xlabel('Sales Method')
plt.ylabel('Number of Customers')
plt.title('Number of customers by sales method')

plt.show()

# New cell would start here:
# Total sum of revenue by sales method. There's more sales made, but less avg revenue. Let's see who got the highest revenue in total.
erev = email_method['revenue'].sum().round()
ecrev = ec_method['revenue'].sum().round()
crev = c_method['revenue'].sum().round()

print(erev, ecrev, crev)

# New cell would start here:
# Revenue over time by sales method
sns.relplot(x='week', y='revenue', data=sales,
            kind='line',
            style='sales_method',
            hue='sales_method',
            markers=True,
            dashes=False,
            ci=None)

plt.xlabel('Weeks until sale, since product launch')
plt.ylabel('Mean revenue for the week')
plt.title('Revenue over time by sales method')

plt.gcf().set_size_inches(8, 6)
plt.show()

# New cell would start here:
# Average years of client's loyalty by sales method. Will a customer that has known us for several years be more willing to buy with just an impersonal Email approach?
avg_years_by_method = sales.groupby('sales_method')['years_as_customer'].mean()

avg_years_by_method

# New cell would start here:
# Relation between site visits and revenue
sns.relplot(x='revenue', y='nb_site_visits', data=sales,
            kind='scatter',
            hue='sales_method',
            alpha=0.5)

plt.title('Site Visits vs Revenue')
plt.xlabel('Revenue')
plt.ylabel('Num. of site visits')

plt.show()

# New cell would start here:
# Correlation between site visits and revenue
general_corr = sales.corr(method='pearson')

email_plus_call_corr = ec_method[['revenue', 'nb_site_visits']].corr(method='pearson')

print(general_corr)
print(email_plus_call_corr)

# New cell would start here:
# Business Metric to track. We will assume more prospect clients were reached by the only-email strategy and thus generated a higher total revenue. Assuming both methods are equally likely to produce a sale, we should focus on the AVG revenue instead, as our business metric.

print(email_method['revenue'].mean())
print(ec_method['revenue'].mean())
print(c_method['revenue'].mean())
