import os
from time import sleep
import pandas as pd
import shutil
from timeit import default_timer as timer
from datetime import datetime, timedelta
from scripts.set_driver import BrowserDefine
from scripts.helium10 import (
    csv_read,
    zip_change,
    csv_download,
    del_gen_csv,
    wait_4_csv,
    input_dir,
    download_dir,
    country_dict,
    input_visualizer,
    outputs_csv_dir,
    outputs_chart_dir,
)
from scripts.visualizer_scripts.data_visualizer import visualizer
from scripts.visualizer_scripts.concatinate_csv import csv_concate


# input_asins_path = os.path.join(input_dir, "input_marketshare.csv")
gen_csv_file = os.path.join(download_dir, "chart.csv")

start_time = timer()


def main(asins, Marketplace, Zipcode, Brands):

    current_date = datetime.now().strftime("%Y/%m/%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    print("---------------------------------------")
    print("Scrape Start Date Time = {} {}".format( current_date, current_time))
    print("---------------------------------------")

    # h10 data scraper switch
    scraper_switch = True

    # visualizer Switch
    visualizer_switch = True

    # retry times
    retry_times = 5

    if scraper_switch:
        # Driver Open
        browser_obj = BrowserDefine()
        browser_obj.chrome_driver_download()
        browser_obj.chrome_open()
        driver = browser_obj.connexion_to_website()

        # df = pd.read_csv(input_asins_path)
        #by ab
        liste=[]
        for i in range(len(asins)):
            liste.append([asins[i], Marketplace[i], Zipcode[i], Brands[i]])
        df=pd.DataFrame(liste,columns=['ASIN','Marketplace','Zipcode','Brand'])
        
        print(df)
        #end by ab
        input_dicts = df.to_dict(orient="records")
        input_dicts = [
            {str(key).strip(): str(value).strip() for key, value in inp_dict.items()}
            for inp_dict in input_dicts
        ]

        for idx, input_dict in enumerate(input_dicts):
            asin = input_dict["ASIN"]
            country = input_dict["Marketplace"]
            zipcode = input_dict["Zipcode"]
            brand_name = input_dict["Brand"]

            bool_zip = False

            for retry in range(retry_times):
                try:

                    print("-----------------------------------")
                    print("On input {}/{}".format(idx + 1, len(input_dicts)))
                    [print("{}: {}".format(key, value)) for key, value in input_dict.items()]
                    print("")

                    base_url = country_dict.get(country)
                    product_url = base_url + '/dp/' + asin

                    # Change ZIP
                    bool_zip = zip_change(driver, base_url, zipcode)
                    sleep(1)

                    if bool_zip:
                        # Visit Product URL Page
                        driver.get(product_url)

                        # CSV Download
                        csv_download(driver)

                    # Delete all cookies
                    print('Delete all cookies')
                    driver.delete_all_cookies()

                    # Wait Until File downloaded
                    wait_4_csv(gen_csv_file)

                    input_name = f"{brand_name}_{asin}_{country}.csv"
                    input_visualizer_dir = os.path.join(input_visualizer, input_name)
                    shutil.move(gen_csv_file, input_visualizer_dir)

                    print(f"{input_name} Move Sucessfully")
                    end_time = timer()
                    print("Time Elapsed: {}".format(timedelta(seconds=int(end_time - start_time))))
                    print("---------------------------------------")

                    break
                except:
                    end_time = timer()
                    print("---------------------------------------")
                    print("Some problems occurred...")
                    print("Retying {}/{}".format(retry+1, retry_times))
                    print("Time Elapsed: {}".format(timedelta(seconds=int(end_time - start_time))))
                    print("---------------------------------------")

        end_time = timer()
        print("------------------------------------------------------")
        print("The bot has finished scraping for all the inputs successfully...")
        print("------------------------------------------------------")
        print(
            "Total Time Elapsed: {}".format(timedelta(seconds=int(end_time - start_time)))
        )
        print("------------------------------------------------------")

        try:
            driver.delete_all_cookies()
        except:
            pass
        driver.close()

    if visualizer_switch:
        print("---------------------------------------")
        print("Starting the H10 data visualizer...")
        print("---------------------------------------")
        concatinated_df = csv_concate(input_visualizer)
        print("---------------------------------------")
        print("Moving the DataFrame to the Data Visualizer...")
        print("---------------------------------------")
        fig=visualizer(concatinated_df, outputs_csv_dir, outputs_chart_dir)
        print("---------------------------------------")
        print("Saving the resultant chart and csv to the outputs section...")
        print("---------------------------------------")

    current_date = datetime.now().strftime("%Y/%m/%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    print("---------------------------------------")
    print("Scrape End Date Time = {} {}".format( current_date, current_time))
    print("---------------------------------------")
    return fig