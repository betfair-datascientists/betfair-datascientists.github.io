# How to access the Betfair API

Betfair has it’s own [Exchange API](http://developer.betfair.com). You can use it to programmatically retrieve live markets, automate successful trading strategies or create your own customised trading interface. Professional punters use it for these functions and many more.

This guide helps Australian and New Zealand customers with obtaining their Betfair API Key. If you’re outside of these two regions please go to the [UK's Developer Program website](http://developer.betfair.com).

There are four steps involved in getting access to our API

- Obtain an SSOID token
- Register your application
- Obtain your app key
- Activate your app key

---
### Find your SSOID token
The simplest way to setup your browser with the SSOID is to follow [this link](https://identitysso.betfair.com/view/login?product=home.betfair.int&url=https%3A%2F%2Fwww.betfair.com.au%2F) and log in - this will allow for the SSOID to be automatically populated in the next step. 

After loggin in, you’ll be sent to the main Betfair website. Note: it may not show that you’re logged in on the site. You can ignore that. Proceed to step two.

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

Grab the application key listed for the live price one - for the example above, that is ‘MkcBqyZrD53V6A’

---
### Activate your app key
Please [contact us](mailto:bdp@betfair.com.au) when you’re ready to activate your app key - we have a dedicated resource to make it as easy for you as possible.