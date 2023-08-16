import unittest
import requests
import json

class TestAPI(unittest.TestCase):

    def test_post(self):
        url = 'http://localhost:8000'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'user_id': 4}
        correct_result = {
             "user_id": 4,
             "json_data": sorted(['3439525', '3439590', '3439598', '3439619', '3439622', '3439652', '3439659', '3439661', '3439696', '3439705', '3439725', '3439748', '3439749', '3439780', '3439781', '3439787', '3439831', '3439838', '3439902', '3440021', '3440033', '3440034', '3440054', '3440055', '3440063', '3440076', '3440379', '3440394', '3440400', '3440541', '3440554', '3440571', '3440577', '3440580', '3440581', '3440596', '3440639', '3440645', '3440653', '3440654', '3440684', '3440696', '3440698', '3440705', '3440711', '3440714', '3440747', '3440762', '3440771', '3440777', '3440780', '3440781', '3440789', '3440791', '3440830', '3440879', '3440925', '3440939', '3440942', '3440963', '3440985', '3441011', '3441074', '3441114', '3441122', '3441242', '3441243', '3441273', '3441287', '3441292', '3441354', '3441358', '3441377', '3441442', '3441475', '3441476', '3441481', '3441483', '3441572', '3441575', '3441577', '3441659', '3441665', '3441674', '3441684', '3441686', '3441702', '3441803', '3441890', '3441894', '3441954', '3441988', '3442007', '3442050', '3442051', '3442057', '3442058', '3442071', '3442098', '3442105', '3442106', '3442138', '3442163', '3442206', '3442221', '3442231', '3442233', '3442236', '3442238', '3442299', '3442398', '3442450', '3442546', '3442568', '3442584', '3442585', '3442587', '3442597', '3442683', '3442716', '3442720', '3442727', '3442750', '3442766', '3442778', '3442803', '3442805', '3442926', '3442939', '3442980', '3443013', '3443025', '3443030', '3443061', '3443173', '3443183', '3443207', '3443256', '3443280', '3443289', '3443341', '3443342', '3443352', '3443356', '3443411', '3443413', '3443533', '3443588', '3443631', '3443632', '3443644', '3443697', '3443737', '3443756', '3443758', '3443861', '3443909', '3443928', '3443952', '3480812', '3480818', '3480819', '3480820', '3480822', '3480823', '3480825', '7838849'])
        }
        response = requests.post(url, headers=headers, data=data)
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(list(response_data['json_data'].keys())), correct_result['json_data'])
        self.assertEqual(response_data['user_id'], correct_result['user_id'])
        self.assertTrue(response_data['timestamp'])

    def test_get(self):
        url = 'http://localhost:8000?user_id=1'
        correct_result = {"percentage": "100.0%", "user_id": "1"}

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), correct_result)

if __name__ == '__main__':
    unittest.main()