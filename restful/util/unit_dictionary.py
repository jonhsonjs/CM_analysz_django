# -*- coding: utf-8 -*-
import collections
import math


class Dictionary:
    # Metric and Imperial systems
    __metric_dict = {
        'E': 1000000000000000000,
        'P': 1000000000000000,
        'T': 1000000000000,
        'G': 1000000000,
        'M': 1000000,
        'k': 1000,
        'h': 100,
        'da': 10,
        None: 1,
        'd': .1,
        'c': .01,
        'm': .001,
        'μ': .000001,
        'n': .000000001,
        'p': .000000000001,
        'f': .000000000000001,
        'a': .000000000000000001
    }
    __imperial_dist_dict = {
        'lea': 190080,
        'mi': 63360,
        'fu': 7920,
        'ch': 792,
        'rod': 198,
        'yd': 36,
        'ft': 12,
        'li': 7.92,
        'in': 1,
        'th': .001
    }
    __imperial_vol_dict = {
        'gal': 128,
        'qt': 32,
        'pt': 16,
        'gi': 4,
        'floz': 1
    }
    __imperial_mass_dict = {
        't': 2240,
        'cwt': 112,
        'qr': 28,
        'qtr': 28,
        'st': 14,
        'lb': 1,
        'oz': .0625,
        'dr': .00390625,
        'gr': .00014285714
    }
    __digital_storage_dict = {
        'PB': math.pow(2, 53),
        'TB': math.pow(2, 43),
        'GB': math.pow(2, 33),
        'MB': math.pow(2, 23),
        'KB': math.pow(2, 13),
        'bytes': 8,
        'bit': 1
    }
    __digital_storage_dict_sorted = collections.OrderedDict(
        sorted(__digital_storage_dict.items(), key=lambda t: t[1], reverse=True))

    __time_dict = {
        'Ys': math.pow(10, 24),
        'Zs': math.pow(10, 21),
        'Es': math.pow(10, 18),
        'Ps': math.pow(10, 15),
        'Ts': math.pow(10, 12),
        'Gs': math.pow(10, 9),
        'yr': 31540000,
        'mo': 2628000,
        'Ms': math.pow(10, 6),
        'wk': 604800,
        'day': 86400,
        'hr': 3600,
        'ks': 1000,
        'min': 60,
        's': 1,
        'ds': .1,
        'cs': .01,
        'ms': .001,
        'µs': math.pow(10, -6),
        'ns': math.pow(10, -9),
        'ps': math.pow(10, -12),
        'fs': math.pow(10, -15),
        'as': math.pow(10, -18),
        'zs': math.pow(10, -21),
        'ys': math.pow(10, -24)
    }

    def metric_dict(self):
        return self.__metric_dict

    def imperial_dist_dict(self):
        return self.__imperial_dist_dict

    def imperial_vol_dict(self):
        return self.__imperial_vol_dict

    def imperial_mass_dict(self):
        return self.__imperial_mass_dict

    def digital_storage_dict(self):
        return self.__digital_storage_dict_sorted

    def time_dict(self):
        return self.__time_dict
