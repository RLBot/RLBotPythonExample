import os
import sys


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

    root_path = os.path.dirname(os.path.dirname(path))
    sys.path.insert(0, root_path)  # this is for first process imports

    import run
    run.main()
