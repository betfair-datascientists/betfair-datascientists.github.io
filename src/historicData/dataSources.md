# Historical Data Sources

We know that your automated strategies and models are only as good as your data. We work hard to make sure you have access to the data you need to allow you to achieve what you're setting out to in your automation and modelling projects. There’s a huge variety of historic pricing data available, and hopefully this page shows you how to access what you're looking for.

For more information on how to use this data to make your own predictive model, take a look at our [modelling section](/modelling/howToModel). 

---
## [Historical Stream API data](https://historicdata.betfair.com/#/mydata)

Betfair UK give access to all the historical Stream API data since 2016. It is excellent to use in building models and back testing strategies, however isn't necessarily in an easily accessible format for everyone. 

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

- [How to download and access the data files](/historicData/usingHistoricDataSite)
- [Historic Data FAQs & sample data](https://historicdata.betfair.com/#/help)
- [Historic Data Specifications](https://historicdata.betfair.com/Betfair-Historical-Data-Feed-Specification.pdf)
- [API for downloading historic data files](https://historicdata.betfair.com/#/apidocs) (quicker than manually downloading)
- [Sample code for using the historic data download API](https://github.com/betfair/historicdata)

### Tutorials for working with this data

- [JSON to CSV in Python](/historicData/jsonToCsvTutorial)
- [Backtesting ratings using historic data in Python](/historicData/backtestingRatingsTutorial)
- [Automated betting angles: no modelling required](/historicData/automatedBettingAnglesTutorial)

---
## [Historical racing data](https://promo.betfair.com/betfairsp/prices)

This is an excellent resource if you are interested in racing and like to see market level data in a CSV format.

### What you need to know about this data source:

- CSV format
- Free to download
- All Australian and overseas races, dating back to the beginning of the Exchange
- Available as a single file per day, per country, win or place market
- Market snapshot by runner, including
    - Max and min matched prices and volume, pre-play and in-play
    - Weighted average price, pre-play and in-play
    - BSP
    - Winner

---
If none of these options suit your needs please contact us at data@betfair.com.au to discuss other potential options.