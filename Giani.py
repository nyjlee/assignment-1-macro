import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy import signal
from statsmodels.tsa.api import VAR
from scipy.optimize import root
from numpy.linalg import inv

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
#plt.show()

#Not sure if constant should be added
result_1 = adfuller(inf, regression='ct')

# Extracting test statistics and p-value
adf_statistic = result_1[0]
p_value = result_1[1]

# Printing test results
print('Inflation:')
print("ADF Statistic:", adf_statistic)
print("p-value:", p_value)

result_2 = adfuller(int, regression='ct')

# Extracting test statistics and p-value
adf_statistic = result_2[0]
p_value = result_2[1]

# Printing test results
print('Interest Rates:')
print("ADF Statistic:", adf_statistic)
print("p-value:", p_value)

result_3 = adfuller(unemp, regression='ct')

# Extracting test statistics and p-value
adf_statistic = result_3[0]
p_value = result_3[1]

# Printing test results
print('Unemployment:')
print("ADF Statistic:", adf_statistic)
print("p-value:", p_value)

dataset = pd.DataFrame()
dataset["dCPI"] = inf - inf.shift(1)
dataset["dint"] = int - int.shift(1)
dataset["dump"] = unemp - unemp.shift(1)
dataset = dataset[1:]

dataset["dCPIs"] = signal.detrend(dataset["dCPI"])
dataset["dints"] = signal.detrend(dataset["dint"])
dataset["dumps"] = signal.detrend(dataset["dump"])
#print(dataset)


plt.figure(figsize=(16,10))
plt.subplot(211)
plt.plot(dataset['dCPI'],label='observed')
plt.plot(dataset['dCPIs'],label='detrended')
plt.xlabel('Date')
plt.ylabel('CPI')
plt.title('CPI')
plt.grid()
plt.subplot(212)
plt.plot(dataset['dint'],label='observed')
plt.plot(dataset['dints'],label='detrended')
plt.xlabel('Date')
plt.ylabel('Interest Rates')
plt.title('Interest Rates')
plt.grid()
#plt.show()

X = dataset.loc[:,["dCPIs","dints"]].copy()

model = VAR(X)
print(model.select_order(12, trend='n').summary())

results = model.fit(8, trend='n')
roots = results.roots

print(results.summary())

all_stable = all(np.abs(root) > 1 for root in roots)
if all_stable:
    print("The VAR model is stable.")
else:
    print("The VAR model is not stable.")

XLAG = pd.DataFrame()

num_lags = 8
for i in range(1,num_lags+1):
    XLAG = pd.concat([XLAG,X.shift(i).add_suffix("-"+str(i))],axis=1)
    
#change names to frames that we modify    
X2 = X.iloc[num_lags:,:]
XLAG2 = XLAG.iloc[num_lags:,:]
num_vars = X2.shape[1]
num_obs = X2.shape[0]

X3 = np.array(X2)
XLAG3 = np.array(XLAG2)

Bhat = inv(XLAG3.T@XLAG3)@XLAG3.T@X3

print(results.coefs)
print(Bhat)