This project is used to analyze ethereum wallet performance.
# How to use it
1. Install the dependency `python -r requirement.txt`
2. Download csv from https://zerion.io
3. Run `python main.py pth_to_your_csv.csv`

# How to interpret the output?
**Notice that we calculate everything based on ETH.**

Sample output:
```
2019-12-04 00:00:00  To  2020-11-02 00:00:00
Total order numbers: 1766
'WETH'
'USDT'
'YFV'
'BRAIN\nBRAIN'
'UNI-V2'
'xETH'
'USDT'
'WETH'
'USDC'
'WETH'
'USDC'
'WETH'
'USDT'
'USDT'
'UNI-V2'
'WETH'
'USDT'
'WETH'
'USDT'
'USDT'
'USDT'
'WETH'
'USDT'
'YFI'
'USDT'
'USDT'
'YFV'
'SERGS'
'SUSHI'
'USDT'
'UNI-V2'
'WBTC'
'WETH'
'WETH'
'USDT'
'YFI'
['1PC' 'AAT' 'ABOT' 'ALLCORE' 'ALPA' 'AMPL' 'ANTIPP' 'APECASINO' 'ASTRO'
 'AUSCM' 'AXIAv3' 'BANA' 'BECKY' 'BLUE' 'BPT' 'BRAIN' 'BURGER' 'CAPY'
 'CAT' 'CHARGED' 'CLIT' 'CLK' 'COCK' 'COM' 'CORE' 'CORIA' 'COUNTERCORE'
 'CYCL' 'Copy' 'DEUS' 'DOGEFI' 'DOKI' 'DORA' 'DORB' 'DR' 'DRC' 'EGEX'
 'ENCORE' 'EXP' 'FARM' 'FASE' 'FCT' 'FEEL' 'FOMO' 'FOOD' 'FSW' 'FUSDC'
 'FYRE' 'GDC' 'GRO' 'HATE' 'HEX' 'HEZ' 'HIPPO' 'HOLEv2' 'HOLY' 'IPM'
 'JIAOZI' 'KIMBAP' 'KORE' 'KP3R' 'LMS' 'LOCK' 'MEW' 'MOO' 'MTA' 'MUGA'
 'NIP' 'NOODLE' 'NVA' 'ORAI' 'OWL' 'PABA' 'PPBLZ' 'PRIA' 'PRINT' 'Poor'
 'QQQ' 'RARI' 'RCORE' 'REACTOR' 'RED' 'REVV' 'RPTC' 'SALE' 'SASHIMI'
 'SECO' 'SERGS' 'SHROOM' 'SNOW' 'SPORE' 'SPRINGROLL' 'SSL' 'STAMPS' 'SURF'
 'SUSHI' 'Seal' 'TABS' 'TACO' 'TGT' 'TOKEN' 'UFT' 'UNDB' 'UNI' 'UNT'
 'URUG' 'VAMP' 'VGA' 'VOX' 'Voyager' 'WBTC' 'WCB' 'WETH' 'WOA' 'XCORE'
 'XMM' 'YDEX' 'YELD' 'YFFI' 'YFI' 'YFR' 'YFV' 'YNK' 'YSEAL' 'YUGI'
 'ZOMBIESV2' 'ZZZ' 'brBTC' 'craft' 'dcore' 'locked brainweth' 'nSEAL'
 'nami' 'rPepe' 'renBTC' 'stacy' 'tens' 'xETH' 'yBAN' 'yCrv' 'yENOKI']
Total orders: 133
Total Analysis order:  100
No Cheat order:  97
Profit order: 70
Order Success ration: 0.7216494845360825
Net profit: 13.430388538888202
Mean profit rate: 0.6272346409045615
Mean profit rate: 0.7216494845360825
Median Duration: 13 minutes
```

The first part is basic information about the address. The transaction history time span and the total number of transaction.

```
2019-12-04 00:00:00  To  2020-11-02 00:00:00
Total order numbers: 1766
```

