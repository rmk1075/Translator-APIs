import json
import os
import pathlib
import requests


class Papago:
    def __init__(self, resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())):
        self._path = os.path.join("/", resource, "key.json")
        self._id, self._key = self.read_key(self._path)

    def read_key(self, path):
        with open(path, "r") as file:
            jf = json.load(file)
            if "id" not in jf or "key" not in jf:
                raise RuntimeError("error :: invalid key file. please check key.json. jf={}".format(jf))
            return jf["id"], jf["key"]

    def translate(self, text):
        method = "POST"
        url = "https://openapi.naver.com/v1/papago/n2mt"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": self._id,
            "X-Naver-Client-Secret": self._key,
        }

        source = "zh-CN"
        target = "ko"
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


def main(resource=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())):
    if not os.path.exists(resource) or not os.path.isdir(resource):
        print("warning :: invalid resource path. resource={}".format(resource))
        return

    try:
        api = Papago(resource)
        for file_name in os.listdir(resource):
            file_path = os.path.join("/", resource, file_name)
            if os.path.isdir(file_path):
                continue

            if file_path.split(".")[-1] != "txt":
                continue
            
            with open(file_path, "r") as file:
                for line in file.readlines():
                    line = line.strip()
                    # TODO: consider separator
                    # for sentence in line.split("! | 。 | ?"):
                    for sentence in line.split("。"):
                        if len(sentence) == 0:
                            print()
                            continue

                        translated_text = api.translate(sentence)

                        print(sentence)
                        print(translated_text)
                        print()
    except Exception as e:
        print("exception={}".format(e))


if __name__ == "__main__":
    # constant
    DIR_LOCATION = str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())
    main(DIR_LOCATION)