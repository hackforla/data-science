from ..domain import trafficsign as ts


class Properties():

    def __init__(self):
        pass

    def transform_json_(self, json_dict):
        sub_json_ = json_dict["features"]
        new_json_list = []
        for collection in range(len(sub_json_)):
            try:
                accuracy = sub_json_[collection]['properties']['accuracy']
                altitude = sub_json_[collection]['properties']['altitude']
                direction = sub_json_[collection]['properties']['direction']
                first_seen_at = sub_json_[collection]['properties']['first_seen_at']
                last_seen_at = sub_json_[collection]['properties']['last_seen_at']
                key = sub_json_[collection]['properties']['key']
                layer = sub_json_[collection]['properties']['layer']
                value = sub_json_[collection]['properties']['value']
                coordinates = sub_json_[collection]['geometry']['coordinates']
                geometry_type = sub_json_[collection]['geometry']['type']
                traffic_sign = ts.TrafficSign(accuracy, altitude, direction, 
                                            first_seen_at, last_seen_at, key, 
                                            layer, value, coordinates, 
                                            geometry_type)
                new_json_list.append(traffic_sign.to_dict())
            except Exception:
                pass
        return new_json_list

            
