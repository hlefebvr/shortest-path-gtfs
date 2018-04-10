from math import sin, cos, sqrt, atan2, radians;

def distance(lat1, lon1, lat2, lon2):
    lat1 = radians(float(lat1));
    lat2 = radians(float(lat2));
    lon1 = radians(float(lon1));
    lon2 = radians(float(lon2));
    R = 6373.0 # approximate radius of earth in km
    dlon = lon1 - lon2
    dlat = lat1 - lat2
    a = sin(dlat / 2)**2 + cos(lat2) * cos(lat1) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c;

def distance_to_center(lat, lon):
    return distance(lat, lon, 48.8610, 2.3439);
