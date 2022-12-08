from wronganonimizer import Anonimizer
from unittest import TestCase

import pytest


def test_anonimizer_fixture(cfg: dict):
    assert cfg is not None


def test_anonimize_dict_raise_error_when_config_contains_invalid_key(
    valid_input_with_all_functions: dict,
):

    invalid_cfg = {
        "Name": "required",
        "Surname": "required",
        "Age": "copy",
        "SecretNumber": "INVALID_VALUE_FOR_CONFIG",
        "SecretAddress": "INVALID_VALUE_FOR_CONFIG",
    }
    anon = Anonimizer()
    with TestCase().assertRaises(Exception) as e:
        anonimized_dict = anon.anonimize_dict(
            config_dict=invalid_cfg, source_dict=valid_input_with_all_functions
        )
        print(anonimized_dict)
    assert (
        e.exception.__str__()
        == "Invalid value in config!INVALID_VALUE_FOR_CONFIG is not valid config value."
    )


def test_anonimize_dict_successful(cfg: dict, valid_input_with_all_functions: dict):

    anon = Anonimizer()
    anonimized_dict = anon.anonimize_dict(
        config_dict=cfg, source_dict=valid_input_with_all_functions
    )
    expected_dict = {
        "Age": "19",
        "Name": "Adam",
        "SecretAddress": "fakehash-----24214214",
        "SecretNumber": "implement it",
        "Surname": "Novak",
    }
    TestCase().assertDictEqual(expected_dict, anonimized_dict)
