import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_trend(df, column, title, save_path=None):
    """
    Plot the trend of a specific column over time (quarters).

    Parameters:
    - df: DataFrame with a 'Date' column and the target column.
    - column: str, the column name to plot.
    - title: str, the plot title.
    - save_path: str or None, if provided saves plot to this path instead of showing.
    """
    if column not in df.columns:
        print(f"Skipping plot: Column '{column}' not found.")
        return
    
    if df.empty or df[column].isnull().all():
        print(f"Skipping plot: No valid data in column '{column}'.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df[column], marker="o", linestyle='-')
    plt.title(title)
    plt.xlabel("Quarter")
    plt.ylabel(column)
    plt.grid(True)

    # Format date axis for quarters nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
