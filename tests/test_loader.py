import pytest
from blue.loader import jsonify
import os


pets_yaml = \
"""
cats:
 - meow
 - scratch
dog: indy
"""


@pytest.fixture
def jsonify_setup(pets_yaml=pets_yaml):
    with open('_temp.yaml', 'w') as f:
        f.write(pets_yaml)
    pet_json = jsonify('_temp.yaml')
    os.remove('_temp.yaml')
    return pet_json


def test_jsonify(jsonify_setup):
    assert jsonify_setup['dog'] == 'indy'
