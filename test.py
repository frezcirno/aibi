# %%
import yfinance as yf
import math
msft = yf.Ticker("JSML")
# %%
df=msft.history(period="1y",interval="3mo")
# %%
df.shape
# %%
df.dropna(inplace=True)
# %%
tf=msft.financials
# %%


# show institutional holders
# %%
print(msft.institutional_holders)
msft.get_cashflow(proxy="http://7c00h.xyz:7890")
# show balance sheet
msft.balance_sheet
msft.quarterly_balance_sheet

# show cashflow
msft.cashflow
msft.quarterly_cashflow

# show earnings
msft.earnings
msft.quarterly_earnings

# show sustainability
msft.sustainability

# show analysts recommendations
msft.recommendations

# show next event (earnings, etc)
msft.calendar


# %%
msft = yf.Ticker("MSFT")
# %%
df=msft.cashflow
# %%
df=msft.quarterly_financials
# %%
# df1=msft.major_holders
df2=msft.history(period="1y",interval="3mo")
# %%
import yfinance as yf
import math
def ScoreforO(ticker:str):
    msft = yf.Ticker(ticker)
    df=msft.quarterly_financials
    items=["Income Before Tax",""]
    weight=[0.55,0.15,0.05,0.05,0.1,0.1]
    fin=[]
    i=df.loc["Income Before Tax"]
    fin.append((i.sum()-i.min()*4)/(i.max()-i.min()))
    #i=df.loc["Total Revenue"]/df.loc["Total Revenue"]
    return fin[0]

# %%
def ScoreforI(tickers:list,edu:int):
    score=0
    for i in tickers:
        score+=ScoreforO(i) 
    edu=edu/1.6
    score=(math.exp(score)/(math.exp(score)+1)-0.5)*16
    lscore=(math.exp(edu)/(math.exp(edu)+1)-0.5)*2
    return score+lscore
# %%
score=10
score=(math.exp(score)/(math.exp(score)+1)-0.5)*16 
# %%
l=6
l=l/1.6
print((math.exp(l)/(math.exp(l)+1)-0.5)*2)
# %%
df.to_csv("1.csv")
# %%
import numpy as np
import math
# %%


# %%
rand_data = np.random.normal(1, 3, 1)
# %%
n=np.random.random(1)*3
n = (math.exp(n)/(math.exp(n)+1)-0.5)*20
print(n)
# %%
score=15
score=score/6
score = (math.exp(score)/(math.exp(score)+1)-0.5)*8
print(score)
# %%
