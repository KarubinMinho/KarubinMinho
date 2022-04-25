from pathlib import Path
import shutil
import random
# import re


def check_exist(path):
    """
    :param path: list of Path objects ot Path obj
    :return:
    """
    # if got a Path obj, convert to list
    if isinstance(path, Path):
        path = [path]
    for p in path:
        if p.exists():
            shutil.rmtree(p)

def create_filename():
    """
    :return: random 4 bit '[a-z]'.lower()
    """
    lower_list = [chr(97+i) for i in range(26)]
    filename = random.choices(lower_list, k=4)
    return ''.join(filename)

def touch_file(dirname):
    """
    :param dirname: Path objects
    :return: None
    """
    return {(dirname / create_filename()).touch() for _ in range(50)}

def ignore(src, names):
    """
    :param src:
    :param names: os.listdir(src)
    :return: set of ingore names
    """
    # 1.
    # s = set()
    # for name in names:
    #     print(src, type(src), name, type(name))
    #     if not re.match('[x-z]', name) and (Path(src) / name).is_file():
    #         s.add(name)
    # 2.
    # s =  {name for name in names if not re.match('[x-z]' and (Path(src) / name).is_file(), name)}
    # ignore_names = set(filter(lambda x: not re.match('[x-z]', x) and (Path(src) / x).is_file(), names))
    # S.startswith(prefix[, start[, end]]) -> bool
    # prefix can be a tuple
    ignore_names = set(filter(lambda x: not x.startswith(('x', 'y', 'z')) and (Path(src) / x).is_file(), names))
    return ignore_names


if __name__ == '__main__':
    src = Path('D:/temp')
    dst = Path('D:/dst')
    # rmtree if check_exist
    check_exist([src, dst])

    # touch_files
    src_dirs = src / 'a/b/c/d'
    src_dirs.mkdir(parents=True) #, exist_ok=True)
    dirnames = list(src_dirs.parents)[0:3]
    dirnames.append(src_dirs)
    for p in dirnames:
        touch_file(p)

    # copytree; not contain dir:a
    shutil.copytree((src / 'a'), dst, ignore=ignore)
