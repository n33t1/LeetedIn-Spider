import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))
import pytest
from utils.IEParser import IEParser 

event = [{'event_title': 'AtCoder',
  'events': [{'addtionalInfo': u'Participate: All ; Rated: All',
              'duratoin': 110,
              'endDateTime': 1531608600,
              'name': 'AtCoder Grand Contest 026',
              'registrationDeadline': 1531602000,
              'startDateTime': 1531602000,
              'url': 'https://agc026.contest.atcoder.jp'}]}]
              
testIEParser = IEParser(event)

def test_calc_event_length_1():
    assert testIEParser.calc_event_length(0, 3600) == 60

def test_calc_event_length_2():
    assert testIEParser.calc_event_length(1531602000, 1531608600) == 110

# Edge Case: Duration of 0
def test_calc_event_length_e1():
    with pytest.raises(Exception):
        testIEParser.calc_event_length(1531602000, 1531602000)