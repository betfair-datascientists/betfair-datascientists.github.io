# Golden Rules of Automation
| Some rules of thumb to help on your modelling & automation journey
 ---
So, you're interested in modelling and automation? That's great to hear, but between having that interest and actually developing a fully working automated betting strategy is often a lot of effort, mistakes and iterative learning. Here we share some of our internal 'golden rules' of automation 
- those lessons we've learnt ourselves or heard from others in the community 
- in the hope that this might help to expedite your automation journey and help you avoid making some of the same mistakes we have along the way! As a high level philosophy, we suggest taking a risk averse approach to modelling and automation, avoiding bias in your model and back testing, being conservative in your staking and setting your automation up with fail safes and, if in doubt, to simply not bet. Hopefully this philosophy will stand you in good stead on your automation journey!

---
## Modelling
Obviously before you can have an automation you need a model, of one form or another. Although this isn't the main focus of this article we do have several tutorials written by our in-house data scientists and modellers from the wider community that might be valuable:

- [Greyhound modelling using form data in Python](https://betfair-datascientists.github.io/modelling/greyhoundModellingPython/)
- [Modelling the Aus Open](https://betfair-datascientists.github.io/modelling/howToModelTheAusOpen/)
- [EPL ML walk through in Python](https://betfair-datascientists.github.io/modelling/EPLmlPython/)
- [AFL modelling in Python](https://betfair-datascientists.github.io/modelling/AFLmodellingPython/)

---
## Back testing
Once you've developed the first cut of your model you're going to want to make sure you test your strategy using historical data before you start betting with real money. Although you can never know exactly how a strategy is going to play out in the real world, particularly in terms of the 'butterfly effect' that your activity might have on the wider market, there is a lot you can do to test your theories before putting them into practice.

- We've put together several tutorials on how to use the JSON historical Betfair pricing data which is available back to 2016, including one specifically focused on back testing: [Back testing ratings in Python](https://betfair-datascientists.github.io/historicData/backtestingRatingsTutorial/)
- To prevent data leakage it's important to make sure to only use data that is available before the outcome of the event you are modelling begins e.g. the BSP is only known after a Horse Racing market goes in play, therefore make sure you don't include the BSP of the race you're modelling, as you won't have it before the jump when you might be looking to bet. It sounds simple but it's one that catches the best of us more often than we'd like to admit!
- When back testing make sure to partition your dataset:
    - It is common in data science to split your dataset into training, testing and validation sets, this way you can create and train your strategy on the training dataset and test and validate your strategy on separate datasets.
    - Strategies can often become overfitted to the dataset they were trained on, leading to strategies that may not be generalizable or don't hold in real life. Making sure you separate your testing and validation datasets will help mitigate this risk by back testing your strategy on an out of sample data set.
- If you don't have the data you need to back test your strategy reach out to <Data@betfair.com.au> and we'll see what we can do!

---
## Staking
Hand in hand with your back testing you need to develop a staking strategy. Different people can bet the same model and get very different results, and those differences come down to the betting and staking strategies you use to implement your model. Here are some things to consider when developing your staking and bank management strategy: 

- The staking approach that you use should mirror the staking approach used when back testing your strategy
- If you want to change your staking you should consider re-running your back testing before going live with any changes.
- Is there a maximum stake size you want to have on any given bet/selection? 
    - If you are using a pure Kelly staking approach you may end up putting a large portion of your account onto a single selection - capped Kelly is a potential option here. 
- Minimum bet sizes
    - If you are using Kelly or some variable staking measure it's important to note that Betfair has minimum bet sizes (AUD5 unless you have minimum bets removed from your app key for testing, when it's then 1p), and lay bets have [minimum bet liabilities](https://forum.developer.betfair.com/forum/developer-program/announcements/32066-retrospective-api-release-to-prevent-minimum-bet-abuse-19th-june). 
- If your strategy is creating ratings, it might be worth checking the difference between your rated price and the market price; if your ratings are significantly different to the market odds close to the jump then a general rule of thumb is that your model is probably missing something as the market is (generally speaking), the best source of truth. This is particularly important to consider when your staking strategies increase your stake size based on the size of your edge e.g. Kelly. There are a couple of ways of handling this, one way of doing so is to set a maximum stake size, effectively capping the size of your bets, and another to stay out of the market if the difference is too significant. 
- What impact might your strategy have on the market? For example, if you're trying to place large stakes on longer prices you may crunch the price in or not get fully matched, either of which would not be in keeping with your back testing and lead to unexpected variance.

---
## Automation 

### Choose a tool that suits the job
Depending on the complexity of your strategy and your skillset. If you can achieve what you need using one of the [many tools that exist for automation on the Exchange](https://www.betfair.com.au/hub/betting-applications/), great! If not, and you have some coding skills, probably the next best option is to see whether there's a code library around in a language that you're familiar with. We've put together [a collection of some of the most popular libraries and repos](https://github.com/betfair-down-under/AwesomeBetfair) for interacting with the Exchange APIs that might help you decide where to start. 

### Code modularization
It's easy to dive straight into it when you're building a bot, but being intentional in your design can save you grief in the long term. Writing modular code will help create a more robust pipeline that makes it easier to diagnose errors when they occur and deploy fixes and is much easier to maintain. It's also worth commenting your code as you go (we know, do as we say, not as we do!), but it really makes it easier to come back to your code down the track and understand what your logic is doing. The same principle also applies to using existing tools.

### Logging
Your bot will need debugging, guaranteed, and having a decent logging functionality in place from the beginning will save you grief during the process. Consider implementing a function to log important information as you need to check it, such as the ratings/predictions generated by your model, bet placement attempts from your bot and other relevant fields. This will be really helpful for:

- Diagnosing where and how things are going wrong 
- often you can see there's an issue, but you don't know where or what the issue is.
- Optimizing your automation program in the future 
- Logging your model's predictions can also be useful to further evaluate your strategy once you go live so it's worth saving them for later use (more on this under the Monitoring section).

### Automatic Stop & Manual Override
The best and worst thing about automated bots is that they work autonomously, but that also means that at times they can do things you don't want them to do when you're not actively monitoring them. To this end it's worth considering implementing a function that stops your automation from placing bets if a certain situation arises, for example if the same bet is placed multiple times in a short amount of time. This can help to minimise the potential risks and damage of automation bugs. Similarly, creating a manual override function that you can use at any time in case of emergencies to instantly stop all bet placement and/or to cancel all unmatched bets may also be worth considering. Worst case this can be a kill switch, but you need to be prepared in advance for these situations, and they will happen, so, you want to make sure you can resolve them with as little negative impact as possible. 

---
## Going Live
### Start Small
If you have an edge that's worth having it's unlikely that it will disappear overnight, and you really should consider starting with small stakes when you're implementing a new model or strategy to ensure that reality matches theory before you stake up. There are a few reasons to start small before considering scaling up:

- This allows you to evaluate your strategies live without too much skin in the game. It's really easy to have a live bot that doesn't track against the back testing performance, often because there was a flaw in the logic used to back test or there was too much biasing in the model. 
- This also ensures your bet placement system is working correctly with minimal risk; there are too many stories of large multimillion dollar, financial trading companies who have fallen to trading errors which have wiped them out e.g., Knight Capital - you don't want to make the same mistake!
- Starting small also allows you to gain confidence that your program and strategies are behaving as expected before you start putting more substantial stakes through the system.

### Testing
When you first turn on your automation on it can be a good idea to keep an eye on your bot to make sure it's doing what you expect it to do:

- This will give you a better understanding of how your automation works in practice, and you can quickly pick up where things work differently to expected.
- This is especially important for strategies which place multiple bets and cancel bets allowing you to optimise code to trade more or less aggressively.
- You will also be able to catch if there are any errors in your logic or bet placement before it has a chance to cause you too much grief.

### Keep a Small Account Balance
At the end of the day, in the worst-case scenario you can't lose more than the balance that's in your betting account, so it can be worth considering limiting the available balance while you're testing a new strategy or bot just to be on the safe side. There are a few things to consider:

- Make sure to do a quick estimate of how much working capital is required to cover your expected liabilities - you equally don't want your bot to run out of available funds when you do want bets to go on.
- An alternative approach to this is to use the `customerStrategyRef` field in the API to cap the amount you can have on any given strategy. 
- Once you have tested your system and are happy with how it's working you can increase your bank size.

---
## Monitoring
Congratulations, you made it and you've got your model up and running all on its own, fantastic! So, what's next? Despite the temptation, neither model or automated strategies should really be left to their own devices long term without regular monitoring and sense checks, to make sure that your model is still solid and nothing has changed in your data or the wider market to undermine your potential edge. 

### Variance
Any long-term strategy is likely to see variance across time, and it is challenging to know when a period of poor performance is expected variance or whether it's a result of something changing in your data, model efficacy or the wider market. A couple of things to consider:
- Regularly compare your back tests against reality, i.e., for the last 30 days what did your simulation say your outcomes should be, and how does that compare with what really happened? If these are significantly different you may want to do some digging. 
- Consider what time period you want to review your automation, once it's established. Some people check daily, others weekly, and others again look at it monthly. Whatever your preference, this helps to give you a framework to work against and regular accountability. 

--- 
## Resources
If you want to learn more, here are some resources that might be valuable:

- [Meet ups and workshop recordings](https://www.betfair.com.au/hub/analytical-meet-ups/)
- [API resources](https://betfair-datascientists.github.io/api/apiResources/)
- [Historic pricing data](https://betfair-datascientists.github.io/historicData/dataSources/)
- [Modelling tutorials](https://betfair-datascientists.github.io/modelling/howToModel/)

---
## Over to you!
Building and automating a model on the Exchange can be great fun, and hopefully some of this resonates with you or you can apply within your automation journey. If we can help along the way please [reach out!](mailto:automation@betfair.com.au)

---
## Disclaimer
Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.
