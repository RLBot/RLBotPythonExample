# https://stackoverflow.com/a/51704613
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain
try:
    import httplib
except:
    import http.client as httplib


# https://stackoverflow.com/a/24773951
def install_and_import(package):
    import importlib

    try:
        importlib.import_module(package)
    except ImportError:
        pipmain(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


# https://stackoverflow.com/questions/3764291/checking-network-connection
def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


if __name__ == '__main__':
    install_and_import('rlbot')
    from rlbot.utils import public_utils

    if not have_internet():
        print('NewConnectionError: unable to connect to install requirements.')  
    elif public_utils.is_safe_to_upgrade():
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
