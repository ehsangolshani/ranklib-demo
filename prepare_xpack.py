from elasticsearch_xpack import XPackClient
import getpass
import sys

from log_conf import Logger
from utils import elastic_connection

if __name__ == "__main__":
    """This script set the default roles and users to run the LTR ranklib-demo"""
    if len(sys.argv) == 2:
        password = getpass.getpass()
    elif len(sys.argv) == 3:
        password = sys.argv[2]
    else:
        Logger.logger.info("""prepare_xpack.py [elasticsearch.user] [elasticsearch.password]""")
        sys.exit(-1)

    username = sys.argv[1]

    es = elastic_connection(http_auth=(username, password))
    xpack = XPackClient(es)

    Logger.logger.info("Configure ltr_admin role:")
    res = xpack.security.put_role('ltr_admin', {
        "cluster": ["all"],
        "indices": [{
            "names": [".ltrstore*"],
            "privileges": ["all"]
        }]
    })
    Logger.logger.info(res)

    Logger.logger.info("Configure tmdb role:")
    res = xpack.security.put_role('tmdb', {
        'indices': [{
            "names": ["tmdb"],
            "privileges": ["all"]
        }]
    })
    Logger.logger.info(res)

    Logger.logger.info("Configure ltr_demo user:")
    res = xpack.security.put_user('ltr_demo', {
        'password': 'elastic',
        'roles': ['ltr_admin', "tmdb"]
    })
    Logger.logger.info(res)

    Logger.logger.info("\nRoles and user created. Be sure to update settings.cfg")
