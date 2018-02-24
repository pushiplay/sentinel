import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from pushid import PushiDaemon
from pushi_config import PushiConfig


def test_pushid():
    config_text = PushiConfig.slurp_config_file(config.pushi_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000071ed448e4468c0931723e7aa9a422b02c09579309c7a784606b6e103ec0'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000071ed448e4468c0931723e7aa9a422b02c09579309c7a784606b6e103ec0'

    creds = PushiConfig.get_rpc_creds(config_text, network)
    pushid = PushiDaemon(**creds)
    assert pushid.rpc_command is not None

    assert hasattr(pushid, 'rpc_connection')

    # Pushi testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = pushid.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert pushid.rpc_command('getblockhash', 0) == genesis_hash
