import databaseAPI
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress

aircraftdata = databaseAPI.getdatafromsheet('Aircraft Reference Database')

def scatterplot():
    x = pd.to_numeric(aircraftdata['Max Payload (kg)'])
    y = pd.to_numeric(aircraftdata['MTOM (kg)'])

    #k, d, r, p, error = linregress(x, y)
    print(linregress(x, y))

    plt.scatter(x, y)

    #label each data point
    for i, txt in enumerate(aircraftdata['Aircraft Name']):
        plt.annotate(txt, (x[i], y[i]))
    plt.show()



scatterplot()