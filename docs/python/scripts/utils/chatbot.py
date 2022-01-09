import time
import json
import hmac
import base64
import hashlib
import requests
import urllib.parse
from json import JSONDecodeError
from ..utils import SetLogs


logger = SetLogs('chatbot.log')
logger = logger.set_rotate(__name__, stream=True)


class DingtalkChatbot:
    def __init__(self, webhook, secret=None):
        self.webhook = webhook
        self.secret = secret
        if self.secret is not None and self.secret.startswith('SEC'):
            self.update_webhook()

    def update_webhook(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        self.webhook = "{}&timestamp={}&sign={}".format(self.webhook,
                                                        timestamp,
                                                        sign)

    def send_markdown(self, title, text, at_mobiles=None, at_all=True):
        text = text
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": at_all
            }
        }
        if at_mobiles is not None:
            at_mobiles = list(map(str, at_mobiles))
        else:
            at_mobiles = []
        data["at"]["atMobiles"] = at_mobiles
        return self.post(data)

    def post(self, data):
        try:
            post_data = json.dumps(data)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post(self.webhook,
                                     headers=headers,
                                     data=post_data)
        except requests.exceptions.HTTPError as err:
            logger.error("消息发送失败， HTTP error: {}, reason: {}" .format(
                err.response.status_code, err.response.reason))
        except requests.exceptions.ConnectionError:
            logger.error("消息发送失败，HTTP connection error!")
        except requests.exceptions.Timeout:
            logger.error("消息发送失败，Timeout error!")
        except requests.exceptions.RequestException:
            logger.error("消息发送失败, Request Exception!")
        else:
            try:
                result = response.json()
                logger.info(result)
            except JSONDecodeError:
                logger.error("服务器响应异常，状态码：{}，响应内容：{}".format(
                    response.status_code, response.text))
