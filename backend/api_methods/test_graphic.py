from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np


def gen_test_graphic() -> BytesIO:
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sine Wave')

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # Move the cursor to the beginning of the BytesIO object
    plt.close()

    return figfile

