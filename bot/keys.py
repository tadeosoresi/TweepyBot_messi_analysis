''' Go to https://developer.twitter.com/en/apply-for-access and 
    create a developer count! then create a project, 
    after that keys will be gave to you
'''
class ApiKey():
    @staticmethod
    def returnkeys():
        print('--- GETTING API KEYS ---')
        api_key = 'DMBc5whJ3rUq7IL9lRhXhXcUn' # Consumer key here :)
        api_key_secret = 'TcTTFMTZmWoT8U1mUaSJ6JmRwskax9ajXC7M59Ik83pbMWuuPu' # Secret consume key here :)

        return api_key, api_key_secret

class Token():
    @staticmethod
    def returnkeys():
        print('--- GETTING TOKENS ---')
        token_key = '2923241841-FJGTutko51KQT47ONSTwJkAXOWs0isQSky7R8xh' # Access token here :)
        token_secret = 'hrv3wPL9z1UyHCYW7v9VVTxhEV4Lbxh5OZtmnE6SJk6Gi' # Secret access token here :)

        return token_key, token_secret

class MeaningCloud():
    ''' This is standard data for meaning cloud requests,
    the only thing is that you have to enter to https://www.meaningcloud.com/es,
    register and get the key'''
    @staticmethod
    def returndata(tweet, language):
        url = 'https://api.meaningcloud.com/sentiment-2.1'
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        payload={
            'key': '0fbbc49fbe29d2c2133fe1e95cfaf739',
            'txt': tweet,
            'lang': language,
        }

        return url, headers, payload