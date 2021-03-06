import copy

import pytest

import bigchaindb
from bigchaindb import config_utils


ORIGINAL_CONFIG = copy.deepcopy(bigchaindb.config)


@pytest.fixture(scope='function', autouse=True)
def clean_config():
    bigchaindb.config = copy.deepcopy(ORIGINAL_CONFIG)


def test_bigchain_instance_is_initialized_when_conf_provided():
    assert 'CONFIGURED' not in bigchaindb.config

    config_utils.dict_config({'keypair': {'public': 'a', 'private': 'b'}})

    assert bigchaindb.config['CONFIGURED'] == True
    b = bigchaindb.Bigchain()

    assert b.me
    assert b.me_private


def test_bigchain_instance_raises_when_not_configured(monkeypatch):
    assert 'CONFIGURED' not in bigchaindb.config

    # We need to disable ``bigchaindb.config_utils.autoconfigure`` to avoid reading
    # from existing configurations
    monkeypatch.setattr(config_utils, 'autoconfigure', lambda: 0)

    with pytest.raises(bigchaindb.core.KeypairNotFoundException):
        bigchaindb.Bigchain()

