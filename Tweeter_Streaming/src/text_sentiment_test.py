from textblob import TextBlob
wiki = TextBlob("Destituyan al presidente")
print(wiki.detect_language())
wiki_en = wiki.translate(to='en')
print(wiki_en)
print(wiki_en.sentiment)