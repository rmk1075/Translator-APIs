from abc import abstractmethod
from google.cloud import translate_v2 as google_translate

import json
import os
import pathlib
import requests


'''
Translator 클래스
- read_key(cls, path, api_type): path 의 key 파일에서 api_type 에 맞는 api 키 정보를 읽어온다.
- translate(self, text): 입력된 text 를 번역하는 abstract method.
'''
class Translator:
    @classmethod
    def read_info(cls, path, api_type):
        with open(path, "r") as file:
            jf = json.load(file)
            if api_type not in jf:
                raise RuntimeError("error :: key file does not contains thie api account info. please check key.json. api_type={} jf={}".format(api_type, jf))

            info = jf[api_type]
            return info

    @abstractmethod
    def translate(self, text):
        pass


'''
GoogleTranslation 클래스
- Google Translation API 를 사용하는 번역기 클래스
- google cloud 패키지 설치 및 credential 환경변수 설정
'''
class GoogleTranslation(Translator):
    def __init__(self, api_type="GoogleTranslation", resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())):
        self._api_type = api_type
        self._path = os.path.join("/", resource, "key.json")
        self._info = Translator.read_info(path=self._path, api_type=self._api_type)

        if "key" not in self._info:
            raise RuntimeError("error :: invalid account info. please check key.json. info={}".format(self._info))
        self._credential_path = self._info["key"]

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(pathlib.Path(os.path.join("/", resource, self._credential_path)).resolve())
        self._gt = google_translate.Client()

    def translate(self, text):
        target = "zh-CN"
        result = self._gt.translate(text, target_language=target)

        return result["translatedText"]


'''
Papago 클래스
- Naver Papago 번역 API 를 사용하는 번역기 클래스
'''
class Papago(Translator):
    def __init__(self, api_type="Papago", resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())):
        self._api_type = api_type
        self._path = os.path.join("/", resource, "key.json")
        self._info = Translator.read_info(path=self._path, api_type=self._api_type)

        if "id" not in self._info or "key" not in self._info:
            raise RuntimeError("error :: invalid account info. please check key.json. info={}".format(info))
        self._id = self._info["id"]
        self._key = self._info["key"]

    def translate(self, text):
        method = "POST"
        url = "https://openapi.naver.com/v1/papago/n2mt"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": self._id,
            "X-Naver-Client-Secret": self._key,
        }

        # source = "zh-CN"
        # target = "ko"
        source = "ko"
        target = "zh-CN"
        data = {
            "source": source,
            "target": target,
            "text": text
        }

        result = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )

        if result.status_code != 200:
            raise RuntimeError("error :: api request failed.\n url={}\n headers={}\n data={}\n result={}\n result.text={}".format(url, headers, data, result, result.text))

        return result.json()["message"]["result"]["translatedText"]


'''
KakaoTranslation 클래스
- Kakao 번역 API 를 사용하는 번역기 클래스
'''
class KakaoTranslation(Translator):
    def __init__(self, api_type="KakaoTranslation", resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())):
        self._api_type = api_type
        self._path = os.path.join("/", resource, "key.json")
        self._info = Translator.read_info(path=self._path, api_type=self._api_type)

        if "key" not in self._info:
            raise RuntimeError("error :: invalid account info. please check key.json. info={}".format(info))
        self._key = self._info["key"]

    def translate(self, text):
        method = "POST"
        url = "https://dapi.kakao.com/v2/translation/translate"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "KakaoAK " + self._key
        }

        source = "kr"
        target = "cn"
        data = {
            "src_lang": source,
            "target_lang": target,
            "query": text
        }

        result = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )

        if result.status_code != 200:
            raise RuntimeError("error :: api request failed.\n url={}\n headers={}\n data={}\n result={}\n result.text={}".format(url, headers, data, result, result.text))

        return " ".join(result.json()["translated_text"][0])