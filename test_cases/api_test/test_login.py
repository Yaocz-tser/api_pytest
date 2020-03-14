import pytest
import logging
import sys

@pytest.mark.p1
@pytest.mark.apitest
def test_user_login(api,case_data):
    logging.info('正常')
    data_url = case_data.get('url')
    data_type = case_data.get('data_type')
    data_args = case_data.get('args')
    data_expect_res = case_data.get('expect_res')
    res_dict = api.post(data_url,data=data_args).text
    
    
if __name__ == '__main__':
    pytest.main()
    


