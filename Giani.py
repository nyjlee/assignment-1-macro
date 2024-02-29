import matplotlib.pyplot as plt
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

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df.index, inf, label='CPI Domestic')
plt.plot(df.index, unemp, label='Unemployment')
plt.plot(df.index, int, label='Domestic ST Interest Rate')

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Time Series of CPI Domestic, Unemployment, and Domestic ST Interest Rate')
plt.legend()
plt.show()

