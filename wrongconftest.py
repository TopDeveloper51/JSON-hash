from black import Dict
import pytest

#Get file from API
#API: response = requests.get("https://...")
#main_api = 'https://...'

@pytest.fixture
def cfg() -> Dict:
    sample_config = {
        "Name": "required",
        "Surname": "required",
        "Age": "copy",
        "SecretNumber": "hash&find",
        "SecretAddress": "hash",
    }

    return sample_config


@pytest.fixture
def valid_input_with_all_functions() -> Dict:
    sample_config = {
        "Name": "Adam",
        "Surname": "Novak",
        "Age": "19",
        "SecretNumber": "1999999",
        "SecretAddress": "24214214",
    }

    return sample_config
