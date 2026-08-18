---
title: Projects
type: page
permalink: /projects/
status: publish
author_profile: false
classes: portfolio-projects-page
description: "Selected backend, distributed systems, data, and machine learning projects by Kevin Chuang."
---
<div class="portfolio-page projects-page">
  <p class="portfolio-page__lead">Selected projects that explore distributed architecture, production-oriented backend services, data systems, and applied machine learning.</p>

  <section class="project-showcase" aria-labelledby="url-shortener-title">
    <div class="project-showcase__number">01</div>
    <div class="project-showcase__body">
      <p class="portfolio-eyebrow">Distributed systems · Team project</p>
      <h2 id="url-shortener-title">Yet Another URL Shortener</h2>
      <p class="project-showcase__problem">A URL platform designed to scale beyond a single service while supporting accounts, history, and popular-domain analytics.</p>
      <div class="project-details">
        <div><h3>What we built</h3><p>A React client backed by Go API microservices, deployed on AWS behind Kong and multiple load balancers.</p></div>
        <div><h3>Engineering decisions</h3><p>Applied the AKF Scale Cube and sharded MongoDB clusters to separate responsibilities and distribute load.</p></div>
      </div>
      <ul class="portfolio-tags"><li>Go</li><li>AWS</li><li>MongoDB</li><li>Kong</li><li>Docker</li><li>React</li></ul>
    </div>
  </section>

  <section class="project-showcase" aria-labelledby="summarizer-title">
    <div class="project-showcase__number">02</div>
    <div class="project-showcase__body">
      <p class="portfolio-eyebrow">Backend systems · NLP</p>
      <h2 id="summarizer-title">Text Summarizer Chrome Extension</h2>
      <p class="project-showcase__problem">A browser-based workflow for condensing long-form web content without leaving the page.</p>
      <div class="project-details">
        <div><h3>What I built</h3><p>A Chrome extension with a cloud-hosted summarization service, initially in Python and later rewritten in Go.</p></div>
        <div><h3>Engineering decisions</h3><p>Compared TextRank and Pointer-Generator approaches, separated the browser client from the service, and used Docker with Google App Engine for deployment.</p></div>
      </div>
      <ul class="portfolio-tags"><li>Go</li><li>Python</li><li>JavaScript</li><li>GCP</li><li>Docker</li><li>TextRank</li></ul>
      <a class="portfolio-text-link" href="https://github.com/k-chuang/tldr-extension-go">View source on GitHub <span aria-hidden="true">↗</span></a>
      <figure class="project-showcase__media">
        <video
          class="project-showcase__demo"
          data-lazy-video
          width="960"
          height="554"
          controls
          loop
          muted
          playsinline
          preload="none"
          poster="{{ '/assets/images/tldr-extension-go-demo-poster.webp' | relative_url }}"
          aria-label="Text Summarizer Chrome extension demo">
          <source data-src="{{ '/assets/images/tldr-extension-go-demo.webm' | relative_url }}" type="video/webm">
          <source data-src="{{ '/assets/images/tldr-extension-go-demo.mp4' | relative_url }}" type="video/mp4">
          <p>Your browser does not support embedded video. <a href="{{ '/assets/images/tldr-extension-go-demo.mp4' | relative_url }}">Download the demo</a>.</p>
        </video>
        <noscript><a href="{{ '/assets/images/tldr-extension-go-demo.mp4' | relative_url }}"><img src="{{ '/assets/images/tldr-extension-go-demo-poster.webp' | relative_url }}" width="960" height="554" loading="lazy" alt="Text Summarizer Chrome extension demo"></a></noscript>
        <figcaption>The extension summarizing content directly in the browser.</figcaption>
      </figure>
    </div>
  </section>

  <section class="project-showcase" aria-labelledby="emotion-title">
    <div class="project-showcase__number">03</div>
    <div class="project-showcase__body">
      <p class="portfolio-eyebrow">Applied machine learning · Graduate project</p>
      <h2 id="emotion-title">Emotional State Recognition</h2>
      <p class="project-showcase__problem">A system for recognizing emotional states using both facial expressions and body gestures.</p>
      <div class="project-details">
        <div><h3>What we built</h3><p>A team-developed, containerized deep learning application. I focused on training, testing, deployment, and model serving.</p></div>
        <div><h3>Engineering decisions</h3><p>Used TensorFlow Serving behind Flask and Docker to keep model inference separate from the application interface.</p></div>
      </div>
      <ul class="portfolio-tags"><li>Python</li><li>TensorFlow</li><li>Keras</li><li>Flask</li><li>Docker</li><li>OpenCV</li></ul>
    </div>
  </section>

  <section class="project-showcase" aria-labelledby="competitions-title">
    <div class="project-showcase__number">04</div>
    <div class="project-showcase__body">
      <p class="portfolio-eyebrow">Data science</p>
      <h2 id="competitions-title">Data Science Competitions</h2>
      <p class="project-showcase__problem">A collection of recommendation, classification, clustering, and text-mining problems evaluated on final leaderboards.</p>
      <div class="project-details">
        <div><h3>Results</h3><p>Placed 1st in book recommendation, 2nd in traffic-image classification, 3rd in news clustering, and 5th in medical-text classification.</p></div>
        <div><h3>Approach</h3><p>Worked through data analysis, feature engineering, model selection, validation, and metric-driven iteration in Python.</p></div>
      </div>
      <ul class="portfolio-tags"><li>Python</li><li>scikit-learn</li><li>SciPy</li><li>pandas</li><li>NumPy</li></ul>
      <a class="portfolio-text-link" href="https://github.com/k-chuang/data-science-competitions">View source on GitHub <span aria-hidden="true">↗</span></a>
    </div>
  </section>

  <section class="project-archive" aria-labelledby="archive-title">
    <p class="portfolio-eyebrow">Archive</p>
    <h2 id="archive-title">Earlier projects</h2>
    <p class="project-archive__intro">Smaller projects that mark earlier stages of my engineering path, preserved here without making them the focus of the portfolio.</p>
    <div class="project-archive__grid">
      <article><h3><a href="https://github.com/k-chuang/utopia-alexa-skill">Utopia Alexa Skill</a></h3><p>A serverless Alexa skill built with Python, AWS Lambda, automated tests, and continuous integration.</p></article>
      <article><h3><a href="https://github.com/k-chuang/automate-download-freesound">Freesound CLI Scraper</a></h3><p>A tested Python and Selenium tool that automated downloads of audio files and associated metadata.</p></article>
      <article><h3>Save Sister Script</h3><p>A Python and Selenium utility that monitored medical-exam availability and sent an email when an earlier appointment opened.</p></article>
    </div>
  </section>
</div>

<script src="{{ '/assets/js/lazy-video.js' | relative_url }}" defer></script>
