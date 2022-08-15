import pandas as pd
import matplotlib.pyplot as plt


def show_data(data:pd.DataFrame):
    ax = plt.axes(projection='3d')
    # Data for three-dimensional scattered points
    zdata = data['color'].apply(lambda x:x[2])
    ydata = data['color'].apply(lambda x:x[1])
    xdata = data['color'].apply(lambda x:x[0])
    d_color = data['color'].apply(lambda x:(x[0]/255,x[1]/255,x[2]/255)).values
    ax.scatter3D(xdata, ydata, zdata, s=data['freq']/100, c=d_color)
    plt.show()
