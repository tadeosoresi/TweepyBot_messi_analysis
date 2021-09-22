''' Go to https://developer.twitter.com/en/apply-for-access and 
    create a developer count! then create a project, 
    after that keys will be gave to you
'''
class ApiKey():
    @staticmethod
    def returnkeys():
        print('--- GETTING API KEYS ---')
        api_key = '' # Consumer key here :)
        api_key_secret = '' # Secret consume key here :)

        return api_key, api_key_secret

class Token():
    @staticmethod
    def returnkeys():
        print('--- GETTING TOKENS ---')
        token_key = '' # Access token here :)
        token_secret = '' # Secret access token here :)

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
            'key': '', # MeaningCloud key here :)
            'txt': tweet,
            'lang': language,
        }

        return url, headers, payload
