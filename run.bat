@rem Change the working directory to the location of this file so that relative paths will work
cd /D "%~dp0"

@rem You will automatically get updates for all versions starting with "0.0.".
python -m pip install rlbot==0.0.* --upgrade

python -c "from rlbot import runner; runner.main();"
