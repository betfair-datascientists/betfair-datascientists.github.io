A common struggle shared by many a user of Betfair is how to build a database of results from the Betfair Exchange.

There are many different sources of data available, each with its own limitations and lag times.
These sources include:

 - [Daily CSV Files](https://promo.betfair.com/betfairsp/prices) 
 - [Monthly CSV Blocks](https://betfair-datascientists.github.io/data/dataListing/)
 - [Hub Results Graphical UI](https://www.betfair.com.au/hub/racing/horse-racing/racing-results/)
 - [Historical Stream Files](https://historicdata.betfair.com/#/mydata)

However, as is often said, the most accurate and valuable source of data that you can use for modelling is data that you collect yourself.
Collecting your own data ensures that data leakage is excluded from your database, as is always a danger when using someone else's data.

The challenge with collecting your own data is, of course, patience. And the fewer events that take place for your chosen sport or racing code, the longer you need to wait to collect a meaningful data set.
Greyhound Racing, sometimes with 150+ Australian races per day, won't take long, maybe 3 months, to collect a meaningful dataset, whereas Thoroughbred racing might be 12 months, and sport data even longer.
And for events like the Olympics, well you'll need to have the patience of a saint.

There goes a saying of unknown origin that states **"The best time to plant a tree is twenty years ago. The second best time is now."**
Well let's look at how we plant the seed of building a database of recordings from the Betfair Streaming and Polling APIs

