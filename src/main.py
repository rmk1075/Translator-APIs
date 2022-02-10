from translator.common import TranslatorFactory

import os
import pathlib
import traceback


def init_path(root):
    resource_path = "/".join([root, "resource"])
    if not os.path.exists(resource_path) or not os.path.isdir(resource_path):
        raise FileNotFoundError("error :: invalid resource path. resource_path={}".format(resource_path))

    input_path = "/".join([root, "input"])
    if not os.path.exists(input_path) or not os.path.isdir(input_path):
        raise FileNotFoundError("error :: invalid input path. input_path={}".format(input_path))

    output_path = "/".join([root, "output"])
    if not os.path.exists(output_path) or not os.path.isdir(output_path):
        print("info :: output directory is created. output_path={}".format(output_path))
        os.makedirs(output_path)

    return input_path, output_path, resource_path

def main(root=str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).resolve()), translator_type="PAPAGO"):
    try:
        input_path, output_path, resource_path = init_path(root)

        translator = TranslatorFactory.getTranslator(translator_type=translator_type, resource=resource_path)
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
    TRANSLATOR_TYPE = "GoogleTranslation"
    main(ROOT_LOCATION, TRANSLATOR_TYPE)