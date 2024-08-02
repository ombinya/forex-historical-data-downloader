tradeitems = [
    'frxAUDJPY', 'frxAUDUSD', 'frxEURAUD', 'frxEURCAD', 'frxEURCHF', 'frxEURGBP', 'frxEURJPY',
    'frxEURUSD', 'frxGBPAUD', 'frxGBPJPY', 'frxGBPUSD', 'frxUSDCAD', 'frxUSDCHF', 'frxUSDJPY',
    'frxAUDCAD', 'frxAUDCHF', 'frxAUDNZD', 'frxEURNZD', 'frxGBPCAD', 'frxGBPCHF', 'frxGBPNOK',
    'frxGBPNZD', 'frxNZDJPY', 'frxNZDUSD', 'frxUSDMXN', 'frxUSDNOK', 'frxUSDPLN', 'frxUSDSEK',
    'OTC_AS51', 'OTC_HSI', 'OTC_N225', 'OTC_SX5E', 'OTC_FCHI', 'OTC_GDAXI', 'OTC_AEX',
    'OTC_SSMI', 'OTC_FTSE', 'OTC_SPC', 'OTC_NDX', 'OTC_DJI', 'frxXAUUSD', 'frxXPDUSD',
    'frxXPTUSD', 'frxXAGUSD', '1HZ10V', 'R_10', '1HZ25V', 'R_25', '1HZ50V', 'R_50', '1HZ75V',
    'R_75', '1HZ100V', 'R_100', '1HZ150V', '1HZ250V', 'RDBEAR', 'RDBULL', 'WLDAUD', 'WLDEUR',
    'WLDGBP', 'WLDUSD', 'WLDXAU', 'stpRNG', 'BOOM300N', 'BOOM500', 'BOOM1000', 'CRASH300N',
    'CRASH500', 'CRASH1000', 'JD10', 'JD25', 'JD50', 'JD75', 'JD100', 'cryBTCUSD', 'cryETHUSD'
]

tradeitemsdisplay = [
    'AUD/JPY', 'AUD/USD', 'EUR/AUD', 'EUR/CAD', 'EUR/CHF', 'EUR/GBP', 'EUR/JPY', 'EUR/USD',
    'GBP/AUD', 'GBP/JPY', 'GBP/USD', 'USD/CAD', 'USD/CHF', 'USD/JPY', 'AUD/CAD', 'AUD/CHF',
    'AUD/NZD', 'EUR/NZD', 'GBP/CAD', 'GBP/CHF', 'GBP/NOK', 'GBP/NZD', 'NZD/JPY', 'NZD/USD',
    'USD/MXN', 'USD/NOK', 'USD/PLN', 'USD/SEK', 'Australia 200', 'Hong Kong 50', 'Japan 225',
    'Euro 50', 'France 40', 'Germany 40', 'Netherlands 25', 'Swiss 20', 'UK 100', 'US 500',
    'US Tech 100', 'Wall Street 30', 'Gold/USD', 'Palladium/USD', 'Platinum/USD', 'Silver/USD',
    'Volatility 10 (1s) Index', 'Volatility 10 Index', 'Volatility 25 (1s) Index',
    'Volatility 25 Index', 'Volatility 50 (1s) Index', 'Volatility 50 Index',
    'Volatility 75 (1s) Index', 'Volatility 75 Index', 'Volatility 100 (1s) Index',
    'Volatility 100 Index', 'Volatility 150 (1s) Index', 'Volatility 250 (1s) Index',
    'Bear Market Index', 'Bull Market Index', 'AUD Basket', 'EUR Basket', 'GBP Basket',
    'USD Basket', 'Gold Basket', 'Step Index', 'Boom 300 Index', 'Boom 500 Index',
    'Boom 1000 Index', 'Crash 300 Index', 'Crash 500 Index', 'Crash 1000 Index',
    'Jump 10 Index', 'Jump 25 Index', 'Jump 50 Index', 'Jump 75 Index', 'Jump 100 Index',
    'BTC/USD', 'ETH/USD'
]

assetsdict = dict(zip(tradeitemsdisplay, tradeitems))

if __name__ == "__main__":
    for asset in assetsdict.keys():
        print(asset)

