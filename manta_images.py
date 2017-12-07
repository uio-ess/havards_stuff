import h5py
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

with h5py.File('/tmp/gain0/0000000000000000-M660L4.h5', 'r') as h5f:
    plt.set_cmap('hot')
    image = h5f.get('data/images/CAM1/data')[:]

    image = image

    plt.matshow(image, vmin=19, vmax=25)
    plt.colorbar()
    plt.show()

    counts = image.ravel()
    (mu, sigma) = norm.fit(counts)
    print(str(mu) + ', ' + str(sigma))

    counts, bins, patches = plt.hist(counts, 6, (19, 25), normed=1)

    print(counts)
    print(bins + 0.5)

    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins + 0.5, y)
    plt.show()



(45 - 16.9)/0.8
