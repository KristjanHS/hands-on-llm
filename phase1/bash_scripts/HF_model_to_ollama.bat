@echo off
REM -------------------------------------------------------------------
REM === HF Model to Ollama Import Script ===
REM This script fetches a model from Hugging Face & packages it for Ollama.
REM Prerequisites (install first):
REM   • huggingface-cli (v0.16+)
REM   • curl (Win10 built-in or via Git Bash)
REM   • ollama
REM Usage:
REM   import_ollama_model.bat <huggingface-repo-path>
REM   e.g. import_ollama_model.bat bartowski/Mistral-7B-Instruct-v0.3-GGUF
REM -------------------------------------------------------------------

setlocal ENABLEDELAYEDEXPANSION

REM -------------------------------------------------------------------
REM 1) Validate input argument (repo path)  
REM -------------------------------------------------------------------
if "%~1"=="" (
  echo Usage: %~nx0 huggingface-repo-path
  exit /b 1
)
set "REPO=%~1"

REM -------------------------------------------------------------------
REM 2) Download the model index (tree) JSON from Hugging Face API  
REM -------------------------------------------------------------------
echo Fetching file list from %REPO% ...
curl -s https://huggingface.co/api/models/%REPO%/tree/main > model.json

REM -------------------------------------------------------------------
REM 3) Parse out all “.gguf” file paths into files.txt  
REM    Using FINDSTR to pick lines containing .gguf and FOR to extract
REM -------------------------------------------------------------------
for /f "tokens=2 delims=:" %%A in (^
  'findstr /r "\"path\".*\.gguf\"" model.json'^) do (
  set "line=%%~A"
  REM strip trailing commas and quotes
  set "line=!line:,=!"
  set "line=!line:"=!"
  echo !line!
) > files.txt

if not exist files.txt (
  echo No .gguf files found.
  del model.json
  exit /b 1
)

REM -------------------------------------------------------------------
REM 4) Display a numbered menu of available .gguf files  
REM    Store each filename in an environment array for selection  
REM -------------------------------------------------------------------
echo.
echo Available .gguf files:
set /a IDX=0
for /f "usebackq delims=" %%F in ("files.txt") do (
  set /a IDX+=1
  echo !IDX!) %%F
  set "FILE[!IDX!]=%%F"
)

REM -------------------------------------------------------------------
REM 5) Prompt user to choose which .gguf to download  
REM    Loop until a valid number is entered  
REM -------------------------------------------------------------------
:select
set /p CHOICE=Enter number to download: 
call set "FILENAME=%%FILE[%CHOICE%]%%"
if "%FILENAME%"=="" (
  echo Invalid choice. Try again.
  goto select
)
echo Selected: %FILENAME%

REM -------------------------------------------------------------------
REM 6) Prepare target directory name by stripping “.gguf” and replacing slashes  
REM -------------------------------------------------------------------
set "BASENAME=%FILENAME:.gguf=%"
set "BASENAME=%BASENAME:/=-%"
set "DIR=ollama-%BASENAME%"
mkdir "%DIR%" 2>nul

REM -------------------------------------------------------------------
REM 7) Download the chosen .gguf via Hugging Face CLI  
REM    Then write a Modelfile, build & run via ollama  
REM -------------------------------------------------------------------
echo Downloading model file...
huggingface-cli download %REPO% --include %FILENAME% --local-dir "%DIR%" --local-dir-use-symlinks False ^
  && echo Creating Modelfile... ^
  && (
       echo FROM ./%FILENAME%
       echo TEMPLATE ^"<s>[INST] {{ .Prompt }} [/INST]</s>^"
       echo PARAMETER stop "[/INST]"
       echo PARAMETER stop "</s>"
     ) > "%DIR%\Modelfile" ^
  && echo Building model... ^
  && ollama create %BASENAME% -f "%DIR%\Modelfile" ^
  && echo Running model... ^
  && ollama run %BASENAME%

REM -------------------------------------------------------------------
REM 8) Clean up temporary JSON and listing file, end delayed expansion  
REM -------------------------------------------------------------------
del model.json files.txt
endlocal
