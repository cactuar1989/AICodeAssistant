from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_set_api_key():
    test_key = input('Enter your OpenAI key: ').strip()
    response = client.post('/set_api_key', json={'api_key': test_key})
    assert response.status_code == 200, f'Unexpected status: {response.status_code}'
    assert response.json() == {'message': 'API key saved successfully'}
    print('API key set via test')

def test_get_api_key():
    response = client.post('/get_api_key')
    data = response.json()
    assert response.status_code == 200, f'Unexpected status: {response.status_code}'
    assert 'api_key' in data, 'Missing api_key in response'
    assert isinstance(data['api_key'], str), 'API key is not a string'
    assert len(data['api_key']) > 0, 'API key empty'
    print(f'API get via test: {data["api_key"][:10]}...') 

def test_explain_code():
    request = {
        'language': 'python',
        'code': 'print("Hello World!")'
    }
    response = client.post('/explain_code', json=request)
    print(response.json)

def main():
    #test_set_api_key()
    test_get_api_key()
    test_explain_code()

if __name__ == '__main__':
    main()