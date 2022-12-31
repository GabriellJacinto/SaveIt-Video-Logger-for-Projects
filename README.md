# projects-video-log
Automantion for video logging progress and reflexions about goals, projects, and research (Gojects). Kinda like the characters on the first avatar movie. Notion integration WIP.

## Current Version: 0.1

This software is a work in progress.

### Version 1.1 Features

The current version is capable of:

- [x] Execution by command line (see [Execution](#execution))
- [] Manage Goals and Projects:
  - [x] Create Gojects
  - [x] Delete Gojects
  - [x] Edit Gojects
  - [x] Save Gojects
  - [] Select Gojects to record
    - [] Create custom widget to aggragate information of recording progress
    - [] Show custom widgets on the right sidebar
- [x] Recording:
  - [x] Quick Log Recording (less than one minute)
    - [] Custom widget to set timer duration as a dial
  - [x] Long Log Recording (more than one minute)
    - [] Custom widget to set timer duration as a dial
  - [x] Folder manager 

### Version 1.2 Features
- [] Execution by executable
- [] Recording:
  - [] Show recording on the main menu (currently opens up another window)
    - [] Create progress bar for the whole duration of the log
    - [] Create button to stop current log and go to next one
    - [] Create button to go to next section of current log
    - [] Create button to stop recording
  - [] Create sections for each log (not restricted to):
    - [] Introduction
    - [] Reflexion
    - [] Conclusion
- [] Log Data Processing
  - [] Audio Transcription
  - [] Computer Vision Sentiment Analysis
  - [] Log Manager:
    - [] Compile Logs
    - [] Compress Logs Compilation
    - [] Clean Logs Older Than 6 months
    - [] Generate Report with overall sentiment and summary of reflexions

### Version 1.3 Features
- [] Playing:
  - [] Create class to play recording on the main menu:
    - [] Select and play older logs
    - [] Play other videos
- [] Notion API integration
  - [] Import
  - [] Edit and Save


## Execution

To install dependencies, run the command below

```
pip install requirements.txt
```
### Run application

```
python3 main.py
```
