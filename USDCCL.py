#https://ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/


import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style
#from datetime import date
import matplotlib.patheffects as path_effects

%matplotlib inline


#DEFINE LAS FECHAS
start_date = dt.datetime(2019, 8, 1) #YYYY--MM--DD
end_date = dt.datetime(2020, 9, 24)

# Dólar CCL

CCL_0 = web.DataReader("GGAL", "yahoo", start_date, end_date) # NASDAQ
CCL0_close = CCL_0.drop(CCL_0.columns[0:5], axis=1)

CCL_1 = web.DataReader("GGAL.BA", "yahoo", start_date, end_date) # BCBA
CCL1_close = CCL_1.drop(CCL_1.columns[0:5], axis=1)


mCCL = CCL_1["Adj Close"] * 10 / CCL_0["Adj Close"]

# Dólar mayorista

Money = web.DataReader("USDARS=X", "yahoo", start_date, end_date)

Money_close = Money.drop(Money.columns[0:5], axis=1)
# Fechas conversiones

PAIS_start = "2019-12-23"
PAIS_end = "2020-09-14"

AFIP_start = "2020-09-15"
AFIP_end = end_date

# Fechas para formato

lastDayDate = (Money_close.index.array[-1]).day
lastMonthDate = (Money_close.index.array[-1]).month

# Cambia los valores del Solidario y el AFIP. Se suma 4 pesos de la comisión BNA.
dollarBNA = 4

Money_close.loc[PAIS_start:PAIS_end, "Adj Close"] = Money_close.loc[PAIS_start:PAIS_end, "Adj Close"] + dollarBNA
Money_close.loc[PAIS_start:PAIS_end, "Adj Close"] = Money_close.loc[PAIS_start:PAIS_end, "Adj Close"]*1.3

k1 = Money_close.loc[AFIP_start:AFIP_end, "Adj Close"] + dollarBNA

Money_close.loc[AFIP_start:AFIP_end, "Adj Close"] = k1*1.65




# Se calcula la brecha

breach = ((mCCL/Money_close["Adj Close"]))*100

# Ploteo #

style.use("dark_background")

plt.figure(figsize=(10,8))

h0 = plt.subplot(2,1,1)
h0.set_title(f"Cotización del dólar Solidario BNA (prom.) y brecha cambiaria minorista al {lastDayDate}/{lastMonthDate}/20", fontsize=12)
h0 = sns.lineplot(x = Money_close.index, y = Money_close["Adj Close"], color = "lemonchiffon", label="Dólar BNA (Incluye recargos impositivos)")
h0 = sns.lineplot(x = mCCL.index, y = mCCL, color = "red", label="Dólar CCL (GGAL)")
h0.legend()
h0.set(xlabel = "Fecha", ylabel = "Cotización")
plt.grid(linestyle = "dashed", alpha=0.3)

# Ploteo brecha #
h1 = plt.subplot(2,1,2)
h1 = sns.lineplot(x = breach.index, y = breach, color = "blue", label="Brecha base 100")
h1.legend()
h1.set(xlabel = "Fecha", ylabel = "Base 100 = Dólar BNA Solidario (promedio)")
plt.grid(linestyle = "dashed", alpha=0.3)



# Anotaciones #
lastPrice = round(Money_close["Adj Close"].iloc[-1], 2)
lastPrice_CCL = round(mCCL[-1], 2)
lastBreach_index = breach.index.get_loc(breach.last_valid_index())
lastBreach = round((breach[lastBreach_index] - 100), 2)# https://bit.ly/32E2gV3

# Último precio

# Money #
plt.text(Money_close.index.array[-1] + pd.Timedelta(25, unit="D"),
                        Money_close["Adj Close"].iloc[-1] + 63, f"${lastPrice}", color="lemonchiffon", fontdict=None)

# CCL #
plt.text(mCCL.index.array[-1] + pd.Timedelta(25, unit="D"),
                        lastPrice_CCL + 54, f"${lastPrice_CCL}", color="red", fontdict=None)

# Última brecha
plt.annotate(f"{lastBreach}%", 
              xy = (breach.index[-1], breach[lastBreach_index]),
              xytext = (breach.index[-1] + pd.Timedelta(25, unit="D"),
                        breach[lastBreach_index] - 1),
              color = "white")
# path_effects = [path_effects.Stroke(linewidth=2, foreground='white'),
# path_effects.Normal()]
#https://bit.ly/35Hop73
#https://bit.ly/2Ha2Th4


# SAVE #
plt.savefig(f"filename_breach_{lastDayDate}.{lastMonthDate}.png", dpi=300)