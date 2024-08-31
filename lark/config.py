import codecs
import json
import os

from config_bean import ConfigBean

root_path = os.path.dirname(os.path.dirname(__file__))
config_file_path = os.path.join(root_path, 'lark', 'config.json')
image_save_tmp_path = os.path.join(root_path, 'tmp', 'image')

def write_config(config):
    try:
        with open(config_file_path, 'w') as writeFile:
            json.dump(config, writeFile, indent=4)
    except Exception as e:
        print(e)

def get_image_form_url(dir, url):
    image_folder_path = os.path.join(image_save_tmp_path, dir)
    if not os.path.exists(image_folder_path):
        raise Exception(f'文件夹不存在 {image_save_tmp_path, dir}')
    image_file_path = os.path.join(image_folder_path, os.path.basename(url))
    if not os.path.exists(image_file_path):
        raise Exception(f'文件不存在 {image_file_path, dir}')
    return image_file_path

def read_config() -> ConfigBean:
    if not os.path.exists(config_file_path):
        with codecs.open(config_file_path, 'a+', encoding='utf-8') as f:
            f.write("{}")
            return ConfigBean()
    try:
        with open(config_file_path) as f:
            config = json.load(f)
            if config is None:
                os.remove(config_file_path)
                read_config()
            else:
                bean = ConfigBean(**config)
                return bean
    except Exception as e:
        os.remove(config_file_path)
        read_config()
