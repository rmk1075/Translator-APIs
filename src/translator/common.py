from translator.translators import *

import json
import os
import pathlib
import sys


'''
TranslatorFactory 클래스
- 입력받은 translator_type 에 맞는 Translator 객체를 반환하는 팩토리 클래스
- translator_types 목록에 지원하는 translator 종류를 저장
'''
class TranslatorFactory:
    Papago = "Papago"
    GT = "GoogleTranslation"
    KT = "KakaoTranslation"
    translator_types = [Papago, GT, KT]

    @classmethod
    def getTranslator(cls, translator_type="Papago", resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../../resource")).resolve())):
        if translator_type not in cls.translator_types:
            raise RuntimeError("error :: unsupported translator type. please check translator type. translator_type={}".format(translator_type))

        mod = getattr(sys.modules[__name__], translator_type)
        if not mod:
            raise RuntimeError("error :: unknown translator type class. please check translator type and the Translator classes. translator_type={}".format(translator_type))
        return mod(translator_type=translator_type, resource=resource)
