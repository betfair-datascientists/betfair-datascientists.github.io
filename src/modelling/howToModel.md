# Intro to modelling

Want to learn how to create your own predictive model using sports or racing data, but you don’t know where to start? We’re here to help.

The Data Scientists at Betfair have put together the first few steps we suggest you take to get you started on your data modelling journey. We also run occasional data modelling workshops to help you get the basics down – [reach out and let us know](mailto:bdp@betfair.com.au) if you’re interested in being notified about upcoming data events.

---
## Choose your language

There are lots of programming languages to choose from. For our data modelling workshops we work in R and Python, as they’re both relatively easy to learn and designed for working with data.

If you’re new to these languages, here are some resources that will help get you set up.

### Language 1: R

- [What is R?](https://www.r-project.org/about.html)
- [Download and install R](https://cran.ms.unimelb.edu.au/) – get the language set up on your computer
- [Download and install RStudio](https://www.rstudio.com/) – you’ll need a program to develop in, and this one is custom-designed to work with R
- Take a look at the some of the existing R libraries you can use if you want to connect to our API, including [abettor](https://github.com/phillc73/abettor) and our [Data Scientists’ R repo](/api/apiRtutorial.md).


### Language 2: Python

- [What is Python?](https://www.python.org/)
- [Download and install Anaconda Distribution](https://www.anaconda.com/download/) – this will install Python and a heap of data science packages along with it

---
## Find a data source

Finding quality data is crucial to being able to create a successful model. We have lots of [historical Exchange data](https://www.betfair.com.au/hub/education/betfair-advanced/historical-data-sources/) that we’re happy to share, and there are lots of other sources of sports or racing specific data available online, depending on what you’re looking for.

For our workshops we use historical NBA odds data from the Exchange ([which you can download directly from here](/modelling/assets/BetfairNBAOdds.csv), along with NBA game data from a variety of sources including:

- [ESPN.com](http://www.espn.com/nba/)
- [NBA.com](http://stats.nba.com/)
- [basketball-reference.com](https://www.basketball-reference.com/)
- [Stattleship’s API](https://api.stattleship.com/)

---
## Learn to Program

Okay, so easier said than done, but you don't actually need a high level of programming knowledge to be able to build a decent model, and there are so many excellent resources available online that the barrier to entry is much lower than it's been in the past.

These are some of our favourites if you want to learn to use R or Python for data modelling:

- [Dataquest](https://www.dataquest.io/) – free coding resource for learning both Python and R for data science
- [Datacamp](https://www.datacamp.com/) – another popular free resource to learn both R and Python for data science
- [Codeacademy](https://www.codecademy.com/) – free online programming courses with community engagement

We've also shared a [R repo for connecting with our API](/../api/apiRtutorial), which might make that part of the learning process easier for you, if you go down that path.

---
## Learn how to model data

We’ve put together some articles to give you an introduction to some of the different approaches you can take to modelling data, but again there are also lots of resources available online. Here are some good places to start:

- Work through the modelling tutorials we've put together using [AFL](/modelling/AFLmodellingPython/) and [soccer](/modelling/soccerEloTutorialR/) data
- This [Introduction to Tennis Modelling](https://betfair-datascientists.github.io/modelling/howToModelTheAusOpen/) gives a good overview of ranking-based models, regression-based models and point-based models
- How we used [ELO](https://betfair-datascientists.github.io/modelling/soccerEloTutorialR/) and [machine learning](https://betfair-datascientists.github.io/modelling/EPLmlPython/) as different approaches to modelling the World Cup

---
## Get your hands dirty

The best way to learn is by doing. Make sure you have a solid foundation knowledge to work from, then get excited, get your hands dirty and see what you can create! Here are a final few thoughts to help you decide where to from here:

- Make sure you’ve got your [Betfair Basics](https://www.betfair.com.au/hub/education/betfair-basics/the-betfair-exchange/) knowledge solid including [back betting](https://www.betfair.com.au/hub/education/betfair-basics/back-betting/), [lay betting](https://www.betfair.com.au/hub/education/betfair-basics/lay-betting/) and [reading exchange markets](https://www.betfair.com.au/hub/education/betfair-basics/read-an-exchange-market/)
- Learn about the importance of ratings and [prices](https://www.betfair.com.au/hub/education/racing-strategy/value-and-odds/) and get inspired by the [models](https://www.betfair.com.au/hub/models/) created by our Data Scientists
- Consider how you could use our [API](/../api/apiappkey) in building and automating your model
- Read about how successful some of our customers have been in their [modelling journeys](https://www.youtube.com/watch?v=zBU5JA4hl1c&list=PLvw8KRdyfOY19ys_5lpSpcbjpy_PBoZEZ)