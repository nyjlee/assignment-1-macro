import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel("Macrodata.xlsx")

# Format the 'Period' column as DD-MM-YYYY and set the 'Period' column as the index
df['Period'] = pd.to_datetime(df['Period'])
df['Period'] = df['Period'].dt.strftime('%d-%m-%Y')
df.set_index('Period', inplace=True)

#Set up variables
inf = df['CPI Domestic']
inf_f = df['CPI Foreign']
unemp = df['Unemployment']
int = df['Domestic ST interest rate']
int_f = df['Foreign ST interest rate']
rex = df['EUR/USD']

print(rex)

