import tweepy
import openai
import os

# Configurações do Twitter
twitter_api_key = 'oxk8BFUwAZpVZzJ8ldEDaBhtU'
twitter_api_secret = 'zLBLU2CBOEVLWExkMZsTOW0Th4cXJYVQBoXZ3UFfqeLfqAEnl6'
twitter_access_token = '1856858508706418690-IMp6Tsj1dMjMz2jpBuemWnHbnv9h2r'
twitter_access_secret = 'ZkkyiWO1yEKD1EhAlMlgSBIqWSH8ErYffMUoLFPorNrSr'

# Configurações do OpenAI
openai.api_key = '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'

# Autenticação no Twitter
auth = tweepy.OAuth1UserHandler(twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)

# Função para responder a tweets
def respond_to_tweet(tweet):
    prompt = f"O que você acha sobre o tweet: '{tweet.text}'? Responda com possíveis redflags."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply_text = response['choices'][0]['message']['content']
    api.update_status(status=f"@{tweet.user.screen_name} {reply_text}", in_reply_to_status_id=tweet.id)

# Função para escutar tweets
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if '@Mushroomdevs' in status.text:
            respond_to_tweet(status)

# Iniciar o stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['@Mushroomdevs'], is_async=True)
