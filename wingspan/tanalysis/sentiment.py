from google.cloud import language_v1
from tanalysis.models import Tweet, ScoreData
from typing import List
import os
import random
import datetime

class SentimentAnalyzer():
    """

    This class is used to perform sentiment analysis on Tweet objects

    Attributes:
        analyzer: A google.cloud LanguageServiceClient instance
        type: A string that indicates the type of text to be given to the analyzer

    """
    def __init__(self, text_type=language_v1.Document.Type.PLAIN_TEXT):
        """

        Initializes a SentimentAnalyzer with text_type

        Args:
            text_type (str): the type of text to be given to the analyzer.
            Defaults to google.cloud.language_v1.Document.Type.PLAIN_TEXT

        """
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.analyzer = language_v1.LanguageServiceClient()
        else:
            self.analyzer = None
        self.type = text_type

    def analyzeTweets(self, tweets: List[Tweet]):
        """

        Iterates through a given list of Tweet objects, uses the analyzer to perform sentiment analysis on the text,
        and updates the sentiment_score and sentiment_magnitude of each Tweet. If the Google API credentials are not
        set with an environment variable, the Tweets will be given random values.

        Args:
            tweets (List[Tweet]): list of tweets to analyze

        Return:
            None
            
        """
        all_score_data = []

        if self.analyzer:
            for tweet in tweets:
                document = language_v1.Document(content=tweet.text, type_=self.type)
                response = self.analyzer.analyze_sentiment(request={'document': document})
                score_data = ScoreData(score=(response.document_sentiment.score * response.document_sentiment.magnitude), 
                    timestamp=tweet.timestamp)
                all_score_data.append(score_data)
        else:
            for tweet in tweets:
                score_data = {"score":(random.uniform(-1, 1) * random.uniform(0, 100)), "timestamp":tweet.timestamp.strftime("%m-%d-%yT%H:%M:%SZ")}
                all_score_data.append(score_data)

        return all_score_data

