class TrafficSign():

    def __init__(self, accuracy: float, altitude: float, direction: float,
                 first_seen_at: str, last_seen_at: str, key: str, layer: str,
                 value: str, coordinates: list, geometry_type: str) -> None:
        self.accuracy = accuracy
        self.altitude = altitude
        self.direction = direction
        self.first_seen_at = first_seen_at
        self.last_seen_at = last_seen_at
        self.key = key
        self.layer = layer
        self.value = value
        self.coordinates = coordinates
        self.geometry_type = geometry_type

    @classmethod
    def from_dict(cls, adict: dict) -> None:
        """ returns an model object from a dictionary."""
        return cls(
                accuracy=adict['accuracy'],
                altitude=adict['altitude'],
                direction=adict['direction'],
                first_seen_at=adict['first_seen_at'],
                last_seen_at=adict['last_seen_at'],
                key=adict['key'],
                layer=adict['layer'],
                value=adict['value'],
                coordinates=adict['coordinates'],
                geometry_type=adict['geometry_type']
                )

    def to_dict(self) -> dict:
        """ returns a dictionary of the model TrafficSign"""
        return {
                'accuracy': self.accuracy,
                'altitude': self.altitude,
                'direction': self.direction,
                'first_seen_at': self.first_seen_at,
                'last_seen_at': self.last_seen_at,
                'key': self.key,
                'layer': self.layer,
                'value': self.value,
                'coordinates': self.coordinates,
                'geometry_type': self.geometry_type
                }
