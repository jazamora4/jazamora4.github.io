import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import io

ckey = "z4LoNxjDncy3bWDzhkVFqoVrp"
csecret = "hRPiQE5O7tKEEtINb9FhGLamNW7MOzuYbK3mnkmCMb5ou2pud9"
atoken = "3218861973-dBd4UC1amnvL1pdNEvgUQXP7DKLV6hUx6dimQMY"
asecret = "NvWlANi2ZCk7nLZ34dmMSvavYbIeoWRBym2ODnHyX2NnQ"

quito = [-78.583794058, -0.3575210651, -78.3671114711, -0.0630414425]

class listener(StreamListener):

    def on_connect(self):
        print("Conectado...")
        
    def on_data(self, coded_data):
        try:
            decoded = json.loads(coded_data)
        except Exception as e:
            print(e) 
            return True
   
        if decoded.get('geo') is not None:
            location = decoded.get('geo').get('coordinates')
        else:
            location = '[,]'

        text = decoded['text'].replace('\n',' ')
        user = '@' + decoded.get('user').get('screen_name')
        created = decoded.get('created_at')
        #tweet = '%s|%s|%s|s\n' % (user,location,created,text)
        tweet = "user: "+user+"\n"+"location:"+location+"\n"+"created_at:"+created+"\n"+"text:"+text+"\n"
        print(tweet)
        file = io.open("tweetsM.txt", "a", encoding="utf-8")
        file.write(tweet)
        file.close()
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    print('Starting')
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=quito)
