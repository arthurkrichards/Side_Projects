#Libraries needed for this visualization and modeling
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



def create_pie_chart(data, title, figsize=(15, 15)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.pie(data, labels=data.index, autopct=autopct_format(data.values), startangle=90)
    ax.axis('equal')
    plt.title(title)
    return fig





#tax
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{pct:.1f}%\n(£{val:,})'
    return my_format

def calculate_after_tax(salary, tax_rate=0.35):
    return salary * (1 - tax_rate)






# Currency Conversion Rate which is currently as stated, would need to change in future potentially
gbp_to_aed_rate = 4.68  

# Sidebar for Currency Selection
st.sidebar.header("Currency Selection")
selected_currency = st.sidebar.selectbox("Choose the currency", ["GBP", "AED"])

def convert_currency(amount, rate):
    return amount * rate if selected_currency == "AED" else amount









# Streamlit App Title
st.title("Compensation Package Visualization")

# Constants
fund_size = 150e6  # £150 million
expected_multiple = 2.0
carry_interest_rate = 0.05 # 5%
annualization_years = 8
tax_rate = 0.35 # 35% tax rate

# Sidebar for Current Compensation
st.sidebar.header("Current Compensation")
tax_rate = st.sidebar.slider("Tax Rate for Base Salary", min_value=0.0, max_value=1.0, value=0.35, step=0.01, format="%.2f")  
base_current = st.sidebar.number_input("Base Salary", value=175000)
bonus_current = st.sidebar.number_input("Bonus", value=100000)




#####
#####
#####

# Calculations for Current Compensation
# Took into account the tax rate 
after_tax_base = calculate_after_tax(base_current, tax_rate)
total_return = fund_size * expected_multiple
profit = total_return - fund_size
carried_interest = profit * carry_interest_rate
annualized_carry = carried_interest / annualization_years



#####
#####
#####





# Current Compensation DataFrame
current_data = {
    'Base Salary After Tax': after_tax_base,
    'Bonus': bonus_current,
    'Carried Interest': annualized_carry
}
current_df = pd.DataFrame(list(current_data.items()), columns=['Component', 'Amount'])
current_total = sum(current_df['Amount'])

# Separator for ease of reading on stakeholder
st.sidebar.markdown("---")  

# Dropdown for Payout option, in the event we do not want to do an immediate payout, an option would be created to model payouts after probationary period.
equity_option = st.sidebar.selectbox("Equity & Carried Interest Payout Option", ["Yes", "No"])

# Interactive Widgets for Offer
st.sidebar.header("Offer Details")
offer_base = st.sidebar.number_input("Base for Offer", value=int(after_tax_base * 1.20))
offer_bonus = st.sidebar.number_input("Bonus for Offer", value=int(offer_base * 1.50))
offer_equity = st.sidebar.number_input("Equity for Offer", value=100000)

# Separator
st.sidebar.markdown("---")  # This creates a horizontal line

# Editable Allowances
flight_cost = st.sidebar.number_input("Flight Cost", value=600)
relocation_cost = st.sidebar.number_input("Relocation Cost", value=15000)
education_cost = st.sidebar.number_input("Education Cost", value=50000)
housing_allowance = st.sidebar.number_input("Housing Allowance", value=100000)


# Prepare New Offer DataFrame
new_offer_data = {
    'Base Salary': offer_base,
    'Bonus': offer_bonus,
    'Other Allowances': flight_cost * 4 + education_cost * 2 + relocation_cost + housing_allowance
}
# For Payout
if equity_option == "Yes":
    new_offer_data['Equity'] = offer_equity
    new_offer_data['Annualized Carry'] = annualized_carry


new_offer_df = pd.DataFrame(new_offer_data.items(), columns=['Component', 'Amount'])

# Totals
new_offer_total = new_offer_df['Amount'].sum()




#To convert from British Pounds to Dirham

if selected_currency == "AED":
    current_total = convert_currency(current_total, gbp_to_aed_rate)
    new_offer_total = convert_currency(new_offer_total, gbp_to_aed_rate)
    current_df['Amount'] = current_df['Amount'].apply(lambda x: convert_currency(x, gbp_to_aed_rate))
    new_offer_df['Amount'] = new_offer_df['Amount'].apply(lambda x: convert_currency(x, gbp_to_aed_rate))


# Prepare data for Current Compensation Table
current_comp_table_data = {
    'Component': ['Base Salary', 'Allowances', 'Bonus', 'Total Compensation'],
    'Amount': [
        after_tax_base, 
        0,  # Assuming no allowances in current compensation
        bonus_current, 
        current_total
    ]
}

# Prepare data for New Offer Table
new_offer_table_data = {
    'Component': [
        'Base Salary', 'Allowances', 'Bonus', 'Total Compensation',
        'Relocation', 'Education', 'Housing', 'Sign On', 'Total Package'
    ],
    'Amount': [
        offer_base, 
        flight_cost * 4 + education_cost * 2 + housing_allowance, 
        offer_bonus, 
        new_offer_total,
        relocation_cost, 
        education_cost, 
        housing_allowance, 
        offer_equity if equity_option == "Yes" else 0, 
        new_offer_total + (relocation_cost + education_cost + housing_allowance + (offer_equity if equity_option == "Yes" else 0))
    ]
}

# Convert to DataFrame
current_comp_table_df = pd.DataFrame(current_comp_table_data)
new_offer_table_df = pd.DataFrame(new_offer_table_data)

# Display Tables
st.write("Current Compensation Breakdown Table")
st.table(current_comp_table_df)

st.write("New Offer Compensation Breakdown Table")
st.table(new_offer_table_df)



currency_symbol = "£" if selected_currency == "GBP" else "AED"
# Displaying Pie Charts with increased size
st.write("Current Compensation Breakdown")
current_pie_chart = create_pie_chart(current_df.set_index('Component')['Amount'], "Current Compensation", figsize=(12, 12))
st.pyplot(current_pie_chart)

st.write(f"New Offer Compensation Breakdown - {equity_option}")
new_offer_pie_chart = create_pie_chart(new_offer_df.set_index('Component')['Amount'], f"New Offer Compensation - {equity_option}", figsize=(12, 12))
st.pyplot(new_offer_pie_chart)
####
####



