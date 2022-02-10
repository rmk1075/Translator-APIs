# Translator-APIs

## Overview

다양한 번역 API 를 사용한 번역기 구현

./input 디렉토리에 위치한 text 파일들을 번역하여 ./output 디렉토리 아래에 input 파일과 동일한 이름의 text 파일로 저장한다.

한국어 (ko) 문서를 중국어 번체 (zh-CN) 로 번역한다.

1. Papago API

    - Papago 번역 API 를 사용한 번역기

    - 파파고 REST API 를 사용하여 POST 통신으로 번역된 텍스트를 얻는다.

2. Google Translation API

    - Google Translation API 를 사용한 번역기

    - Google Translation API 는 google-cloud-translate 패키지의 설치가 필요하다.

    ~~~shell
    pip install google-cloud-translate
    ~~~

    - google-cloud-translate 패키지 설치 후 아래와 같이 translate_v2 의 Client() 인스턴스를 생성하여 사용한다.

    ~~~python
    from google.cloud import translate_v2 as google_translate

    client = google_translate.Client()
    ~~~

3. Kakao Translation API

    - Kakao 번역 API 를 사용한 벙녁기

    - Kakao Developers REST API 를 사용하여 POST 통신으로 번역된 텍스트를 얻느다.

    - 번역된 텍스트들은 마침표를 기준으로 나눠져서 list 에 담겨져 반환된다.
