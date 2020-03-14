import os
import sys
import pytest

sys.path.insert(0,'../..')

from utils.data import Data
from utils.api import Api

@pytest.fixture(scope='session')
def data(request):
    basedir = request.config.rootdir
    try:
        data_file_path = os.path.join(basedir,'data','api_data.yaml')
        data = Data().load_yaml(data_file_path)
        print('data1:',data,type(data))
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return data

@pytest.fixture()
def case_data(request,data):
    case_name = request.function.__name__
    return data.get(case_name)

@pytest.fixture(scope='session')
def api():
    api = Api()
    return api


