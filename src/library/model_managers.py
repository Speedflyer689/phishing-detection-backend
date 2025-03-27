import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

import joblib
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class PhishingEmailDetector:
    def __init__(self, threshold=0.5):
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ml_resources")
        self.max_length = 200
        self.threshold = threshold

    def load(self):
        """Load the model and required components"""
        self.model = load_model(os.path.join(self.filepath, "phishing_lstm_model1.h5"))
        
        with open(os.path.join(self.filepath, "tokenizer.pickle"), 'rb') as handle:
            self.tokenizer = pickle.load(handle)
            
        with open(os.path.join(self.filepath, "label_encoder.pickle"), 'rb') as handle:
            self.label_encoder = pickle.load(handle)
            
    def predict(self, email_text: str) -> bool:
        """Predict if emails are phishing or legitimate.
        Args:
            emails (str): The email text to classify
        Returns:
            bool: False if the email is legitimate, True if phishing
        The function processes the input email text through the following steps:
        1. Converts text to sequences using the tokenizer
        2. Pads sequences to uniform length
        3. Makes prediction using the loaded model
        4. Decodes prediction labels
        Example:
            >>> model.predict("Hello, please verify your account...")
            True
        """
        sequences = self.tokenizer.texts_to_sequences([email_text])
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        predictions = (self.model.predict(padded) > self.threshold).astype("int32")
        decoded_preds = self.label_encoder.inverse_transform(predictions.ravel())
        
        return True if decoded_preds[0] == "Phishing Email" else False



class PhishingUrlDetector:
    def __init__(self):
        self.model = None
        self.char2idx = None
        self.scaler = None
        self.ordered_keys = None
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ml_resources")

    def load(self):
        self.model = load_model(os.path.join(self.filepath, "hybrid_model_tf.h5"))
        with open(os.path.join(self.filepath, "char2idx.json")) as f:
            self.char2idx = json.load(f)
        scaler_data = joblib.load(os.path.join(self.filepath, "scaler_and_columns.pkl"))
        self.scaler = scaler_data['scaler']
        self.ordered_keys = scaler_data['columns']

    def predict(self, url: str, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        url_seq = np.array([self._text_to_seq(url, maxlen=200)])
        title_seq = np.array([self._text_to_seq(title, maxlen=120)])

        url_feats = self._extract_url_features(url)
        html_feats = self._extract_html_features(html)
        features_dict = {**url_feats, **html_feats}
        structured_vector = np.array([self._vectorize(features_dict)])
        structured_scaled = self.scaler.transform(structured_vector)
        padded = np.zeros((1, 50))
        padded[0, :structured_scaled.shape[1]] = structured_scaled
        prob = self.model.predict([url_seq, title_seq, padded])[0][0]
        label = bool(prob > 0.5)
        confidence = prob if label else 1 - prob
        return label, float(confidence)

    def _text_to_seq(self, text, maxlen):
        seq = [self.char2idx.get(char, 0) for char in text]
        return seq[:maxlen] + [0] * max(0, maxlen - len(seq))

    def _extract_url_features(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        tld = domain.split('.')[-1] if '.' in domain else ''
        is_https = int(parsed.scheme == 'https')
        is_ip = int(bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)))

        return {
            'URLLength': len(url),
            'DomainLength': len(domain),
            'IsDomainIP': is_ip,
            'TLDLength': len(tld),
            'IsHTTPS': is_https,
            'NoOfSubDomain': domain.count('.') - 1,
            'NoOfDegitsInURL': sum(c.isdigit() for c in url),
            'NoOfLettersInURL': sum(c.isalpha() for c in url),
            'SpacialCharRatioInURL': len(re.findall(r'[^\w]', url)) / len(url),
            'NoOfEqualsInURL': url.count('='),
            'NoOfQMarkInURL': url.count('?'),
            'NoOfAmpersandInURL': url.count('&'),
            'NoOfOtherSpecialCharsInURL': len(re.findall(r'[$+,:;@]', url))
        }

    def _extract_html_features(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return {
            'LineOfCode': html.count('\n'),
            'LargestLineLength': max((len(line) for line in html.split('\n')), default=0),
            'NoOfImage': len(soup.find_all('img')),
            'NoOfJS': len(soup.find_all('script')),
            'NoOfCSS': len(soup.find_all('link', rel='stylesheet')),
            'NoOfiFrame': len(soup.find_all('iframe')),
            'HasTitle': int(bool(soup.title and soup.title.string.strip())),
            'HasDescription': int(bool(soup.find('meta', attrs={'name': 'description'}))),
            'HasSubmitButton': int(bool(soup.find('button', type='submit'))),
            'HasHiddenFields': len(soup.find_all('input', type='hidden')),
            'HasPasswordField': int(bool(soup.find_all('input', type='password'))),
            'HasSocialNet': int(any(d in html for d in ["facebook.com", "twitter.com", "linkedin.com"])),
            'Bank': int("bank" in html.lower()),
            'Pay': int("pay" in html.lower()),
            'Crypto': int("crypto" in html.lower()),
            'HasCopyrightInfo': int("copyright" in html.lower()),
            'Robots': int("robots" in html.lower()),
            'IsResponsive': int("viewport" in html.lower()),
            'NoOfURLRedirect': html.count('http'),
            'NoOfSelfRedirect': html.count('window.location'),
            'HasExternalFormSubmit': int('action="http' in html),
            'NoOfSelfRef': html.count('href="#"'),
            'NoOfEmptyRef': html.count('href=""'),
            'NoOfExternalRef': html.count('http'),
            'DomainTitleMatchScore': 0,
            'URLTitleMatchScore': 0,
            'TLDLegitimateProb': 0,
            'URLCharProb': 0,
            'CharContinuationRate': 0,
            'ObfuscationRatio': 0,
            'NoOfObfuscatedChar': 0,
            'HasObfuscation': 0
        }

    def _vectorize(self, features_dict):
        return [features_dict.get(k, 0) for k in self.ordered_keys]

   

if __name__ == "__main__":
    phishing_email_detector = PhishingEmailDetector()
    phishing_email_detector.load()
    print(phishing_email_detector.predict("Your meeting is confirmed for tomorrow at 10am."))
    