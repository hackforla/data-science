from mapillarywrapper.domain import trafficsign as ts 


def test_trafficsign_model_init():
    trafficsign = ts.TrafficSign(accuracy=0.89477366, altitude=41.56068,
                                 direction=117.38304,
                                 first_seen_at="2019-02-24T09:06:02.000Z",
                                 last_seen_at="2019-02-24T10:05:50.000Z",
                                 key="up3nwgj3sq92ndb1n2mx744a6u",
                                 layer="trafficsigns",
                                 value="information--general-directions--g1",
                                 coordinates=[-117.92518140142575,
                                              33.80102254820244],
                                 geometry_type="Point")
    assert trafficsign.accuracy == 0.89477366
    assert trafficsign.altitude == 41.56068
    assert trafficsign.direction == 117.38304
    assert trafficsign.first_seen_at == "2019-02-24T09:06:02.000Z"
    assert trafficsign.last_seen_at == "2019-02-24T10:05:50.000Z"
    assert trafficsign.key == "up3nwgj3sq92ndb1n2mx744a6u"
    assert trafficsign.layer == "trafficsigns"
    assert trafficsign.value == "information--general-directions--g1"
    assert trafficsign.coordinates == [-117.92518140142575, 33.80102254820244]
    assert trafficsign.geometry_type == "Point"


def test_trafficsign_from_dict():
    trafficsign = ts.TrafficSign.from_dict(
            {
                'accuracy': 0.89477366, 
                'altitude': 41.56068,
                'direction': 117.38304,
                'first_seen_at': "2019-02-24T09:06:02.000Z",
                'last_seen_at': "2019-02-24T10:05:50.000Z",
                'key': "up3nwgj3sq92ndb1n2mx744a6u",
                'layer': "trafficsigns",
                'value': "information--general-directions--g1",
                'coordinates': [-117.92518140142575,
                                33.80102254820244],
                'geometry_type': "Point"
                }
            )

    assert trafficsign.accuracy == 0.89477366
    assert trafficsign.altitude == 41.56068
    assert trafficsign.direction == 117.38304
    assert trafficsign.first_seen_at == "2019-02-24T09:06:02.000Z"
    assert trafficsign.last_seen_at == "2019-02-24T10:05:50.000Z"
    assert trafficsign.key == "up3nwgj3sq92ndb1n2mx744a6u"
    assert trafficsign.layer == "trafficsigns"
    assert trafficsign.value == "information--general-directions--g1"
    assert trafficsign.coordinates == [-117.92518140142575, 33.80102254820244]
    assert trafficsign.geometry_type == "Point"


def test_trafficsign_to_dict():
    traffic_dict = {
                'accuracy': 0.89477366, 
                'altitude': 41.56068,
                'direction': 117.38304,
                'first_seen_at': "2019-02-24T09:06:02.000Z",
                'last_seen_at': "2019-02-24T10:05:50.000Z",
                'key': "up3nwgj3sq92ndb1n2mx744a6u",
                'layer': "trafficsigns",
                'value': "information--general-directions--g1",
                'coordinates': (-117.92518140142575,
                                33.80102254820244),
                'geometry_type': "Point"
            }
    trafficsign = ts.TrafficSign.from_dict(traffic_dict)
    assert trafficsign.to_dict() == traffic_dict
