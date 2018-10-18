# https://stackoverflow.com/a/51704613
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain


# https://stackoverflow.com/a/24773951
def install_and_import(package):
    import importlib

    try:
        importlib.import_module(package)
    except ImportError:
        pipmain(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


if __name__ == '__main__':
    install_and_import('rlbot')
    from rlbot.utils import public_utils

    if public_utils.is_safe_to_upgrade():
        pipmain(['install', '-r', 'requirements.txt', '--upgrade', '--upgrade-strategy=eager'])

    try:
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == 'gui':
            from rlbot.gui.qt_root import RLBotQTGui
            RLBotQTGui.main()
        else:
            from rlbot import runner
            runner.main()
    except Exception as e:
        print("Encountered exception: ", e)
        print("Press enter to close.")
        input()
