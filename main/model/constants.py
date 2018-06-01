gtfs_sql = {
    'routes': {
        'PK': ['route_id'],
        'types':{
            'route_type': 'INT'
        }
    },
    'trips': {
        'PK': ['trip_id'],
        'FK': [('route_id', 'routes(route_id)')],
    },
    'stops': {
        'PK': ['stop_id'],
        'types': {
            'stop_lat': 'Decimal(9,6)',
            'stop_lon': 'Decimal(9,6)'
        }
    },
    'transfers': {
        'FK': [('from_stop_id', 'stops(stop_id)'), ('to_stop_id', 'stops(stop_id)')],
        'types': {
            'min_transfer_time': 'INT'
        }
    },
    'stop_times': {
        'FK': [('stop_id', 'stops(stop_id)'), ('trip_id', 'trips(trip_id)')],
    }
}

def getFieldType(tableName, field):
    try: return gtfs_sql[tableName]['types'][field]
    except: return "TEXT"

def getPKStatements(tableName):
    try: return ["PRIMARY KEY (%s)" % (', '.join(gtfs_sql[tableName]["PK"]))]
    except: return [];

def getFKStatements(tableName):
    try: return list(map(lambda x: "FOREIGN KEY (%s) REFERENCES %s" % x, gtfs_sql[tableName]["FK"]))
    except: return [];

def getKStatement(tableName): return ', '.join(getPKStatements(tableName) + getFKStatements(tableName))

def getCreateTableOrder(): return ['routes', 'trips', 'stops', 'transfers', 'stop_times']
