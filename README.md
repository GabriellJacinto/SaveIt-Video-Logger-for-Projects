# SaveIt: Personal Video Logger

<div align="center">

![PyPI](https://img.shields.io/pypi/v/customtkinter)
![PyPI - Downloads](https://img.shields.io/pypi/dm/customtkinter?color=green&label=downloads)
![Downloads](https://static.pepy.tech/personalized-badge/customtkinter?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads)
![PyPI - License](https://img.shields.io/pypi/l/customtkinter)
![](https://tokei.rs/b1/github/tomschimansky/customtkinter)
![Mozilla Add-on](https://img.shields.io/amo/dw/teste)
</div>

Automation for video logging progress and reflexions about goals, projects, and research (Gojects). Kinda like the characters on the first avatar movie. Notion integration WIP.


<img src="./utils/example.JPG" alt="Main Menu">

## 💻 Requirements

Before downloading, certify that you have the following requirements:
* You have the most recent version of `python`
* Your operating system is `Windows` based. (Pygrabber uses COMTypes, which is designed for Windows, not Linux)

## 🚀 Installing SaveIt: Personal Video Logger

To run SaveIt: Personal Video Logger, run the following commands:

```
pip install -r requirements.txt
```

Lauching the application:

```
python3 main.py
```
## Current Version: 1.2.1

This software is on realese 1.2. The current version is capable of:

<details>
<summary>Version 1.1.* Features</summary>

- [x] Execution by command line (see [Installation](#🚀-Installing-SaveIt:-Personal-Video-Logger))
- [x] Manage Goals and Projects:
  - [x] Edit Gojects Window
    - [x] Create Gojects
    - [x] Delete Gojects
    - [x] Edit Gojects
    - [x] Save Gojects
  - [X] Select Gojects to record
    - [x] Create custom widget to aggragate information of recording progress
    - [x] Show custom widgets on the right sidebar
- [x] Recording:
  - [x] Quick Log Recording (less than one minute)
    - [x] Custom widget to set timer duration as a dial
  - [x] Long Log Recording (more than one minute)
    - [x] Custom widget to set timer duration as a dial
  - [x] Folder manager 

</details>

<details open>
<summary>Version 1.2.* Features</summary>

- [ ] Execution by executable
- [ ] Notion API integration:
  - [ ] Basic report of completed tasks (show name and its project/goal)
  - [ ] Automatic selection upon clicking quicklog (longlog will remain as manual selection)
- [ ] Code optimization:
  - [ ] CRUD functions optimizations of GojectEditWindow class
  - [ ] Reimplementation of top level windows and Gojects widgets with inheretance and abstract classes
- [ ] Gojects:
  - [ ] Add attribute of parent/child goject
  - [ ] Create visual representation of parent/child goject (as a pathway visualizer)
- [ ] Video Player:
  - [ ] Show option to watch/listen to the last quicklog or longlog recorded
  - [ ] Integration with [mindfulness at the computer](https://gitlab.com/mindfulness-at-the-computer/mindfulness-at-the-computer) to play animations
- [ ] Recording:
  - [x]  Add Recording info on the screen while recording and on the saved file
  - [ ] Select devices on the main page
    - [x] Camera
    - [ ] Microphone 
  - [ ] Show recording on the main menu (currently opens up another window)
    - [x] Create progress bar for the whole duration of the log
    - [ ] Create button to stop current log and go to next one
    - [ ] Create button to go to next section of current log
    - [ ] Create button to stop recording
  - [ ] Create sections for each log during recording (not restricted to):
    - [ ] Introduction
    - [ ] Reflexion
    - [ ] Conclusion
- [ ] Log Data Processing
  - [ ] Audio Transcription
  - [ ] Computer Vision Sentiment Analysis
  - [ ] Log Manager Window:
    - [ ] Compile Logs
    - [ ] Compress Logs Compilation
    - [ ] Clean Logs Older Than 6 months
    - [ ] Generate Report with overall sentiment and summary of reflexions
</details>


<details>
<summary>Version 1.3.* Features</summary>

- [ ] Video Player:
  - [ ] Create class to play recording on the main menu:
    - [ ] Select and play older logs
    - [ ] Play any video
- [ ] Notion API integration
  - [ ] Import
  - [ ] Edit and Save

</details>

## 📝 License

See [License](LICENSE) for more information.

[⬆ Back to the top](#SaveIt:-Personal-Video-Logger)<br>

