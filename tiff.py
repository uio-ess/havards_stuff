import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
import math

img = plt.imread('/home/dev/Downloads/2017-12-01-C13440_20CU-1000F16.tif')
plt.set_cmap('hot')
plt.matshow(img, vmin=100)
plt.colorbar()
plt.show()

counts = img.ravel()
filtered = counts[counts < 200]
print('sqrt(Variance): ' + str(math.sqrt(filtered.var())))
(mu, sigma) = norm.fit(filtered)

print(str(mu) + ', ' + str(sigma))
counts, bins, patches = plt.hist(img.ravel(), 50, (75, 125), normed=1)
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins+0.5, y)
plt.show()

plt.show()

#250/3.135
# img = plt.imread('/home/dev/Downloads/VimbaImage1msf16v2_0_01.tif')
# fig = plt.matshow(img)
# plt.clim(100, 150)
# plt.colorbar()
# plt.show()
