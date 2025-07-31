"""
Find S&P 500 good tickers.
"""


from datetime import datetime, timedelta
import yfinance as yf
# import pandas_datareader as pdr
import pandas as pd
import time
import asyncio

# Set up parameters.
# n_tickers = 10
n_batch = 50
days_lookback = 365
tiingo_api_key = '075bcce532428f40548b0dc38e63b33458de3aad'

def get_sp500_data():
    sp_500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    return pd.read_html(sp_500_url)

def get_sp_500_names():
    return get_sp500_data()[0]

sp_500_names = get_sp_500_names()
ticker_to_name = dict(zip(sp_500_names['Symbol'], sp_500_names["Security"]))

extra_ticker_to_name = {
    "ARM" : "Arm Holdings",
    "TSM" : "Taiwan SemiConductor Manufactoring Company",    
    }

ticker_to_name.update(extra_ticker_to_name)
YEARS_LOOKBACK = 1
TICKERS = list(ticker_to_name.keys())
START_DATE = str((datetime.now() - timedelta(days = YEARS_LOOKBACK * 365)).date())
END_DATE = str(datetime.now().date())


def fetch_stock_data(stock: str) -> pd.DataFrame:
    try:
        print(f"Downloading: {stock}")
        data = yf.download(stock, start=START_DATE, end = END_DATE, 
                           auto_adjust=None)
        # print(data)
        data[("DailyReturn", stock)] = data.Close - data.Close.shift(1)
        data[("Energy", stock)] = data.DailyReturn * data.Volume
        return data.fillna(0)
    except Exception as e:
        print(f"Error: {stock}: {e}")
    
async def async_fetch_stock_data(stock: str) -> pd.DataFrame:
    try:
        print(f"Downloading: {stock}")
        data = yf.download(stock, start=START_DATE, end = END_DATE)
        data["ticker"] = stock
        data[("DailyReturn", stock)] = data.Close - data.Close.shift(1)
        data[("Energy", stock)] = data.DailyReturn * data.Volume
        return data
    except Exception as e:
        print(f"Error: {stock}: {e}")
    
async def get_sp500_stocks_data():
    #Compute the daily returns.
    tasks = [async_fetch_stock_data(stock) for stock in TICKERS]
    df_list = await asyncio.gather(*tasks)
    return df_list

def get_n_days_energy(all_data: pd.DataFrame, n_day: int) -> pd.DataFrame:
    """Gets the energy in the last n days.
    
    Args:
        n_day: number of days to look back.
        
    Returns:
        A dataframe of the returns and energies of all stocks.
    """
    if n_day == 0:
        return pd.DataFrame()
    
    sub_data = all_data.loc[all_data.index[-n_day:]]
    col = f'{n_day}D_Energy'
    energy_df = pd.DataFrame(sub_data.Energy.sum(), columns = [col]).reset_index()
    energy_df["Stock"] = energy_df["Ticker"].replace(ticker_to_name)
    energy_df.sort_values(by = [col], ascending = [False], inplace = True)
    return energy_df

def get_n_days_return(all_data: pd.DataFrame, n_day):
    if n_day == 0:
        return pd.DataFrame()
    
    last_day_data =  all_data.loc[all_data.index[-1], ["Close"]]
    last_n_day_data =  all_data.loc[all_data.index[-n_day], ["Close"]]
    
    return_n_day = (last_day_data / last_n_day_data - 1).apply(lambda x: round(x, 2))
    col_name = f"{n_day}D_Return"
    return_df = pd.DataFrame(return_n_day, columns = [col_name]).reset_index()
    return_df["Stock"] = return_df["Ticker"].replace(ticker_to_name)
    return return_df.sort_values(col_name, ascending=False)

from  multiprocessing import Pool, freeze_support

if __name__ == '__main__':
    freeze_support()

    start_time = time.time()
    
    with Pool(10) as pool:
        df_list = pool.map(fetch_stock_data, TICKERS)
    
    # df_list = []
    # for stock in TICKERS:
    #     df_list.append(fetch_stock_data(stock))
    
    all_data = pd.concat(df_list, axis = 1)
    
    runtime_min = (time.time() - start_time)/60
    print(f"\n Runtime Mins: {runtime_min}")
    
    print("\nTop 30 10D Energy: \n", get_n_days_energy(all_data, 10)[:30])
    print("\nBottom 30 10D Energy: \n", get_n_days_energy(all_data, 10)[-30:])
    
    
