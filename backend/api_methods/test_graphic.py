from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('agg')
import numpy as np


def gen_test_graphic() -> BytesIO:
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure(figsize=(6, 4))
    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sine Wave')

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()

    return figfile
