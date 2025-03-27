import numpy as np
import joblib
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tensorflow.keras.models import load_model

class PhishingUrlDetector:
    def __init__(self):
        self.model = None
        self.char2idx = None
        self.scaler = None

    def load(self):
        self.model = load_model("hybrid_model_tf.h5")
        with open("char2idx.json") as f:
            self.char2idx = json.load(f)
        self.scaler = joblib.load("scaler.pkl")

    def predict(self, url: str, title: str, html: str) -> dict:
        url_seq = np.array([self._text_to_seq(url, maxlen=200)])
        title_seq = np.array([self._text_to_seq(title, maxlen=120)])

        url_feats = self._extract_url_features(url)
        html_feats = self._extract_html_features(html)
        features_dict = {**url_feats, **html_feats}
        structured_vector = np.array([self._vectorize(features_dict)])
        structured_scaled = self.scaler.transform(structured_vector)

        # Pad structured input to shape (None, 50) to match model expectation
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
        ordered_keys = [
            'URLLength', 'DomainLength', 'IsDomainIP', 'TLDLength', 'IsHTTPS',
            'NoOfSubDomain', 'NoOfDegitsInURL', 'NoOfLettersInURL', 'SpacialCharRatioInURL',
            'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'NoOfOtherSpecialCharsInURL',
            'LineOfCode', 'LargestLineLength', 'HasTitle', 'HasDescription', 'HasSubmitButton',
            'HasHiddenFields', 'HasPasswordField', 'HasSocialNet', 'Bank', 'Pay', 'Crypto',
            'HasCopyrightInfo', 'NoOfImage', 'NoOfCSS', 'NoOfJS', 'NoOfiFrame', 'Robots',
            'IsResponsive', 'NoOfURLRedirect', 'NoOfSelfRedirect', 'HasExternalFormSubmit',
            'NoOfSelfRef', 'NoOfEmptyRef', 'NoOfExternalRef', 'DomainTitleMatchScore', 'URLTitleMatchScore',
            'TLDLegitimateProb', 'URLCharProb', 'CharContinuationRate', 'ObfuscationRatio',
            'NoOfObfuscatedChar', 'HasObfuscation'
        ]
        return [features_dict.get(k, 0) for k in ordered_keys]
detector = PhishingUrlDetector()
detector.load()

url = "http://example.com/login"
title = "Login Page"
html = "<html><head><title>Login</title></head><body><form><input type='password'></form></body></html>"

result = detector.predict(url, title, html)
print(result)
