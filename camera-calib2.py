import h5py
import math
import scipy.constants
import matplotlib.pyplot as plt


def counts_per_second_per_mm_sq(h5f):
    data = h5f.get('data/images/CAM1/data')[:]
    counts = data.sum()
    print(counts)
    shutter_time = h5f.get('data/images/CAM1').attrs['acquire_duration']
    counts_per_second = counts / shutter_time
    area = data.shape[0] * data.shape[1] * 0.00375**2
    return(counts_per_second/area)


def photons_per_second_per_mm_sq(hf5):
    watts = hf5.get('data/powermeter/PM100/y_values')[:].mean()
    print(watts)
    wavelength = hf5.get('data/powermeter/PM100').attrs['wavelength']
    frequency = scipy.constants.c / (wavelength * 1e-9)
    photons_per_second = watts / (scipy.constants.h * frequency)
    area = math.pi * ((9.5/2)**2)
    return(photons_per_second/area)


darkCounts = 0
counter = 0.0
for trig in range(100):
    fname = '/home/dev/data/lab/2018-12-21-cam-calib/' + str(trig+1).zfill(16) + '-L660M4-0mA.h5'
    with h5py.File(fname, 'r') as h5f:
        darkCounts += counts_per_second_per_mm_sq(h5f)
        counter += 1.0

counts = []
photons = []
for trig in range(100):
    fname = '/home/dev/data/lab/2018-12-21-cam-calib/' + str(trig+1).zfill(16) + '-L660M4-350mA.h5'
    with h5py.File(fname, 'r') as h5f:
        counts.append(counts_per_second_per_mm_sq(h5f))
        photons.append(photons_per_second_per_mm_sq(h5f))

plt.hist(counts)
plt.show()
plt.hist(photons)
plt.show()


print('darkCounts')
print(darkCounts)
darkCounts = darkCounts/counter
print(darkCounts)


avgCount = sum(counts)/len(counts)
print(avgCount)
avgPhotons = sum(photons)/len(photons)
print(avgPhotons)
print(avgPhotons/avgCount)

print(avgPhotons/(avgCount - darkCounts))
