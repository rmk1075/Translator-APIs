from translator.common import TranslatorFactory

import os
import pathlib
import traceback


def main(root=str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).resolve()), api_type="PAPAGO"):
    input_path = "/".join([root, "input"])
    output_path = "/".join([root, "output"])
    resource = "/".join([root, "resource"])
    if not os.path.exists(resource) or not os.path.isdir(resource):
        print("warning :: invalid resource path. resource={}".format(resource))
        return

    try:
        if not os.path.exists(input_path) or not os.path.isdir(input_path):
            print("warning :: invalid input path. input_path={}".format(input_path))
            return

        if not os.path.exists(output_path) or not os.path.isdir(output_path):
            os.makedirs(output_path)

        translator = TranslatorFactory.getTranslator(api_type=api_type, resource=str(pathlib.Path(os.path.join("/", root, "resource")).resolve()))
        for file_name in os.listdir(input_path):
            file_path = os.path.join("/", input_path, file_name)
            if os.path.isdir(file_path):
                continue

            if file_path.split(".")[-1] != "txt":
                continue
            
            out_path = os.path.join("/", output_path, file_name)
            with open(out_path, "w") as out:
                with open(file_path, "r") as file:
                    for line in file.readlines():
                        line = line.strip()
                        if len(line) == 0:
                            out.write("\n")
                            continue

                        translated_text = translator.translate(line)
                        write = line + "\n" + translated_text + "\n"
                        out.write(write)
    except Exception as e:
        print("exception={}".format(e))
        traceback.print_exc()


if __name__ == "__main__":
    ROOT_LOCATION = str(pathlib.Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).resolve())
    API_TYPE = "KakaoTranslation"
    main(ROOT_LOCATION, API_TYPE)