import h5py
import statistics
import integrateImages
import math
import scipy.constants


def photonsPerCount(fname, aperture_area):
    """
    Assumption is: all light passing thourgh aperture hit the sensor
    aperture_area is in units of mm^2
    """
    with h5py.File(fname, 'r') as h5f:
        mean_power = h5f.get('meas1/PMVals/pmVals')[:].mean()
        print('Mean power is ' + str(mean_power))
        pm_radius = 9.5 * 0.5  # mm
        power_density = mean_power/(math.pi * pm_radius**2)
        print('Power per mm^2 is: ' + str(power_density))
        frequency = scipy.constants.c / (h5f.get('meas1/PMVals/').attrs['wavelength'] * 1e-9)
        photon_density = power_density / (scipy.constants.h * frequency)
        print('Photons per mm^2 per s is: ' + str(photon_density))
        sums, times = integrateImages.integrator(h5f, 'meas1/images/', False, False)
        image_mean = statistics.mean(sums)
        print('Mean counts per image is ' + str(image_mean))
        exposure_time = h5f.get('meas1/images/').attrs['exposure']
        photons_on_sensor = photon_density * aperture_area * exposure_time
        print('Number of photons on sensor: ' + str(photons_on_sensor))
        photons_per_count = photons_on_sensor/image_mean
        print('Photons per count: ' + str(photons_per_count))
        return(photons_per_count)


def lens_aper_area(focal_length, f_number):
    radius = 0.5 * focal_length / f_number
    return(math.pi * radius**2)


print('\n\n')
fname = '/var/data/lab/2017-11-13-OCL-camera-without-lens-calib.h5'
with h5py.File(fname, 'r') as h5f:
    sensor_area = (h5f.get('meas1/images/').attrs['sizeX'] *
                   h5f.get('meas1/images/').attrs['sizeY'] *
                   0.00375**2)
    photonsPerCount(fname, sensor_area)

print('\n\n')
photons_per_count = 0
fname = '/var/data/lab/2017-11-13-OCL-camera-with-lens-calib.h5'
with h5py.File(fname, 'r') as h5f:
    photons_per_count = photonsPerCount(fname, lens_aper_area(50, 11.0))


# Get relative transmissions of lens at different f-stops
fnames = ['/var/data/lab/2017-11-13-OCL-lens-PM-F11.h5',
          '/var/data/lab/2017-11-13-OCL-lens-PM-F56.h5',
          '/var/data/lab/2017-11-13-OCL-lens-PM-F28.h5',
          '/var/data/lab/2017-11-13-OCL-lens-PM-F20.h5']

for fname in fnames:
    with h5py.File(fname, 'r') as h5f:
        mean_power = h5f.get('meas1/PMVals/pmVals')[:].mean()
        f_num = h5f.get('meas1/').attrs['F-num']
        area = lens_aper_area(50.0, f_num)
        ppa = mean_power / area
        print('Power per mm**2 at F/' + str(f_num) + ': ' + str(ppa))


# Get photons per square mm in OCL
# 100nA, ex 0.01, distance 1170mm
# calculate photons per second on sensor


def photons_on_sensor(fname, sample, exposure_time):
    """
    Photons absorbed on sensor per second
    """
    with h5py.File(fname, 'r') as h5f:
        pathname = sample + '/images_ex' + str(exposure_time) + '/'
        sums, times = integrateImages.integrator(h5f, pathname, False, False)
        image_mean = statistics.mean(sums)
        exposure_time = h5f.get(pathname).attrs['exposure']
        photons = image_mean * photons_per_count
        photons_absorbed_per_second = photons/exposure_time
        print('Number on photons on camera per second: ' + str(photons_absorbed_per_second))
        return(photons_absorbed_per_second)


def photons_emitted(fname, sample, exposure_time, focal_length=50, f_number=2.0):
    """
    Photons emitted from sample per MeV
    """
    print('\nSample: ' + sample + ', exposure time = ' + str(exposure_time))
    with h5py.File(fname, 'r') as h5f:
        photons_absorbed = photons_on_sensor(fname, sample, exposure_time)
        current = h5f.get(sample).attrs['BeamCurrent']
        print('Current is ' + str(current * 1e9) + 'nA')

        aper_area = lens_aper_area(focal_length, f_number)
        two_pi_area = 1170**2 * math.pi * 2
        photons_emitted = two_pi_area * photons_absorbed / aper_area
        print('Photons emitted per second: ' + str(photons_emitted))
        protons_per_coloumb = 6.2415e18
        print('Photons emitted per proton: ' +
              str(photons_emitted/(protons_per_coloumb * current)))
        mevs_per_proton = 0.95
        deposited_energy = current * protons_per_coloumb * mevs_per_proton
        photons_per_mev = photons_emitted / deposited_energy
        print('Photons emitter per absorbed MeV ' + str(photons_per_mev))


photons_emitted('/var/data/ocl/2017-11-14-OCL-currentscan-100nA.h5', 'HV1', 0.01)
photons_emitted('/var/data/ocl/2017-11-14-OCL-currentscan-100nA.h5', 'FC', 0.01)
photons_emitted('/var/data/ocl/2017-11-14-OCL-currentscan-100nA.h5', 'HV1', 0.001)
photons_emitted('/var/data/ocl/2017-11-14-OCL-currentscan-100nA.h5', 'FC', 0.001)

print('Done!\n\n')

mev_to_joule = 1.60217662e-13
frequency = scipy.constants.c / (693 * 1e-9)
emittable_photons = mev_to_joule / (scipy.constants.h * frequency)
print('Max number of r-line photons a mev can excite: ' + str(emittable_photons))
