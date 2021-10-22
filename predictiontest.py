# line plot of time series
from matplotlib import pyplot
from pandas import read_csv
from statsmodels.tsa.arima.model import ARIMA
import numpy
from statsmodels.datasets import sunspots
from statsmodels.tsa.deterministic import CalendarTimeTrend


series = read_csv('noodlesbones.csv', header=0, index_col=0)
split_point = len(series) - 0
dataset, validation = series[0:split_point], series[split_point:]
print('Dataset %d, Validation %d' % (len(dataset), len(validation)))
dataset.to_csv('dataset.csv', index=False)
validation.to_csv('validation.csv', index=False)

# load dataset
series = read_csv('dataset.csv', header=0)
print(type(series))
# seasonal difference
X = series.values
# fit model
model = ARIMA(X)
model_fit = model.fit()
# print summary of fit model
print(model_fit.summary())

forecast = model_fit.forecast()[0]
print('Forecast: %f' % forecast)