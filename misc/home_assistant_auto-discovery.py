#!/usr/bin/env python3

import sys
from pathlib import Path
from pprint import pformat  # noqa: F401
import time
import json
import paho.mqtt.publish as publish
import logging

sys.path.append(str(Path(__file__).parent.absolute().parent))

from mcpConfig import McpConfig

logger = logging.getLogger('home-assistant-auto-discovery')
logger.setLevel(logging.INFO)

class HADiscovery(object):
    discovery_base_topic = 'homeassistant'
    unique_id_base = '001'

    def __init__(self):
        self.config = McpConfig()
        self._port = 1883


    def main(self):
        if not self.config.get('MQTT_ENABLE'):
            logger.error('MQ Publishing not enabled')
            sys.exit(1)

        hostname = self.config.get('MQTT_HOST')
        port = self.config.get('MQTT_PORT')
        username = self.config.get('MQTT_USER')
        password =  self.config.get('MQTT_PASS')
        base_topic  = self.config.get('MQTT_TOPIC')

        print('')
        print('#################################################')
        print('##### Home Assistant Discovery Setup Script #####')
        print('#################################################')
        print('')
        print('Hostname: {0}'.format(hostname))
        print('Port: {0}'.format(port))
        print('Username: {0}'.format(username))
        print('')
        print('Auto-discovery base topic: {0}'.format(self.discovery_base_topic))
        print('mlCloudDetect base topic:    {0}'.format(base_topic))
        print('')


        basic_sensor_list = [
            {
                'component' : 'sensor',
                'object_id' : 'mlCloudDetect_status',
                'config' : {
                    'name' : 'Cloud Status',
                    'unique_id' : 'mlCloudDetect_{0}'.format(self.unique_id_base),
                    'state_topic' : '/'.join((base_topic, 'Clouds')),
                },
            },]
        
        retain=True
        message_list = list()
        for sensor in basic_sensor_list:
            message = {
                'topic'    : '/'.join((self.discovery_base_topic, sensor['component'], sensor['object_id'], 'config')),
                'payload'  : json.dumps(sensor['config']),
                'qos'      : 0,
                'retain'   : retain,
            }
            message_list.append(message)

            logger.warning('Create topic: %s', message['topic'])
            logger.warning('Data: %s', pformat(message))

        mq_auth = None
        mq_tls = None


        if username:
            mq_auth = {
                'username' : username,
                'password' : password,
            }

        logger.warning('Publishing discovery data')
        publish(
            message_list,
            transport='tcp',
            hostname=hostname,
            port=int(port),
            client_id='',
            keepalive=60,
            auth=mq_auth,
            tls=mq_tls,
        )


if __name__ == "__main__":

    had = HADiscovery()
    had.main()

