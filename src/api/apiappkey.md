# How to access the Betfair API

Betfair has it’s own [Exchange API](http://developer.betfair.com). You can use it to programmatically retrieve live markets, automate successful trading strategies or create your own customised trading interface. Professional punters use it for these functions and many more.

This guide helps Australian and New Zealand customers with obtaining their Betfair API Key. If you’re outside of these two regions please go to the [UK's Developer Program website](http://developer.betfair.com).

There are four steps involved in getting access to our API

- Obtain an SSOID token
- Register your application
- Obtain your app key
- Activate your app key

!!! info "API access"
    Customers are able to access our API to embed it into their programs and automate their strategies
    Please [reach out](mailto:api@betfair.com.au) if you're an Australian or New Zealand based customer and are keen for support.
    
---
### Find your SSOID token
The simplest way to setup your browser with the SSOID is to follow [this link](https://identitysso.betfair.com/view/login?product=home.betfair.int&url=https%3A%2F%2Fwww.betfair.com.au%2F) and log in - this will allow for the SSOID to be automatically populated in the next step. 

After logging in, you’ll be sent to the main Betfair website. *Note: it may not show that you’re logged in on the site. You can ignore that. Proceed to step two.*

---
### Register your application
Navigate to the [API-NG accounts visualiser](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/).

If you’ve followed step 1 correctly, your SSOID token should be automatically populated in the visualiser.

![Creating an API app key](./img/apiVisualiser.png)

Next click on `createDeveloperAppKeys` in the left hand navigation.

Type in an application name (this is your app key name, so make sure this is unique), then click ‘Execute’ down the bottom of the page.
 
If you receive an error message saying that your app key couldn’t be created, it’s most likely because you already have one. Use the `getDeveloperAppKeys` method in the left hand menu to check whether there’s already an app key associated with your account.

---
### Find your app key
After your key is created, you should see in the right hand panel your application:

![Creating an API app key](./img/apiAppKey.png)

You’ll notice that two application keys have been created;

- Version – 1.0-Delay: is a delayed app key for development purposes

- Version – 1.0: is the live pricing app key; on yours it should have a status ‘No’ in Active.

Grab the application key listed for the live price one - for the example above, that is ‘MkcBqyZrD53V6A..’

---
### Activate your app key
This process will generate two app keys: 

- A developer key which is designed for development purposes. This has a variable delay of between 1 and 180 seconds, doesn’t show matched volume and doesn’t need to be activated prior to use.

- A live app key is intended for transacting on the Exchange and should only be used when you’re ready to start placing bets or can no longer test your strategy effectively using the developer key. 

***Please note that if the live key is used to pull data from the Exchange without corresponding bets being placed a delay may be automatically applied to the live key.***

If you’re ready to start testing your strategy or placing bets, please contact api@betfair.com.au and we will be happy to assist with activating the live key and implementing your strategy. 