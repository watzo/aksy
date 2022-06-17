from contextlib import closing

from aksy.device import Devices


def get_sampler_name():
    with closing(Devices.get_instance('mock_z48', 'mock')) as z48:
        print(f'hello {z48.systemtools.get_sampler_name()}!')

    with closing(Devices.get_instance('z48', 'usb')) as z48:
        print(f'hello real {z48.systemtools.get_sampler_name()}!')


if __name__ == "__main__":
    get_sampler_name()
