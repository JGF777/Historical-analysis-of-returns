"""
THIS SCRIPT ANALYSES PAST HISTORICAL DATA TO PERFORM DIFFERENT
CALCULATIONS ON RETURNS OF SEVERAL ASSETS.

DATA SOURCE : OBTAINED FROM DAMODARAN (NYU FINANCE DEPARTMENT)

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker 
import pandas as pd 
import random
import seaborn as sns

# STYLE GUIDE
sns.set_style('darkgrid')  # darkgrid, white grid, dark, white and ticks
plt.style.use('fivethirtyeight')
plt.rc('axes', titlesize=18)  # fontsize of the axes title
plt.rc('axes', labelsize=14)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=13)  # fontsize of the tick labels
plt.rc('ytick', labelsize=13)  # fontsize of the tick labels
plt.rc('legend', fontsize=13)  # legend fontsize
plt.rc('font', size=13)  # controls default text sizes

#  LIST WITH THE MOST RELEVANT RETURNS
ASSETS = ["SPY", "3M TBILL", "10Y BONDS", "BAA CORP BONDS", 
		 "REAL ESTATE", "INFLATION RATE", "60/40 returns", "ONLY STOCKS"]

#MAIN FUNCTION.

def main():

	def get_data():
		df = pd.read_excel("historical_modified.xlsx")
		df.set_index("Year", inplace=True)
		return df[2:]

	df = get_data()

	def get_macro_data(df):
		"""
		CONSIDER TO IMPLEMENT A FUNCTION THAT PULLS DATA
		FROM RELEVANT ONLINCE SOURCES ABOUT MACRO FACTORS
		"""
		pass


	def portfolio_construction(df):
		df["60/40 returns"] = 0.6 * df["SPY"] + 0.4 * df["10Y BONDS"]
		df["ONLY STOCKS"] = df["SPY"]

		return df

	portfolio_construction(df)
 

	def asset_acumulated(df):
			
		for asset in ASSETS:
			df[f"{asset} ACUMULADO"] = (df[f"{asset}"] + 1).cumprod()

		return df

	df_acumulado = asset_acumulated(df)
	
	

	def get_graph_assets(df_acumulado):
		"""
		FUNCTION THAT PLOTS THE MAIN GRAPH FOR THE ANALYSIS.
		INCLUDES ACCUMULATED GROWTH AND MACROECONOMIC INDICATORS
		"""
		fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

		fig.suptitle("REAL RETURN OF DIFFERENT ASSETS", fontsize=18)

		ASSETS_GRAPH = ["SPY", "3M TBILL", "10Y BONDS", "BAA CORP BONDS", "REAL ESTATE"]
		COLORS = ['b', 'g', 'r', 'c', 'm']
		graph_elements = zip(ASSETS_GRAPH, COLORS)

		for asset in graph_elements:
			ax1.plot(df_acumulado[f"{asset[0]} ACUMULADO"], label=f"{asset[0]}", 
	                	color=f"{asset[1]}", linewidth=2.0)


		#EDIT GRAPHS AND DESIGN OF THE DIFFERENT SUBPLOTS
		ax1.legend()
		ax1.set_ylabel("Growth of 1$")
		#ax1.set_yscale("log")
		for axis in [ax1.yaxis]:
			axis.set_major_formatter(mticker.ScalarFormatter())
			axis.set_major_formatter(mticker.FormatStrFormatter('%.d $'))

		#PLOT INFLATION RATE
		ax2.plot(df_acumulado["INFLATION RATE ACUMULADO"], label="INFLATION RATE", color="k", linewidth=2.0)
		for axis in [ax2.yaxis]:
			axis.set_major_formatter(mticker.FormatStrFormatter('%.d $'))
		ax2.set_ylabel("Accumulated inflation (CPI)")

		#MAIN KEYWORDS = "M2 SUPPLY" or "INTEREST RATE" or "INFLATION RATE ACUMULADO"
		def macro_indicator(ax, indicator, color, label):
			ax.plot(df_acumulado[f"{indicator}"], label=f"{indicator}", color=f"{color}", linewidth=2.0)
			ax.set_ylabel(f"{label}")

		macro_indicator(ax3, "M2 SUPPLY", "c", "M2 (BILLIONS USD)")

		plt.show()

	get_graph_assets(df_acumulado)



	def get_graph_portfolio_performance(df_acumulado):
	   """
	   GRAPH TO COMPARE GROWTH OVER TIME BETWEEN PORTFOLIOS
	   """
	   plt.figure(figsize=(16,8))
	   plt.title("Growth of portfolio")   
	   plt.legend()
	   plt.plot(df["60/40 returns ACUMULADO"], label="60/40 Portfolio", color="r", linewidth=2.0)
	   plt.plot(df["ONLY STOCKS ACUMULADO"], label="Only stocks portfolio", color="b", linewidth=2.0)
	   plt.ylabel("Growth of 1$")
	   plt.show()

	get_graph_portfolio_performance(df_acumulado)



	def plot_bars(df_acumulado):
		"""
		FUNCTION THAT PLOTS THE AVERAGE ANNUAL RETURN
		OF DIFFERENT ASSETS PER DECADE
		"""
		df3 = df.groupby((df.index//10)*10).mean().applymap(lambda x: x * 100)

		#FILTER BY RELEVANT COLUMNS
		df_final = df3[["SPY", "3M TBILL", "10Y BONDS", 
						"BAA CORP BONDS", "REAL ESTATE", "INFLATION RATE", "GOLD"]]

		df_final.plot.bar(grid=True)
		plt.title("AVERAGE REAL RETURNS PER DECADE")
		plt.ylabel("%", fontsize=18)
		plt.show()

	plot_bars(df_acumulado)


if __name__ == "__main__":
	analysis = main()
