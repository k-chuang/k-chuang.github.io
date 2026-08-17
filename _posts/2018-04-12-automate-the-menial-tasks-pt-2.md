---
title: Automate the Menial Tasks Pt.2
date: 2018-04-12 17:10:26.000000000 -07:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- Projects
tags:
- CLI
- Coveralls
- Python
- Selenium
- Travis CI
meta:
  _wpcom_is_markdown: '1'
  timeline_notification: '1523578229'
  _rest_api_published: '1'
  _rest_api_client_id: "-1"
  _publicize_job_id: '16741018740'
permalink: "/2018/04/12/automate-the-menial-tasks-pt-2/"
---
This is part 2 (and the final part) of the automating the menial tasks mini-series. I will be talking about using Python and Selenium to automate downloading audio files from a free audio database called [Freesound](https://freesound.org/). This was an old project that I had worked on when I was first getting into programming in Python. Recently, I revisited the code, since I remember it being such a cool and exciting project. I wanted to make it even better, so I spent some time refactoring the old, messy, and unPythonic code into a more understandable, clean CLI (Command Line Interface) application.

In addition to refactoring the code, I also started writing some unit tests and test cases to test the newly refactored code and the application as a whole. It was my first time writing unit tests and test cases for testing code, and it was such an awesome and fulfilling experience! I learned about a bunch of cool Python test frameworks and libraries ([pytest](https://docs.pytest.org/en/latest/), [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/), [unittest](https://docs.python.org/2/library/unittest.html)), an open source, hosted continuous integration service called [travis-ci](http://travis-ci.org), and&nbsp;a coverage statistic web service that publishes and tracks your code coverage stats online called [coveralls.io](http://coveralls.io).

Both **travis-ci** and **coveralls.io** sync with GitHub, so every commit to a GitHub repo will trigger a new build, and generate updated code coverage stats. Also, these two services&nbsp; both provide a nice dynamic badge icon that represents the status of your current build ( **travis-ci** ) or displays the current percentage of code coverage ( **coveralls.io** ).

The two dynamic and clickable icons that are on my GitHub are located here. Click them if you are interested in seeing the up-to-date details and status of my build on travis-ci and the code coverage stats on coverage.io:

[![Build Status](https://travis-ci.org/k-chuang/automate-download-freesound.svg?branch=master)](https://travis-ci.org/k-chuang/automate-download-freesound)

[![Coverage Status](https://coveralls.io/repos/github/k-chuang/automate-download-freesound/badge.svg?branch=master)](https://coveralls.io/github/k-chuang/automate-download-freesound?branch=master)

The Python code for this project can be found on my GitHub along with the cool badge icons shown above, courtesy of **travis-ci** and **coveralls.io** :

[Freesound Downloader](https://github.com/k-chuang/automate-download-freesound)

## Setting Up

Install chromedriver via brew or from the&nbsp;[Google site](https://sites.google.com/a/chromium.org/chromedriver/downloads), and set the location of the chromedriver on your SYSTEM PATH.

I installed the chromedriver via&nbsp;[brew](https://brew.sh/) (command is below), and naturally, brew installs packages to /usr/local/bin, which is already in the $PATH, so that is pretty convenient. You can always do an echo $PATH to make sure that /usr/local/bin is in it, and if it's not in your $PATH variable, then export it by editing either ~/.bash\_profile or /etc/paths/.

```
$ brew install chromedriver
```

After installing the chromedriver, here is rest of the setup:

```
$ git clone https://github.com/k-chuang/automate-download-freesound.git
$ cd automate-download-freesound
$ virtualenv -p /usr/bin/python2.7 venv
$ source venv/bin/activate
$ pip install -r dev-requirements.txt
$ pytest
```

Also, you will need to create a free account on [Freesound](http://freesound.org) in order to download files.

## How to Use

Run the command below for more information regarding the arguments (positional or optional, default values, description, etc.)

```
$ python automate_download_freesound.py --help
```

There is one required argument, and that is the desired sounds you wish to download from&nbsp;[Freesound](http://freesound.org/). You may list more than one sound, but make sure to separate each one by commas, and if the sound you want to download includes spaces, please put quotation marks around it to ensure a smooth experience. Also, make sure it is the first argument after the script. Example:

```
$ python automate_download_freesound.py "dogs barking,cats purring"
```

There are more features and arguments, including download path, file format, sample rate, and advanced filtering. These are all optional arguments, and can help with filtering for your specific needs.

Here is another example, where all the optional arguments are specified:

```
$ python automate_download_freesound.py "baby crying,smoke alarm" --download-dir /Users/KevinChuang/Desktop --file-format wav --sample-rate 48000 --advanced-filter True
```

This command will download 'baby crying' and 'smoke alarm' wav files with a sampling rate of 48000 from [Freesound.org](http://freesound.org).

Here are brief descriptions of each of the arguments, and some sample parameters:

| Argument | Type | Description |
| --- | --- | --- |
| sound | required | a list of sounds (or just one sound) separated by commas (if multiple), and enclosed in parenthesis |
| ––download-dir | optional | a string literal with a path to the download folder you wish to download files to. The default value for this argument is your respective 'Downloads' folder. This works for both MacOS and Windows environment. |
| ––file-format | optional | a string literal with the desired audio file format extension of the downloaded files. Default will be all available audio file formats with no filtering. Choices include wav, ogg, mp3, m4a, aiff, and flac. |
| ––sample-rate | optional | a integer with the desired sample rate of the downloaded files. Default will be all available sample rates with no filtering. Choices include 11025, 16000, 22050, 44100, 48000, 88200, and 96000. |
| ––advanced-filter | optional | a boolean value (True or False) that initiates advanced filtering to limit audio files based on search query. The advanced filter will limit the audio files based on the search query found in tags, filenames, and file descriptions. |

## Conclusion

Thus concludes the "Automate the Menial Tasks" mini series. I had a lot of fun working on this old project, and I learned a lot from refactoring it, like how to write sophisticated and complete tests for Python applications. I want to give one last shout out to the two open source and easy to use services that I used in this project:&nbsp;[travis-ci](http://travis-ci.org) & [coveralls.io](http://coveralls.io). I highly recommend checking those two services out.

Again, you can check out my GitHub repo of this project here: [Freesound Downloader](https://github.com/k-chuang/automate-download-freesound)
