# Historical Data Sources

We know that your automated strategies and models are only as good as your data. We work hard to make sure you have access to the data you need to allow you to achieve what you're setting out to in your automation and modelling projects. There’s a huge variety of historic pricing data available, and hopefully this page shows you how to access what you're looking for.

For more information on how to use this data to make your own predictive model, take a look at our [modelling section](/modelling/howToModel). 

---
## [Historical Stream API data](https://historicdata.betfair.com/#/mydata)

Betfair UK give access to all the historical Stream API data since 2016. It is excellent to use in building models and back testing strategies, however isn't necessarily in an easily accessible format for everyone.
Australian and New Zealand customers should email us at data@betfair.com.au before purchasing any data from this site.

### What you need to know about this data source:

- JSON format, downloads as TAR files (zipped)
- Australian and overseas racing, plus soccer, tennis, cricket, golf and ‘other sport’ data
- All Exchange markets included since the Stream API was introduced in 2016
- Time-stamped odds and volume data
- Able to filter by Event ID, market type and other parameters 
- 3 tiers of access:
    - Basic free tier – 1 minute intervals for odds, no volume (free)
    - Advanced tier – 1 second intervals for odds, volume included (cost associated)
    - Pro tier – 50 millisecond intervals for odds, volume included (cost associated)
- Includes a Historic Data API endpoint for download management 

### Supporting resources to help you access this data:

- [Historic Data FAQs & sample data](https://historicdata.betfair.com/#/help)
- [Historic Data Specifications](https://historicdata.betfair.com/Betfair-Historical-Data-Feed-Specification.pdf)
- [Sample code for using the historic data download API](https://github.com/betfair/historicdata)

### Tutorials for working with this data

- [JSON to CSV in Python](/tutorials/jsonToCsvTutorial)
- [JSON to CSV | Revisited](/tutorials/jsonToCsvRevisited) - where we make it 30 times faster
- [Backtesting ratings using historic data in Python](/tutorials/backtestingRatingsTutorial)
- [Automated betting angles: no modelling required](/tutorials/automatedBettingAnglesTutorial)
- [TAR Files 101](/tutorials/processingTarFiles101)

---
## [Historical racing data](https://promo.betfair.com/betfairsp/prices)

This is an excellent resource if you are interested in racing and like to see market level data in a CSV format.

### What you need to know about this data source:

- CSV format
- Free to download, no login required
- All Australian and overseas races, dating back to the beginning of the Exchange
- Available as a single file per day, per country, win or place market
- Market snapshot by runner, including
    - Max and min matched prices and volume, pre-play and in-play
    - Weighted average price, pre-play and in-play
    - BSP
    - Winner

---

## [Sports and Racing CSV Files - Australia and New Zealand](/data/dataListing)

### What you need to know about this data source:

- CSV format
- Free to download, no login required
- All Australian and New Zealand races, dating back to January 2023 in monthly blocks, separated by racing code
- Market snapshot by runner, including
    - Max and min matched prices and volume, pre-play and in-play
    - Weighted average price, pre-play and in-play
    - BSP & Result (Win & Place)
    - Best Available Prices & Market Overrounds at Scheduled Race Start Time
- Select Australian Sports leagues, dating back to 2020
    - AFL & AFLW
    - A-League & A-League Women's
    - BBL & WBBL
    - NRL
    - NBL
- Condensed historical ratings files with results for Betfair Hub Tipsters and Prediction Models
    - [Iggy Greyhound Predictions Model](https://www.betfair.com.au/hub/racing/greyhound-tips/greyhound-predictions-model/)
    - [Kash Thoroughbred Predictions Model](https://www.betfair.com.au/hub/racing/horse-racing/predictions-model/)
    - [Top 5 Thoroughbred Predictions Model](https://www.betfair.com.au/hub/racing/horse-racing/top-5-predictions/)
    - [Globetrotter Harness Predictions Model](https://www.betfair.com.au/hub/racing/harness/harness-racing-predictions/)
 ---

If none of these options suit your needs please contact us at data@betfair.com.au to discuss other potential options.