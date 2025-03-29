import os
import yaml


def config(app):

    # config root
    root = app.config_root

    # default config
    conf = {
        "web": {
            "host": "0.0.0.0",
            "port": 8001,
            "workers": 1,
            "debug": True,
            "sanic": {
                "REQUEST_TIMEOUT": 60,
                "RESPONSE_TIMEOUT": 1*60*60,
                "KEEP_ALIVE": True,
                "KEEP_ALIVE_TIMEOUT": 10*60
            }
        }
    }

    # yaml file config
    with open(
            os.path.join(root, 'config.yml'),
            'r',
            encoding='utf-8'
    ) as f:
        # loaded_conf = yaml.load(f.read())
        loaded_conf = yaml.safe_load(f)
        conf = {
            **conf,
            **loaded_conf
        }
        f.close()

    return conf
