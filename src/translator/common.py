from translator.translators import *

import json
import os
import pathlib
import sys


'''
TranslatorFactory 클래스
- 입력받은 api_type 에 맞는 api 객체를 반환하는 팩토리 클래스
- api_types 목록에 지원하는 api 종류를 저장
'''
class TranslatorFactory:
    Papago = "Papago"
    GT = "GoogleTranslation"
    KT = "KakaoTranslation"
    api_types = [Papago, GT, KT]

    @classmethod
    def getTranslator(cls, api_type="Papago", resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../../resource")).resolve())):
        if api_type not in cls.api_types:
            raise RuntimeError("error :: unsupported api type. please check api type. api_type={}".format(api_type))

        mod = getattr(sys.modules[__name__], api_type)
        if not mod:
            raise RuntimeError("error :: unknown api type class. please check api type and the API classes. api_type={}".format(api_type))
        return mod(api_type=api_type, resource=resource)
