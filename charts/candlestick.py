from pylab import *
import matplotlib.pyplot as plt
from datetime import datetime
import time
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY
from matplotlib.finance import candlestick,\
     plot_day_summary, candlestick2
import csv

# Parsing function
def parsing(line):
	return (date2num(datetime.strptime(line['Date'], "%Y-%m-%d")), 
		float(line['Open']),
		float(line['Close']),
		float(line['High']),
		float(line['Low']))

# Create an empty list
Prices = list()

# Load csv file.
with open("spy.csv") as F:
	for line in csv.DictReader(F):
		Prices.append(parsing(line)) # Parsing the data

# The following code is from http://matplotlib.org/examples/pylab_examples/finance_demo.html
mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays    = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d %Y')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12
 
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
candlestick(ax, Prices, width=0.6)

ax.xaxis_date()
ax.autoscale_view()
plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()