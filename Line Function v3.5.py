import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates
import pandas as pd
import pandas_datareader.data as web
import numpy as np

def pct_change(first, second):
    return (second-first) / first*100.00

start = dt.datetime(2017, 5, 1)
end = dt.datetime(2017, 7, 30)
df = web.DataReader('MSFT', 'google', start, end)  # retrieving data from google

# df2 = pd.read_csv('D:\Folders\ArJuN\Coding\My Projects\Trading Algorithm\VEDL.txt', names = ['Date','Time','Open','High','Low', 'Close', 'Volume'])
# df2.index = df['Time']
# df2 = df2.drop('Time', axis=1)
# df2.shift(-1)
# print(df2.head())

high_1 = df['High'].max()
idx_1 = df['High'].idxmax()  # use this to get index in timestamp format
arrays = df.loc[idx_1:, 'High']  # this returns arrays starting from ts_idx_1 in df[High]
# skipdates = 10  this lets us skip index by the specified points in array.
arraysWskip = arrays[11:]  # returns array with keeping distance from the highest high 1

high_2 = 0

# this loops see whether the high 2 is below the specified percent change.
for i in arraysWskip:
    if pct_change(high_1, arraysWskip.max()) < -3.50:
        high_2 = i
        print('Found high_2 which is < -2.00 : ', high_2)
        print('high2 = ', high_2)
        idx_2 = arraysWskip[arraysWskip == high_2].index.tolist()[0]
        print('idx 2 = ', idx_2)
        # idx_2 = arraysWskip.idxmax()
        # =============Draws Line using x and y coordinates===============#
        idx = [idx_1, idx_2]
        # dates = [ts_idx_1, ts_idx_2]
        x = matplotlib.dates.date2num(idx)
        y = [high_1, high_2]
        Difference = x[1] - x[0]

        print('y1 = ', high_1)
        print('x1 = ', x[0])
        print('y2 = ', high_2)
        print('x2 = ', x[1])
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        # the np.linspace lets you set number of data points, line length.
        x_axis = np.linspace(x[0], x[1] + Difference, 3)  # linspace(start, end, num)
        y_axis = polynomial(x_axis)
        Predicted_Value = y_axis[2]
        print("Predicted_Value", Predicted_Value)

        plt.plot(x_axis, y_axis)
        plt.plot(x[0], y[0], 'go')
        plt.plot(x[1], y[1], 'go')
        loc = matplotlib.dates.AutoDateLocator()
        print("loc = ", loc)
        plt.gca().xaxis.set_major_locator(loc)
        plt.gca().xaxis.set_major_formatter(matplotlib.dates.AutoDateFormatter(loc))
        plt.gcf().autofmt_xdate()
        df['High'].plot()
        plt.grid('on')
        plt.show()
        break
    print("looping... i = ", i)
    # else: pass
print("Out of the loop!")