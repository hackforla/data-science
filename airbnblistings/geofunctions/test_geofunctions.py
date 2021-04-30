#!/usr/bin/env python3
"""tests for helperfunctions"""
import geofunctions as gf

def test_offset():
    """ test offset function"""
    assert gf.offset(37.335480, -121.893028, 500) == (37.33684902755619, -121.89130616517198) 
