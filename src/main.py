import os
import pathlib

def main(root=str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())):
    if not os.path.exists(root) or not os.path.isdir(root):
        print("warning :: invalid root path. root={}".format(root))
        return

    for file_name in os.listdir(root):
        file_path = os.path.join("/", root, file_name)
        print(file_path)
        if os.path.isdir(file_path):
            continue

        if file_path.split(".")[-1] != "txt":
            continue
        
        with open(file_path, "r") as file:
            for line in file.readlines():
                print(line)

if __name__ == "__main__":
    # constant
    DIR_LOCATION = str(pathlib.Path(os.path.join("/", os.path.dirname(os.path.abspath(__file__)), "../resource")).resolve())
    main(DIR_LOCATION)