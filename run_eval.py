import importlib
import json

CONFIG_PATH = 'config.json'

"""
Entry point for the entire evaluation program
"""
if __name__ == "__main__":
    config_file = open(CONFIG_PATH, 'r')
    config = json.load(config_file)

    if 'target_dir' not in config:
        raise NameError('Target directory \'target_dir\' must be specified for evaluation')

    target_module = importlib.import_module(config['target_dir'])
    target_module.main(global_config=config)
