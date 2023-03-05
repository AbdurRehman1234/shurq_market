import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.io as pio
import plotly.graph_objects as go

plt.style.use("seaborn")


def date_extractor(string):
    return str(string).split(",")[0].strip()


def month_year_extractor(date):
    return "{}/{}".format(str(date).split("/")[1], str(date).split("/")[-1])


def visualizer(dataframe, outputs_csv_dir, outputs_chart_dir):
    
    # extracting dates from the dataframe. The Time column is converted into the date col
    dataframe["Date_Time"] = dataframe["Time"].apply(date_extractor)
    dataframe["Date_Time"] = pd.to_datetime(dataframe["Date_Time"]).dt.strftime("%d/%m/%Y")
    dataframe["Date_Time"] = dataframe["Date_Time"].apply(month_year_extractor)
    
    print("---------------------------------------")
    print("Cleaning up the data, grouping by date and calculating information to visualize it...")
    print("---------------------------------------")

    dataframe_to_visualize = dataframe[["Date_Time", "Brand", "Sales Rank"]]
    grouped_df = dataframe_to_visualize.groupby(
        ["Date_Time", "Brand"], as_index=False)["Sales Rank"].mean()

    # extracting the market share by dividing every value of Sales Rank in a specific date by sum of all values
    # in that date and then taking reciprocal of that value
    grouped_df["Market_Share"] = grouped_df.groupby(
        "Date_Time")["Sales Rank"].transform(lambda x: (1 / (x / x.sum())))

    # for determining the percentage contribution doing the same except the receprocal part
    grouped_df["Market_Share_Percentage"] = grouped_df.groupby(
        "Date_Time")["Market_Share"].transform(lambda y: y / y.sum() * 100)

    # chagning the format of string date to datetime format and then sorting values in ascending order
    grouped_df["Date_Time"] = pd.to_datetime(grouped_df["Date_Time"])
    grouped_df.sort_values(by="Date_Time", ascending=True, inplace=True)
    grouped_df["Date_Time"] = grouped_df["Date_Time"].dt.strftime("%d/%m/%Y")
    
    # replace null values with 0
    grouped_df.fillna(0, inplace=True)

    cleaned_df = grouped_df[grouped_df["Market_Share_Percentage"] != 0]
    
    
    # saving the final csv file
    file_path = os.path.join(outputs_csv_dir, "resultant.csv")
    i = 1

    # renaming if the file is already exist
    while os.path.exists(file_path):
        file_path = os.path.join(outputs_csv_dir, "resultant_{}.csv".format(i))
        i += 1
    cleaned_df.to_csv(file_path, index=False)

    data = []
    for brand in cleaned_df["Brand"].unique():
        df = cleaned_df[cleaned_df["Brand"] == brand]
        
        # accessing the latest percentage for the brand to show with the labels
        latest_dates = pd.to_datetime(df["Date_Time"]).idxmax()
        
        modified_df_latest_dates = df.loc[latest_dates]
        
        column_name = "Market_Share_Percentage"
        

        # brand market share percentage is the combination of the percentage and the brand name makes the descriptive Labels
        brand_msp = f"{brand} ({str(round(modified_df_latest_dates[column_name], 2))}%)"

        data.append(
            go.Scatter(x=df["Date_Time"],
                       y=df["Market_Share_Percentage"],
                       name=brand_msp,
                       stackgroup='one'))

    layout = go.Layout(title='Market Share by BSR',
                       xaxis=dict(title='Date Time'),
                       yaxis=dict(title='Market Share Percentage'),
                       showlegend=True)
    
    fig = go.Figure(data=data, layout=layout)
    return fig
    # fig.show() #by ab
    # # saving the resultant image file
    # file_path = os.path.join(outputs_chart_dir, "resultant_chart.png")
    # i = 1
    #
    # # renaming if the file is already exist
    # while os.path.exists(file_path):
    #     file_path = os.path.join(outputs_chart_dir,
    #                              "resultant_chart_{}.png".format(i))
    #     i += 1
    #
    # fig.write_image(file_path)
