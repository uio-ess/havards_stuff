import h5py
import matplotlib.pyplot as plt
import os


def normalize(array):
    summed = array.sum()
    return(array / summed)


def get_sum_of_spctra(path):
    # fiber_path = '/var/data/lab/2017-12-12-mirrortest/fiber/'
    files = os.listdir(path)
    fname = files.pop()
    y_data = None
    x_data = None
    length = 0
    with h5py.File(path + fname, 'r') as h5f:
        x_data = h5f.get('data/spectra/CCS1/x_values')[:]
        length = x_data.size
        y_data = h5f.get('data/spectra/CCS1/y_values')[:length]
    for hdf in files:
        with h5py.File(path + hdf, 'r') as h5f:
            y_data = h5f.get('data/spectra/CCS1/y_values')[:length] + y_data
    return(x_data, y_data)


x_dark, y_dark = get_sum_of_spctra('/var/data/lab/2017-12-12-mirrortest/dark/')


def get_pedestal_removed_normalized(path):
    x_data, y_data = get_sum_of_spctra(path)
    y_data = y_data - y_dark
    return(x_data, normalize(y_data))


x_fiber, y_fiber = get_pedestal_removed_normalized('/var/data/lab/2017-12-12-mirrortest/fiber/')
x_silver, y_silver = get_pedestal_removed_normalized('/var/data/lab/2017-12-12-mirrortest/silver/')
x_alu, y_alu = get_pedestal_removed_normalized('/var/data/lab/2017-12-12-mirrortest/alu/')
x_gold, y_gold = get_pedestal_removed_normalized('/var/data/lab/2017-12-12-mirrortest/gold/')
x_die, y_die = get_pedestal_removed_normalized('/var/data/lab/2017-12-12-mirrortest/dielectric/')

fig, ax = plt.subplots()
ax.plot(x_fiber, y_fiber, label='fiber')
ax.plot(x_silver, y_silver, label='silver')
ax.plot(x_gold, y_gold, label='gold')
ax.plot(x_alu, y_alu, label='alu')
ax.plot(x_die, y_die, label='dielectric')
legend = ax.legend(loc='upper left', shadow=True)
plt.show()


max_length = x_fiber.size - 100

fig, ax = plt.subplots()
ax.plot(x_fiber[1000:max_length], y_fiber[1000:max_length]/y_fiber[1000:max_length], label='fiber')
ax.plot(x_fiber[1000:max_length], y_silver[1000:max_length]/y_fiber[1000:max_length], label='silver')
ax.plot(x_fiber[1000:max_length], y_alu[1000:max_length]/y_fiber[1000:max_length], label='alu')
ax.plot(x_fiber[1000:max_length], y_gold[1000:max_length]/y_fiber[1000:max_length], label='gold')
ax.plot(x_fiber[1000:max_length], y_die[1000:max_length]/y_fiber[1000:max_length], label='dielectric')
legend = ax.legend(loc='lower left', shadow=True)
plt.show()
