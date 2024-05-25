import json
import os
import traceback
import logging
import logging.handlers
import subprocess
import sys
import time

def pre_check_site(sites):
    for i in range(0, len(sites)):
        site = sites[i]
        if "email" not in site or "domain" not in site:
            return False
    return True

def pre_check_data(data):
    if "sites" not in data:
        return False
    if type(data["sites"]) != list:
        return False
    return pre_check_site(data["sites"])
    

if __name__ == "__main__":
    config_path = os.getenv("CONFIG_PATH", "./config.json")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter\
    ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")

    rotate_log = logging.handlers.RotatingFileHandler("log.txt",
                                   maxBytes=1024 * 1024 * 100, backupCount=20)
    rotate_log.setLevel(logging.DEBUG)
    rotate_log.setFormatter(logFormatter)
    logger.addHandler(rotate_log)
    logStdout = logging.StreamHandler(sys.stdout)
    logStdout.setFormatter(logFormatter)
    logStdout.setLevel(logging.DEBUG)
    logger.addHandler(logStdout)
    try:
        time_pause = int(os.getenv("TIME_SLEEP", "43200"))
        logger.info("Loading config file...")
        fp = open(config_path, "r", encoding="utf8")
        data = json.load(fp)
        fp.close()
        logger.info("Config file loaded !")
        logger.info("Check config...")
        if not pre_check_data(data):
            logger.error("Check config failed !")
            exit(-1)
        logger.info("Check config ok !")
        logger.info("Start sites lookup")
        while True:
            for site in data['sites']:
                logger.info("Lookup :" + site['domain'])
                subprocess.call(['/bin/sh', '/cert.sh', site['email'], site['domain']], stdout=sys.stdout, stderr=sys.stderr)
            logger.info("Pause of " + str(time_pause) + " secondes")
            time.sleep(time_pause)
            logger.info("Start sites lookup")
    except Exception as e:
        traceback.print_exc()
        exit(-1)