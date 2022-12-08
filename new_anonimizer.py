from black import Dict
import hashlib
import json
from jsoncomment import JsonComment

config_data = {}
source_data = {}
temp_pattern_list = []
temp_restore_list = {}
error_list = []

# getting json data from config.json file
with open('config.json') as config_file:
    paser = JsonComment(json)
    config_data = paser.load(config_file)

# getting json data from source.json file
with open('source.json') as source_file:
    paser = JsonComment(json)
    source_data = paser.load(source_file)

# compare json data of config.json file and json data of source.json file
def compare_func(config_dict, source_dict):
    if (isinstance(config_dict, list)):
        if isinstance(source_dict, list):
            for value in config_dict:
                for value1 in source_dict:
                    compare_func(value, value1)
        else:
            raise Exception(
                f"The content of source file doesn't match with config file!"
            )
    else:
        for key, value in config_dict.items():
            source_dict_item = source_dict.get(key, None)
            if isinstance(value, str):
                if value == 'Hash&Find':
                    if source_dict_item is not None:
                        temp_pattern_list.append(source_dict.get(key))
                    else:
                        print(f"Warning: Key {key} exists in config but not found in source file!")
                if value == 'Required':
                    if source_dict_item is None:
                        print(f"Error: Key {key} exists in config but not found in source file!")
                        error_list.append(key)
                    else:
                        get_key_element = temp_restore_list.get(key, None)
                        if get_key_element is None:
                            temp_restore_list[key] = source_dict_item
                        else:
                            if isinstance(temp_restore_list[key], list):
                                temp_restore_list[key].append(source_dict_item)
                            else:
                                temp_array = []
                                temp_array.append(get_key_element)
                                temp_array.append(source_dict_item)
                                temp_restore_list[key] = temp_array

                if value == 'Copy' or value == 'Hash':
                    if source_dict.get(key) is None:
                        print(f"Warning: Key {key} exists in config but not found in source file!")
            else:
                if source_dict_item is not None:
                    compare_func(value, source_dict.get(key))
                else:
                    print(f"Warning: Key {key} exists in config but not found in source file!")

# md5 hash and replace value into hash value in source json data
def hash_and_find(value):
    source_data_str = json.dumps(value)
    for value1 in temp_pattern_list:
        hash_value = hashlib.md5(value1.encode("utf-8")).hexdigest()
        source_data_str = source_data_str.replace(value1, hash_value)
    hash_and_find_result = json.loads(source_data_str)
    return hash_and_find_result

# replace the value of 'Required' field into original value in source json data
def restoreRequiredData(hashedData, temp_restore_list):
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
                restoreRequiredData(hashedData.get(key), temp_restore_list)
            if tempValue is not None:
                hashedData[key] = tempValue

# get anonimized json data
def anonimizedDict(config_data, source_data):
    compare_func(config_data, source_data)
    if len(error_list) > 0:
        error_key_str = ''
        for value in error_list:
            error_key_str = error_key_str + "," + value
        raise Exception(
            f"Error: Key {error_key_str} exists in config but not found in source file!"
        )
    temp_pattern_list.sort(key=len, reverse=1)
    hashResult = hash_and_find(source_data)
    restoreRequiredData(hashResult, temp_restore_list)
    return hashResult

# get anonimized file from anonimized source json file
def anonimizedFile(hash_and_find_result):
    with open('output.json', 'w') as outfile:
        outfile.write(json.dumps(hash_and_find_result, indent=3))

anoniDict = anonimizedDict(config_data, source_data)
print(anoniDict)

anonimizedFile(anoniDict)




