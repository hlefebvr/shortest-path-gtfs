from math import sin, cos, sqrt, atan2, radians

def distance_to_center(lat, lon):
    R = 6373.0 # approximate radius of earth in km
    ref_lat = radians(48.8610)
    ref_lon = radians(2.3439)
    dlon = lon - ref_lon
    dlat = lat - ref_lat
    a = sin(dlat / 2)**2 + cos(ref_lat) * cos(lat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c;
