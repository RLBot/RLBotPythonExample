import sys

# https://stackoverflow.com/a/51704613
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

DEFAULT_LOGGER = 'rlbot'

if __name__ == '__main__':

    try:
        from rlbot.utils import public_utils, logging_utils

        logger = logging_utils.get_logger(DEFAULT_LOGGER)
        if not public_utils.have_internet():
            logger.log(logging_utils.logging_level,
                       'Skipping upgrade check for now since it looks like you have no internet')
        elif public_utils.is_safe_to_upgrade():
            pipmain(['install', '-r', 'requirements.txt', '--upgrade', '--upgrade-strategy=eager'])

            # https://stackoverflow.com/a/44401013
            rlbots = [module for module in sys.modules if module.startswith('rlbot')]
            for rlbot_module in rlbots:
                sys.modules.pop(rlbot_module)

    except ImportError:
        pipmain(['install', '-r', 'requirements.txt', '--upgrade', '--upgrade-strategy=eager'])

    try:
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
