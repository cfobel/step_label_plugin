set ARCHIVE_FILE=%PKG_NAME%.zip
set MICRODROP_PLUGINS_DIR=%PREFIX%\share\microdrop\plugins\available
set PROPERTIES_FILE=%MICRODROP_PLUGINS_DIR%\%PKG_NAME%\properties.yml

@echo off
:: Make library directory (and parent directories, if necessary).
setlocal enableextensions
md "%MICRODROP_PLUGINS_DIR%"
endlocal

REM Export git archive, which substitutes version expressions in `_version.py`
REM to reflect the state (i.e., revision and tag info) of the git repository.
git archive -o %ARCHIVE_FILE% --prefix %PKG_NAME%/ HEAD
if errorlevel 1 exit 1
REM Extract exported git archive to Conda MicroDrop plugins directory.
"%PREFIX%"\Library\bin\7za -o"%MICRODROP_PLUGINS_DIR%" x %ARCHIVE_FILE%
if errorlevel 1 exit 1
REM Delete Conda build recipe from installed package.
rmdir /S /Q "%MICRODROP_PLUGINS_DIR%\%PKG_NAME%\.conda-recipe"
if errorlevel 1 exit 1
REM Delete Conda build recipe from installed package.
del "%MICRODROP_PLUGINS_DIR%\%PKG_NAME%\.git*"
if errorlevel 1 exit 1

REM Write package information to (legacy) `properties.yml` file.
"%PYTHON%" -c "import os; os.chdir(r'%MICRODROP_PLUGINS_DIR%/%PKG_NAME%'); import yaml; import _version as v; yaml.dump({'package_name': '%PKG_NAME%', 'plugin_name': '%PKG_NAME%', 'version': v.get_versions()['version'], 'versioneer': v.get_versions()}, open(r'%PROPERTIES_FILE%', 'w'), default_flow_style=False)"
