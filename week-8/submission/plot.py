import numpy as np
import matplotlib.pyplot as plt
def plot(value,policy):
    plt.figure(figsize=(12,6))

    plt.subplot(1,2,1)
    plt.contour(policy,levels = np.arange(-MAX_MOVE,MAX_MOVE+1),cmap='coolwarm')
    plt.colorbar(label='Overnight Bike Movement')
    plt.title('Policy Transfer Matrix')
    plt.xlabel('Location 2')
    plt.ylabel('Location 1')

    plt.subplot(1,2,1)
    plt.imshow(V,cmap='viridis',origin='lower')
    plt.colorbar(label='Value')
    plt.title('Value Function')
    plt.xlabel('Location 2')
    plt.ylabel('Location 1')

    plt.tight_layout()
    plt.show()