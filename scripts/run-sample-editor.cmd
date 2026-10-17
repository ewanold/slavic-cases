@echo off
setlocal
if defined SAMPLE_EDITOR_PYTHON (
  "%SAMPLE_EDITOR_PYTHON%" "%~dp0..\tools\sample_editor\app.py" %*
) else if exist "%LOCALAPPDATA%\LearnGrammaticalCases\sample-editor-venv\Scripts\python.exe" (
  "%LOCALAPPDATA%\LearnGrammaticalCases\sample-editor-venv\Scripts\python.exe" "%~dp0..\tools\sample_editor\app.py" %*
) else (
  py -3.12 "%~dp0..\tools\sample_editor\app.py" %*
)
if errorlevel 1 (
  echo See tools\sample_editor\README.md for setup instructions.
  pause
)