The second part of the output is the token not counted into performance due to technical limitations, which will be improved in the future.
```
'WETH'
'USDT'
'YFV'
'BRAIN\nBRAIN'
'UNI-V2'
'xETH'
'USDT'
'WETH'
'USDC'
'WETH'
'USDC'
'WETH'
'USDT'
'USDT'
'UNI-V2'
'WETH'
'USDT'
'WETH'
'USDT'
'USDT'
'USDT'
'WETH'
'USDT'
'YFI'
'USDT'
'USDT'
'YFV'
'SERGS'
'SUSHI'
'USDT'
'UNI-V2'
'WBTC'
'WETH'
'WETH'
'USDT'
'YFI'
```

The third part it the token we analyzed in this wallet.
```
['1PC' 'AAT' 'ABOT' 'ALLCORE' 'ALPA' 'AMPL' 'ANTIPP' 'APECASINO' 'ASTRO'
 'AUSCM' 'AXIAv3' 'BANA' 'BECKY' 'BLUE' 'BPT' 'BRAIN' 'BURGER' 'CAPY'
 'CAT' 'CHARGED' 'CLIT' 'CLK' 'COCK' 'COM' 'CORE' 'CORIA' 'COUNTERCORE'
 'CYCL' 'Copy' 'DEUS' 'DOGEFI' 'DOKI' 'DORA' 'DORB' 'DR' 'DRC' 'EGEX'
 'ENCORE' 'EXP' 'FARM' 'FASE' 'FCT' 'FEEL' 'FOMO' 'FOOD' 'FSW' 'FUSDC'
 'FYRE' 'GDC' 'GRO' 'HATE' 'HEX' 'HEZ' 'HIPPO' 'HOLEv2' 'HOLY' 'IPM'
 'JIAOZI' 'KIMBAP' 'KORE' 'KP3R' 'LMS' 'LOCK' 'MEW' 'MOO' 'MTA' 'MUGA'
 'NIP' 'NOODLE' 'NVA' 'ORAI' 'OWL' 'PABA' 'PPBLZ' 'PRIA' 'PRINT' 'Poor'
 'QQQ' 'RARI' 'RCORE' 'REACTOR' 'RED' 'REVV' 'RPTC' 'SALE' 'SASHIMI'
 'SECO' 'SERGS' 'SHROOM' 'SNOW' 'SPORE' 'SPRINGROLL' 'SSL' 'STAMPS' 'SURF'
 'SUSHI' 'Seal' 'TABS' 'TACO' 'TGT' 'TOKEN' 'UFT' 'UNDB' 'UNI' 'UNT'
 'URUG' 'VAMP' 'VGA' 'VOX' 'Voyager' 'WBTC' 'WCB' 'WETH' 'WOA' 'XCORE'
 'XMM' 'YDEX' 'YELD' 'YFFI' 'YFI' 'YFR' 'YFV' 'YNK' 'YSEAL' 'YUGI'
 'ZOMBIESV2' 'ZZZ' 'brBTC' 'craft' 'dcore' 'locked brainweth' 'nSEAL'
 'nami' 'rPepe' 'renBTC' 'stacy' 'tens' 'xETH' 'yBAN' 'yCrv' 'yENOKI']
```

We group transactions in to orders. A order contains the whole process of buying a token and selling it. We analyze the newest 75% orders and omit the order contains sends and receives which cannot calculate the token cost.
Profit orders are orders with positive returns.
Order success rate = profit orders / total orders
Net profit is the sum of all returns(including positive and negative).
Profit rate is the return / total investment.
Mean profit return is the mean of all positive profit rates.
Median duration is median of all order time spans(order close time-order open time).

```
Total orders: 133
Total Analysis order:  100
No Cheat order:  97
Profit order: 70
Order Success ration: 0.7216494845360825
Net profit: 13.430388538888202
Mean profit rate: 0.6272346409045615
Median Duration: 13 minutes
```

For the three graphs. The first one measures the order success rate given investment size. The x axis is the investment size(ETH). The y axis is the success rate. The point in the graph is the success rate of all orders smaller than the investment size. 

The second graph the histogram of  the investment size. The x axis is investment size and y axis is the number of orders.

The third graph is the wallet active hours. The x axis is the time and y axis is the number of orders.