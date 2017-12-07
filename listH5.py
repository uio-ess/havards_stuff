import h5py
import matplotlib.pyplot as plt
import argparse


def visitFunction(name, obj, plotp, match):
    print(name)
    for key, val in obj.attrs.items():
        print('    ' + str(key) + ': ' + str(val))
    matching = True
    if(isinstance(match, str) and
       name.find(match) == -1):
        matching = False
    if(type(obj) == h5py._hl.dataset.Dataset and
       matching and
       plotp):
        print(obj)
        if(len(obj[:].shape) == 2):
            plt.matshow(obj[:])
            plt.colorbar()
            plt.show()
        if(len(obj[:].shape) == 1):
            dim = min(obj.len(), 3600)
            plt.plot(obj[0:dim])
            plt.show()


def top_level(fname, plotp, matching):
    with h5py.File('/tmp/image0.h5', 'r') as f:
        root = f.get('/')
        print('/')
        for key, val in root.attrs.items():
            print('    ' + str(key) + ': ' + str(val))
        f.visititems(lambda obj, name: visitFunction(obj, name, True, None))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List contents of HDF5 file. ')
    parser.add_argument('filename')
    parser.add_argument('-p', '--plot', action='store_true', default=False, help="Plot data")
    parser.add_argument('-m', '--match', default=None,
                        help="Print things where the full pathname contains MATCH")
    args = parser.parse_args()
    
    if(args.match):
        args.plot = True

    with h5py.File(args.filename, 'r') as f:
        root = f.get('/')
        print('/')
        for key, val in root.attrs.items():
            print('    ' + str(key) + ': ' + str(val))
        f.visititems(lambda obj, name: visitFunction(obj, name, args.plot, args.match))
