# Features dashboard / Binance futures auto-closing

For now, this is just a small utility that allows me to set a [TradingView](https://www.tradingview.com/) alert's webhook on a candle close and have this handle the closing of that position.

For now it only supports Binance USD-M Futures, and I only tested with [one way mode](https://www.binance.com/en/support/faq/360041513552).

## Use it at your own risk!

I did this for myself, as I rather sleep and not wake up with an alert to stop out of a position. As with every automatic approach, it has the potentital to fail and your position might not be closed, so **test it and use it at your own risk.**

Things that can potentially fail:

- I made a mistake in the code and it failed.
- You made a mistake in the payload message and/or the URL and it failed.
- There was a network issue between TrandingView and Heroku and it failed.
- The IP you got on your dyno (heroku instance) might have been previously gone over their [limits](https://www.binance.com/en/support/faq/360004492232). It's **VERY, VERY** unlikely, but noting it.
- Make sure to remove the alert, because the webhook will continue to close the symbol if you open it again.

## Setting it up

### #1 Binance API Keys

 You will need to [create a set of API keys on binance](https://www.binance.com/en/support/faq/360002502072). It will ask you to give the API Key permissions, please check `Enable reading` and `Enable Futures`. This will get you an `API KEY` and an `API SECRET`. Note those down in some secure way, treat them like passwords. You will use this in the next step.

### #2 Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/hanoii/binance-futures)

You will have to sign up to Heroku first. It gives you 550 hours for free or 1000 if you add a creditcard. Because this app will be used seldomly (when you access it or when the alert accesses it) you'll hardly ever need more than that.

This will ask for a username and password, enter some credentials of your choice. This will be used both to access the dashboard as well as for the webhook.

It will also ask for your Binance API Keys, enter the ones you got on step #1.

### #3 Test it out

That's pretty much it. If all worked, you should be able to open the web app you just deployed from Heroku, enter your credentials and you should see your open poisitions as well as the URL you have to use on TradingView and payload (message format) examples.

## Usage

Besides accesing the dashboard where there's not a lot, you can use it to gather the webhook URL as well as look at some examples. This might evolve over time.

<p align="center">
  <img width="400" src="https://raw.githubusercontent.com/hanoii/binance-futures/main/docs/images/tvexample.png">
</p>

## Binance Tesnet

This can be tested against [binance futures' testnet](https://testnet.binancefuture.com/). You need to register a new account there and a [differet set of API keys](https://dev.binance.vision/t/binance-testnet-environments/99).

You also will have to add a new [configuration variable on Heroku](https://devcenter.heroku.com/articles/config-vars) `BINANCE_TESTNET` with value `true` for it to work

## Update

I might be pushing changes from time to time, you can destroy your Heroku instance and recreate it again, that will pull in any new changes.
