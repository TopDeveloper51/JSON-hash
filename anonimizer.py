from black import Dict
import hashlib
import json

config_data = {}
source_data = {}

with open('config.json') as config_file:
    config_data = json.load(config_file)

with open('source.json') as source_file:
    source_data = json.load(source_file)

class Anonimazer:
    def __init__(self, config_data, source_data):
        self.config_data = config_data
        self.source_data = source_data
        self.temp_pattern_list = []
        self.hash_and_find_result = {}
        self.temp_restore_list = {}

    def compare_func(self, config_dict, source_dict):
        if (isinstance(config_dict, list)):
            if isinstance(source_dict, list):
                for value in config_dict:
                    for value1 in source_dict:
                        self.compare_func(value, value1)
            else:
                raise Exception(
                    f"The content of source file doesn't match with config file!"
                )
        else:
            for key, value in config_dict.items():
                if isinstance(value, str):
                    if value == 'Hash&Find':
                        if source_dict.get(key) is not None:
                            self.temp_pattern_list.append(source_dict.get(key))
                        else:
                            print(f"Key {key} exists in config but not found in source file!");
                    if value == 'Required':
                        source_dict_item = source_dict.get(key, None)
                        if source_dict_item is None:
                            raise Exception(
                                f"Key {key} exists in config but not found in source file!"
                            )
                        else:
                            get_key_element = self.temp_restore_list.get(key, None)
                            if get_key_element is None:
                                self.temp_restore_list[key] = source_dict.get(key)
                            else:
                                if isinstance(self.temp_restore_list[key], list):
                                    self.temp_restore_list[key].append(source_dict.get(key))
                                else:
                                    temp_array = []
                                    temp_array.append(self.temp_restore_list[key])
                                    temp_array.append(source_dict.get(key))
                                    self.temp_restore_list[key] = temp_array
                else:
                    if source_dict.get(key) is not None:
                        self.compare_func(value, source_dict.get(key))
                    else:
                        print(f"Key {key} exists in config but not found in source file!")

    def hash_and_find(self, value):
        global hash_and_find_result
        source_data_str = json.dumps(value)
        for value1 in self.temp_pattern_list:
            hash_value = hashlib.md5(value1.encode("utf-8")).hexdigest()
            source_data_str = source_data_str.replace(value1, hash_value)

        self.hash_and_find_result = json.loads(source_data_str)

    def restoreRequiredData(self, hashedData, temp_restore_list):
        for key, value in hashedData.items():
            if isinstance(value, list):
                for value1 in value:
                    index = value.index(value1)
                    for key2, value2 in value1.items():
                        tempValue = temp_restore_list.get(key2, None)
                        if tempValue is not None:
                            if isinstance(tempValue, list):
                                hashedData[key][index][key2] = tempValue[index]
                            else:
                                hashedData[key][index][key2] = tempValue
            else:
                tempValue = temp_restore_list.get(key, None)
                if tempValue is None and value is object:
                    self.restoreRequiredData(hashedData.get(key), temp_restore_list)
                if tempValue is not None:
                    hashedData[key] = tempValue

    def anonimizedDict(self):
        self.compare_func(self.config_data, self.source_data)
        print(self.temp_restore_list)
        print(self.temp_pattern_list)
        self.temp_pattern_list.sort(key=len, reverse=1)
        print(self.temp_pattern_list)
        self.hash_and_find(self.source_data)
        self.restoreRequiredData(self.hash_and_find_result, self.temp_restore_list)
        return self.hash_and_find_result

    def anonimizedFile(self):
        with open('output.json', 'w') as outfile:
            outfile.write(json.dumps(self.hash_and_find_result, indent=3))

anom = Anonimazer(config_data, source_data)

anoniDict = anom.anonimizedDict()
print(anoniDict)

anom.anonimizedFile()




