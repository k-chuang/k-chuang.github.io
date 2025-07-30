---
title: "Projects"
type: page
permalink: /projects/
status: publish
author_profile: true
# entries_layout: grid
# classes: wide
---
## [Text Summarizer Chrome Extension](https://github.com/k-chuang/tldr-extension-go)
- Researched various text summarization methods (TextRank, Pointer Generator) and created a cloud-native text summarizer application consisting of Chrome Extension (Javascript / HTML / CSS) with Python backend server deployed on Google App Engine using Docker
- Rewrote backend server in Golang for better performance
- **Tools:** Python, Golang, Javascript, GCP, Docker, TextRank

![text summarizer demo](/assets/images/tldr-extension-go-demo.gif)

## [Understanding Emotional States from Body Language using Deep Learning]()
- For SJSU Master's Project, collaborated with team to launch containerized deep learning model to recognize emotional states using face and body gestures
- Focused on training, testing, deploying, and serving the deep learning model using Keras, Tensorflow, Tensorfow serving, Flask, Docker, opencv
- **Tools:** Python, Flask, Keras, Tensorflow, Tensorflow serving, Docker, opencv

<!-- ![emotional states architecture](/assets/images/emotional_recognition_system_architecture.png) -->

## [Yet Another URL Shortener](https://github.com/nguyensjsu/fa19-281-team-red-1)
- Collaborated with team in hackathoon to design & implement microservice architecture satisfying AKF Scale Cube with React.js frontend, Kong API Gateway, multiple load balancers, Golang API microservices, and MongoDB clusters hosted on AWS for shortening URLs with additional features like user profile and user history and most popular domains
- **Tools:** Golang, AWS, MongoDB, React.js, Kong API Gateway, Docker

## [Data Science Competitions](https://github.com/k-chuang/data-science-competitions)
- Ranked **1st** in book recommender system, **2nd** in traffic image classification, **3rd** in news article text clustering, and **5th** in medical text classification in the final leaderboard of data science competitions at SJSU
- **Tools:** Python, scipy, pandas, numpy, seaborn, scikit-learn, surprise

## [Save Sister Script]()
- Wrote Python script to automatically check medical exam scheduling website and alert my sister via email when the earliest available medical exam time slot was available, resulting in a lot of saved time repeatedly manually refreshing the website and successfully getting her an early medical exam time slot (which she also successfully passed!)
- **Tools**: Python, Selenium

## [Utopia Alexa Skill](https://github.com/k-chuang/utopia-alexa-skill)
- Developed and launched a serverless Alexa skill to help people with depression
- **Tools:** Python, Alexa Skills Kit, AWS Lambda, Travis CI, Codecov, pytest

## [Freesound CLI Web Scraper](https://github.com/k-chuang/automate-download-freesound)
- Developed a web scraper to automate downloading audio files & associated metadata from website freesound.org
- **Tools:** Python, Selenium, Travis CI, Coveralls, pytest