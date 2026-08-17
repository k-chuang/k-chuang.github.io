---
title: Programming Utopia, an Alexa skill
date: 2018-06-05 20:33:40.000000000 -07:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- Projects
tags:
- Alexa
- Codecov
- Python
- Travis CI
- Utopia
meta:
  _wpcom_is_markdown: '1'
  _rest_api_published: '1'
  timeline_notification: '1528256023'
  _rest_api_client_id: "-1"
  _publicize_job_id: '18655361981'
  _thumbnail_id: '186'
permalink: "/2018/06/05/programming-utopia-an-alexa-skill/"
---
According to the&nbsp;[World Health Organization](http://www.who.int/mediacentre/factsheets/fs369/en/), 350 million people worldwide suffer from depression. Depression is the leading cause of disability.

> More than&nbsp;[16 million American adults](https://adaa.org/understanding-anxiety/depression), or 6.7% of the adult population, have experienced at least one major depressive episode in the last year.
>
> - Anxiety and Depression Association of America.

Recently, there has been a spike in the rise of suicides in the United States. In the past week, two celebrities (Anthony Bourdain and Kate Spade) committed suicide due to depression. There is a need for more ways that victims of depression can get help. This is the motivation behind why I created Utopia.


This blog post will be about a project I've been working on for the past couple of months. Using Python, some third party Python packages, and the Alexa Skills kit, I programmed [Utopia](https://github.com/k-chuang/utopia-alexa-skill), an Alexa skill that is designed to help people cope with depression.

**[UPDATE 06/07/2018]** After a couple iterations with the Alexa Skills team, I am happy to say that Utopia is now live and available in the Alexa Skill store and can be accessed via this link:&nbsp;[Utopia Alexa skill](https://www.amazon.com/Kevin-Chuang-Utopia/dp/B07CZWS8B2)&nbsp;or by simply saying, `​​"Alexa, start happy place"` to any Alexa supported device.

**Disclaimer** : Utopia is not meant to be a substitute for professional medical advice, treatment or diagnosis. It is more of a supplemental and informational helper to mitigate depression. The person who programmed this are not experts in mental illnesses such as depression, and this is a product of our subjectivity and couple months of research on depression.

The GitHub Page for this project is located here:&nbsp;[Utopia GitHub Page](https://k-chuang.github.io/utopia-alexa-skill/).

The GitHub Repo is located [here](https://github.com/k-chuang/utopia-alexa-skill/).

## Description

This skill is meant to help people who are going through depression. The main feature of this skill involves taking the&nbsp;[Hamilton Depression Rating Scale Survey](https://www.psychcongress.com/saundras-corner/scales-screeners/depression/hamilton-depression-rating-scale-ham-d)&nbsp;to get a general idea of the severity of depression, and based on the score of the survey, the skill would recommend certain natural remedies to help. The other complementary features include giving positive and motivational quotes (other types of quotes are also supported), proposing natural solutions, a mindfulness meditation exercise, recommendations for nearby therapists, and, if necessary, getting help from the National Suicide Prevention Lifeline.

## Architecture

[View the Utopia source and architecture on GitHub.](https://github.com/k-chuang/utopia-alexa-skill)

## Features

- [Hamilton Depression Rating Scale Survey](https://www.psychcongress.com/saundras-corner/scales-screeners/depression/hamilton-depression-rating-scale-ham-d)&nbsp;consisting of 16 questions to analyze and evaluate level of depression.
  - Added three bonus questions that uses&nbsp;[NLTK](http://www.nltk.org/)&nbsp;sentiment analysis to contribute to the survey score.
- Listen to different categories of quotes from&nbsp;[BrainyQuote](https://www.brainyquote.com/)
  - A few popular categories of quotes include positive, motivational, inspirational, family, love, and positive.
- Listen to advice and ideas for activities to improve mood
  - Examples include:
    - _Listen to music that makes you feel good._
    - _Take note of all the small things you've accomplished today._
- Listen to a collection of uplifting & powerful poems
- Recommend therapists nearby using&nbsp;[Google Places API](https://developers.google.com/places/)&nbsp;by providing contact information, current availability, and open hours
  - Will find nearby available therapists, and if there are no open therapists nearby, will default to all nearby therapist places (open or closed)
- [National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/)
  - If certain trigger words are said, this feature will automatically trigger and provide user with contact information for the suicide hotline.
  - For a full list of trigger words, see&nbsp;[Trigger Words](https://github.com/k-chuang/utopia-alexa-skill/blob/master/speech_assets/custom_slot_types/TriggerWords.txt)

## Usage

Different from the skill name, the _invocation name_ is 'happy place'.

To start using it, say a simple invocation phrase, such as the following listed below:

| Starting Phrase | Example |
| --- | --- |
| \<invocation name\> | Alexa, happy place |
| Launch \<invocation name\> | Alexa, Launch happy place |
| Open \<invocation name\> | Alexa, Open happy place |
| Start \<invocation name\> | Alexa, Start happy place |

To start and hear the available features, you can say the following:

```
Alexa, ask happy place for available features
```

## Testing & Code Coverage

To run tests and check code coverage, run the following command in the root project folder:

```source
$ pytest tests/test\_utopia\_unit.py -v —cov utopia —cov-report term-missing
```

This command will execute the tests and check for test code coverage of the main program ([utopia.py](https://github.com/k-chuang/utopia-alexa-skill/blob/master/utopia.py)), and report which lines were not covered by the test suite ([test\_utopia\_unit.py](https://github.com/k-chuang/utopia-alexa-skill/blob/master/tests/test_utopia_unit.py)).

### Travis CI&nbsp; [![Build Status](https://travis-ci.org/k-chuang/utopia-alexa-skill.svg?branch=master)](https://travis-ci.org/k-chuang/utopia-alexa-skill)

This project uses&nbsp;[Travis-CI](https://travis-ci.org/), a hosted, distributed continuous integration service that builds and tests software hosted on GitHub. Every commit that is pushed to a GitHub repo automatically triggers&nbsp;[Travis CI](https://travis-ci.org/)&nbsp;to run, build and test your software.

The continuous integration configuration is specified in&nbsp;[.travis.yml](https://github.com/k-chuang/utopia-alexa-skill/blob/master/.travis.yml)&nbsp;file, and specifies the programming language used, desired building and testing environments, and various other parameters. For this project, the configuration is set up to create environment variables, install necessary dependencies, run the test suite, and after a successful test run, report code coverage.

[Travis CI](https://travis-ci.org/)&nbsp;generates a badge with the current build status (displayed above). Click on the badge for more information.

### Codecov&nbsp; [![codecov](https://codecov.io/gh/k-chuang/utopia-alexa-skill/branch/master/graph/badge.svg)](https://codecov.io/gh/k-chuang/utopia-alexa-skill)

This project uses&nbsp;[Codecov](https://codecov.io/)&nbsp;to generate code coverage reports.&nbsp;[Codecov](https://codecov.io/)&nbsp;is a free, open source code coverage reporting tool that integrates seamlessly with GitHub. It calculates and measures code coverage and delivers the coverage metrics in a clear, understandable way. Similar to Travis CI,&nbsp;[Codecov](https://codecov.io/)&nbsp;also generates a clickable badge (displayed above) with the current code coverage metrics.

&nbsp;
