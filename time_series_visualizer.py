import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col="date")

# Subset data: Remove outliers for "value"
low, high = df["value"].quantile([0.025, 0.975])
mask_pcount = df["value"].between(low, high, inclusive="both")

# Clean data
df = df[mask_pcount]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20, 8))
    df.plot(kind="line",
            color="red",
            xlabel="Date",
            ylabel="Page Views",
            title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
            legend=False,
            ax=ax,  # Place in figure axis
    )

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = pd.pivot_table(df,
                            values="value",
                            index=df.index.year,
                            columns=df.index.month,
                            aggfunc=np.mean
                          )
    # Draw bar plot
    ax = df_bar.plot(kind="bar");
    # Get a Matplotlib figure from the axes object for formatting purposes
    fig = ax.get_figure()
    # Change the plot dimensions (width, height)
    fig.set_size_inches(20, 8)
    # Change the axes labels
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    # Change the plot legends to months
    handles, labels = ax.get_legend_handles_labels()
    labels = [datetime.date(1900, int(monthinteger), 1).strftime('%B') for monthinteger in labels] # strftime(%B)	gets the full month name by converting datetime to string
    ax.legend(labels = labels).set_title("Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20, 12))
    year_wise = sns.boxplot(data=df_box, x="year", y="value", orient='v', ax=ax[0])
    year_wise.set_xlabel("Year")
    year_wise.set_ylabel("Page Views")
    year_wise.set_title("Year-wise Box Plot (Trend)")
    year_wise.set_ylim(0, 200000)
    year_wise.set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])
    month_wise = sns.boxplot(data=df_box, x="month", y="value", orient='v', ax=ax[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov', 'Dec'])
    month_wise.set_xlabel("Month")
    month_wise.set_ylabel("Page Views")
    month_wise.set_title("Month-wise Box Plot (Seasonality)")
    month_wise.set_ylim(0, 200000)
    month_wise.set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig