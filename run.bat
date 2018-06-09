@echo off

@rem Change the working directory to the location of this file so that relative paths will work
cd /D "%~dp0"

setlocal EnableDelayedExpansion

@rem Run the is_safe_to_upgrade function and save the output to a temp file.
python -c "from rlbot.utils import public_utils; print(public_utils.is_safe_to_upgrade());" > %temp%\is_safe_to_upgrade.txt

IF %ERRORLEVEL% NEQ 0 (
    @rem The python command failed, so rlbot is probably not installed at all. Safe to 'upgrade'.
    set is_safe_to_upgrade=True
) ELSE (
    @rem read the file containing the python output.
    set /p is_safe_to_upgrade= < %temp%\is_safe_to_upgrade.txt
)
del %temp%\is_safe_to_upgrade.txt

IF "!is_safe_to_upgrade!"=="True" (
    @rem You will automatically get updates for all versions starting with "0.0.".
    python -m pip install rlbot==0.0.* --upgrade
) ELSE (
    echo Will not attempt to upgrade rlbot because files are in use.
)

python -c "from rlbot import runner; runner.main();"
