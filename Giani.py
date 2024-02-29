import matplotlib.pyplot as plt
import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel("Macrodata.xlsx")

# Convert the 'Period' column to datetime format and set it as the index
df['Period'] = pd.to_datetime(df['Period'])
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
plt.plot(df.index, int, label='Domestic Short-Term Interest Rate')

# Set ticks at every 2 years
plt.xticks(df.index[::8], df.index.strftime('%d-%m-%Y')[::8], rotation=45)

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Rates (%)')
plt.title('Time Series of CPI Domestic, Unemployment, and Domestic Short-Term Interest Rate')
plt.legend()
plt.show()

data = pd.DataFrame({'CPI Domestic': inf, 'CPI Foreign': inf_f, 'Unemployment': unemp,
                     'Domestic ST interest rate': int, 'Foreign ST interest rate': int_f,
                     'EUR/USD': rex})