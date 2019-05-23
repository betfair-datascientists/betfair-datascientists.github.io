![The Automation Hub](/img/automationHubHero.gif)

Betfair is one of the only betting platforms in the world that demands winning clients. Unlike bookies, we don’t ban you when you succeed. We need you, and we want you to be able to keep improving your strategies so you win more. 

We're here to help you in your automation journey, and this site is dedicated to sharing the tools and resources you need to succeed in this journey. 

---
### Accessing our API
As you may already know, Betfair has its own API to allow you to integrate your program into the Exchange. Many of our most successful clients bet exclusively through this by placing automated bets using custom software.

There are lots of resources available to support you in accessing the API effectively:

- [Creating & activating your app key](/api/apiappkey)
- [Developer Program knowledge base](https://betfairdevelopersupport.zendesk.com/hc/en-us)
- [Dev Docs](http://developer.betfair.com)
- [Developer Forum](https://forum.developer.betfair.com/) where you can share your experiences and find out what's worked for other clients
- [Exchange Sports API visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/) for testing market-related queries
- [Exchange Account API visualiser](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/) for testing account-related queries
- Our Datascientists' repos for using [R](/api/apiRtutorial) and [Python](/api/apiPythontutorial) to access the API
- [The UK’s Github repo](https://github.com/betfair/API-NG-Excel-Toolkit) including libraries for other languages

!!! note "API access"
    Customers are able to access our API to embed it into their programs and automate their strategies
    If you're a programmer there are lots of resources around to help

---
### Historic Data

We know that automated strategies are only as good as your data. There’s a huge variety of historic pricing data available for almost any race or sport – you can take a look at our explanation of the [different data sources](/historicData/dataSources) if you’re not quite sure where to start. We’ve also shared some tips on learning to create [predictive models using this data](/modelling/howToModel), which link in with the models shared in the [modelling section](/modelling/EPLmodelPart1).

- [Betfair data sources](/historicData/dataSources)
- [Accessing the official Historic Data site](/historicData/usingHistoricDataSite)
- [Historic Data FAQs & sample data](https://historicdata.betfair.com/#/help)
- [Historic Data Specifications](https://historicdata.betfair.com/Betfair-Historical-Data-Feed-Specification.pdf)
- [API for downloading historic data files](https://historicdata.betfair.com/#/apidocs) (quicker than manually downloading)
- [Sample code for using the historic data download API](https://github.com/betfair/historicdata)
- [The Stream API dev docs](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API) are the best source of information for interpreting the data from the Historic Data site
- [Historic BSP csv files](https://promo.betfair.com/betfairsp/prices)

!!! note "Historic Betfair data"
    There is a lot of historical price data available for all makrets offered on the Exchange, ranging from aggregate, market-level csv files to complete JSON recreations of API Stream data

---
### Using third party tools for automation 

Whilst the following tools are not custom built for your approach, they do allow you to automate your betting strategies. You just set up specific betting conditions and let the third party application do the work for you. [Bet Angel](https://betangel.com) and [Gruss Betting Assistant](http://gruss-software.co.uk) are the most popular third party tools. 

We’re putting together a collection of articles on how to use some of these third party tools to automate basic strategies, to give you a starting point that you can then work from.

- [Bet Angel Overview](/thirdPartyTools/betAngel)
    - [Ratings automation](/thirdPartyTools/betAngelRatingsAutomation)
    - [Market favourite automation](/thirdPartyTools/betAngelMarketFavouriteAutomation) 
    - [Tipping automation](/thirdPartyTools/betAngelTippingAutomation)
    - [Automating multiple simultaneous markets](/thirdPartyTools/betAngelSimultaneousMarkets)
- [Gruss](http://gruss-software.co.uk)
    - [Ratings automation](/thirdPartyTools/grussRatingsAutomation)
    - [Automating multiple simultaneous markets](/thirdPartyTools/grusslSimultaneousMarkets)
- [Cymatic Trader](http://www.cymatic.co.uk/)
    - [Ratings automation](/thirdPartyTools/cymaticTraderRatingsAutomation)

---
### Data modelling 

- [An intro to building a predictive model](/modelling/howToModel)
- [Open source predictive models](/modelling/EPLmodelPart1) built by our in-house Data Scientists
    - [Modelling the Aus Open](/modelling/howToModelTheAusOpen)
    - [EPL modelling series](/modelling/EPLmodelPart1)
    - [AFL modelling series](/modelling/AFLmodelPart1)
    - [Brownlow modelling tutorial](/modelling/brownlowModelTutorial)

!!! note "Predictive modelling"
    Many of our most successful customers use predictive models as the basis for their betting strategies 

--- 
### Inspiration & information 

- [The Banker: A Quant's AFL Betting Strategy](https://www.betfair.com.au/hub/better-betting/customer-insights/the-banker-a-quants-afl-betting-strategy/)
- [The Mathematician](https://www.betfair.com.au/hub/better-betting/customer-insights/mathematician/)
- ['Back and Lay'](https://www.reddit.com/r/BackAndLay/) is a subreddit dedicated to discussing trading techniques
- [Our Twitter community](https://twitter.com/Betfair_Aus) is really active 
- [Staking Plans and Strategies](https://www.betfair.com.au/hub/better-betting/betting-principles/basic-principles/staking-plans-and-strategies/)
- [Staking and Money Management](https://www.betfair.com.au/hub/better-betting/betsmart-education/wagering-and-fundamentals/staking-and-money-management/)

!!! note "Some extra info"
    There are a lot of people who use data, models and automation to make a living out of professional betting. Here are some of their stories, and some extra tools to help you develop your own strategy. 

---
### Need extra help?

If you’re looking for bespoke advice or have extra questions, please contact us at bdp@betfair.com.au. We have a dedicated in-house resource that is here to automate your betting strategies.