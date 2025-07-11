import random
import datetime,time

# create random information about vehicles
def generate_vehicle_data(v_id):
    return {
        'vehicle_id': v_id,
        'lat': round(random.uniform(-90,90),6),
        'long': round(random.uniform(-180,180),6),
        'speed': round(random.uniform(0,200),2),
        'temperature': round(random.uniform(50,150),2),
        'humidity': round(random.uniform(10,90),2),
        'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')[:-3]
    }