def diff_h(h1, h2):
    def to_ms(str_hour):
        hms = str_hour.split(':');
        return int(hms[0]) * 3600 + int(hms[1]) * 60;
    def to_minutes(int_sec):
        return int_sec / 60
    ms1 = to_ms(h1);
    ms2 = to_ms(h2);
    delta = abs(ms1 - ms2);
    return to_minutes(delta);