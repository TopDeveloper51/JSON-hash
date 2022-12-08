import json
from black import Dict

#Get file from API
#API: response = requests.get("https://...")
#main_api = 'https://...'


def hash_and_find(value):
    return "implement it"


def copy(value):
    return value


def hash(value):
    return f"fakehash-----{value}"


def require(value):
    return value


CONFIG_OPTION_TO_FUNC_MAP = {
    "hash": hash,
    "copy": copy,
    "required": require,
    "hash&find": hash_and_find,
}


class Anonimizer:
    def __init__(self):
        hash_list = []

    def anonimize_dict(self, config_dict: Dict, source_dict: Dict) -> Dict:
        out_dict = {}
        for key, value in config_dict.items():
            func_to_perform = CONFIG_OPTION_TO_FUNC_MAP.get(value, None)
            if func_to_perform is None:
                raise Exception(
                    f"Invalid value in config!{value} is not valid config value."
                )
            try:
                initial_value = source_dict[key]
            except KeyError:
                raise Exception(
                    f"Key {key} exists in config but not found in source file!"
                )

            out_value = func_to_perform(initial_value)
            out_dict[key] = out_value

        return out_dict

    def anonimize_file(
        self, config_filename: str, source_filename: str, output_filename: str
    ):
        config_dict = None
        source_dict = None

        with open(config_filename, "r") as cfg_file:
            config_dict = json.load(cfg_file)

        with open(source_filename, "r") as src_file:
            source_dict = json.load(src_file)

        out_dict = self.anonimize_dict(config_dict, source_dict)
        with open(output_filename, "w+") as out_file:
            json.dump(out_dict, out_file)
