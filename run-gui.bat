@echo off

@rem Change the working directory to the location of this file so that relative paths will work
cd /D "%~dp0"

@rem Make sure the environment variables are up-to-date. This is useful if the user installed python a moment ago.
call ./RefreshEnv.cmd

python -V >nul 2>&1 && (
    for /f "delims=" %%a in ('python -V') do @set pythonVer=%%a
    (echo %pythonVer% | findstr /i "3.6. 3.7." >nul) && (
        goto continue
    ) || (
        echo It appears that version of the installed Python is not supported.
        echo Please install version 3.6.5!
        goto end
    )
) || (
    echo Python was not found!
    echo If you recently installed Python reinstall it and check the "Add to PATH" during the installation.
    goto end
)
:continue

python run.py gui

:end
pause
