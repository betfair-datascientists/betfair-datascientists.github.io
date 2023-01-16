---
hide:
  - navigation
#   - toc
---

<!-- hide text header for img header -->
<style> .md-typeset h1 { display: none; } </style>
    
# _

<div markdown style='text-align: center;'>
![The Automation Hub](/img/automationHubHero.gif)
</div>

Betfair is one of the only betting platforms in the world that demands winning clients. Unlike bookies, we don’t ban you when you succeed. We need you, and we want you to be able to keep improving your strategies so you win more. 

We're here to help you in your automation journey, and this site is dedicated to sharing the tools and resources you need to succeed in this journey. 

---
## Accessing Betfair's APIs
Betfair has a set of customer-facing transactional APIs to allow you to integrate your program into the Exchange. Many of our most successful clients bet exclusively through this by placing automated bets using custom software.

There are lots of resources available to support you in accessing the API effectively:

- [Golden rules of automation](/api/GoldenRulesofAutomation)
- [Creating & activating your app key](/api/apiappkey)
- [Developer Program knowledge base](https://betfairdevelopersupport.zendesk.com/hc/en-us)
- [Dev Docs](http://developer.betfair.com)
- [Developer Forum](https://forum.developer.betfair.com/) where you can share your experiences and find out what's worked for other clients
- [Exchange Sports API visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/) for testing market-related queries
- [Exchange Account API visualiser](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/) for testing account-related queries
- Our Datascientists' repos for using [R](/api/apiRtutorial) and [Python](/api/apiPythontutorial) to access the API
- There's an ANZ [Betfair Down Under](https://github.com/betfair-down-under) community GitHub repo where you can find sample code, libraries, tutorials and other resources for automating and modelling on the Exchange and an [`AwesomeBetfair`](https://github.com/betfair-down-under/AwesomeBetfair) list of external repos we think are worth visiting
- [The UK’s Github repo](https://github.com/betfair) including libraries for other languages

!!! info "API access"
    Customers are able to access our API to embed it into their programs and automate their strategies
    Please [reach out](mailto:api@betfair.com.au) if you're an Australian or New Zealand based customer and are keen for support.

---
## Historic pricing data

We know that automated strategies are only as good as your data. There’s a huge variety of historic pricing data available for almost any race or sport – you can take a look at our explanation of the [different data sources](/historicData/dataSources) if you’re not quite sure where to start. We’ve also shared some tips on learning to create [predictive models using this data](/modelling/howToModel), which link in with the models shared in the [modelling section](/modelling).

### Tutorials

- [JSON to CSV in Python](/historicData/jsonToCsvTutorial)
- [Backtesting ratings using historic data in Python](/historicData/backtestingRatingsTutorial)
- [Automated betting angles: no modelling required](/historicData/automatedBettingAnglesTutorial)
- [Do *#theyknow*? Analysing Betfair market formation and market movements](/historicData/analysingAndPredictingMarketMovements)
- [Wisdom of the crowd? Analysing & understanding BSP](/historicData/analysingAndPredictingBSP)

### Other resources
- [Betfair data sources](/historicData/dataSources)
- [Data processor](https://www.betfairhistoricdata.co.uk/) to generate CSVs from the historic JSON files 
- [Historic Data FAQs & sample data](https://historicdata.betfair.com/#/help)
- [Historic Data Specifications](https://historicdata.betfair.com/Betfair-Historical-Data-Feed-Specification.pdf)
- [The Stream API dev docs](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API) are the best source of information for interpreting the data from the Historic Data site

!!! info "Historic Betfair data"
    There is a lot of historical price data available for all markets offered on the Exchange, ranging from aggregate, market-level csv files to complete JSON recreations of API Stream data. If you are interested in the data available please [reach out](mailto:data@betfair.com.au).

---
## Data modelling 

We have a series of modelling tutorials created by community members ranging from racing to sports, including [greyhound modelling using form data in Python](/modelling/greyhoundModellingPython), an [AFL tutorial in Python](/modelling/AFLmodellingPython) and [Brownlow modelling tutorial](/modelling/brownlowModelTutorial)

!!! info "Predictive modelling"
    Many of our most successful customers use predictive models as the basis for their betting strategies 

---
## Automation tools

Whilst the following tools are not custom built for your approach, they do allow you to automate your betting strategies. You just set up specific betting conditions and let the third party application do the work for you. [Bet Angel](https://betangel.com) and [Gruss Betting Assistant](http://gruss-software.co.uk) are probably the most popular automation tools used by Australian customers. 

We’re putting together a collection of articles on how to use some of these third party tools to automate basic strategies, to give you a starting point that you can then work from.

- [Bet Angel Professional](/autoTools/betAngel/betAngel)
- [Gruss Betting Assistant](/autoTools/Gruss/Gruss)
- [Cymatic Trader](/autoTools/CymaticTrader/CymaticTrader)
- [Geeks Toy](/autoTools/GeeksToyinstallationandsetup)

--- 
## Inspiration & information 

There are a lot of people who use data, models and automation to make a living out of professional betting. Here are some of their stories, and some extra tools to help you develop your own strategy. 

- [Analytical Meet Up recordings](https://www.youtube.com/playlist?list=PLvw8KRdyfOY19ys_5lpSpcbjpy_PBoZEZ)
- [Our Twitter community](https://twitter.com/Betfair_Aus) is really active 



!!! info "Betfair Quants Discord Group"
    `betfair quants` is really active Betfair-owned Discord server for people interested in modelling and automation on the Exchange. Please [reach out](mailto:automation@betfair.com.au) if you'd like an invitation. 
    
---
## Need extra help?

If you’re looking for bespoke advice or have extra questions, please contact us at [automation@betfair.com.au](mailto:automation@betfair.com.au). Our automation team are here to support you in automating your betting strategies.