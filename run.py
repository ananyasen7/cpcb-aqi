import json
import base64
import numpy as np
import requests
import argparse
from enum import Enum


class Granularity(Enum):
    HOUR = 1
    DAY = 2
    MONTH = 3


GRANULARITY = {
    Granularity.HOUR: "1 Hours",
    Granularity.DAY: "24 Hours",
    Granularity.MONTH: "1 Month",
}

# Please update the granularity as required. The default is set to daily.
GRANULARITY_REQUESTED = Granularity.DAY
# Please update the parameters as required. Note that the parameter names are case sensitive
# and there might be cities which do not have all the parameters. Please refers to paremeters.json
# for the list of parameters for each city.
PARAMETERS = {
    "parameter_215": "PM10",
    "parameter_193": "PM2.5",
    "parameter_226": "NO",
    "parameter_225": "NOx",
    "parameter_194": "NO2",
    "parameter_311": "NH3",
    "parameter_312": "SO2",
    "parameter_203": "CO",
    "parameter_222": "Ozone",
}


result = {}


def base64_encode(string):
    message = string
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")

    return base64_message


def api_call(headers, encoded_data, site):
    cookies = {"ccr_public": "<cookie_value>"}
    r = requests.post(
        "https://app.cpcbccr.com/caaqms/advanced_search",
        headers=headers,
        data=encoded_data,
        cookies=cookies,
        verify=False,
    )
    if r.status_code == 200:
        decoded_data = base64.b64decode(r.text)
        json_dict = json.loads(decoded_data)
        aqi_data = json_dict["tabularData"]["bodyContent"]
        for row in aqi_data:
            row_data = {}
            row_data["from date"] = row["from date"]
            row_data["to date"] = row["to date"]
            for key in PARAMETERS.values():
                row_data[key] = row[key]
            if site not in result:
                result[site] = []
            result[site].append(row_data)
    else:
        raise Exception(f"Error: {r.status_code}")


get_station_ids = lambda data, city: [
    station["id"]
    for station in next(filter(lambda x: x["cityName"] == city, data), {}).get(
        "stationsInCity", []
    )
]


def get_site_list_from_city(city):
    file_content = open("stations.json", "r")
    data = json.load(file_content)
    return get_station_ids(data, city)


def fetch_data(from_date, to_date, city):
    headers = {
        "Origin": "https://app.cpcbccr.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://app.cpcbccr.com/ccr/",
        "Connection": "keep-alive",
        "Host": "app.cpcbccr.com",
    }

    site_list = get_site_list_from_city(city)

    parameter = list(PARAMETERS.keys())
    parameterNames = list(PARAMETERS.values())

    for site in site_list:
        data = {
            "criteria": GRANULARITY[GRANULARITY_REQUESTED],
            "reportFormat": "Tabular",
            "fromDate": from_date,
            "toDate": to_date,
            "city": "Kolkata",
            "station": site,
            "parameter": parameter,
            "parameterNames": parameterNames,
        }
        json_str = json.dumps(data)
        encoded_data = base64_encode(json_str)
        api_call(headers, encoded_data, site)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Air Quality Fetcher")
    parser.add_argument(
        "--from_date",
        type=str,
        help='Starting date in the format "dd-mm-yyyy THH:MM:00Z"',
    )
    parser.add_argument(
        "--to_date", type=str, help='Ending date in the format "dd-mm-yyyy THH:MM:00Z"'
    )
    parser.add_argument(
        "--city", type=str, help="City name for which data is to be fetched"
    )
    parser.add_argument("--output_json", type=str, help="Output json file name")
    parser.add_argument(
        "--aggregate",
        type=bool,
        help="Aggregates the city level data across all sensors and writes to a separate file",
    )

    args = parser.parse_args()
    from_date = args.from_date
    to_date = args.to_date
    city = args.city
    output_file_json = args.output_json
    fetch_data(from_date, to_date, city)

    with open(f"{city}_{output_file_json}", "w") as fp:
        json.dump(result, fp, indent=2)

    if args.aggregate:
        aggregate_result = {}
        for site in result:
            for key in PARAMETERS.values():
                if key not in aggregate_result:
                    aggregate_result[key] = []
                for row in result[site]:
                    if row[key] is not None:
                        aggregate_result[key].append(float(row[key]))
        for key in aggregate_result:
            aggregate_result[key] = np.mean(aggregate_result[key])
        with open(f"{city}_aggregate_{output_file_json}", "w") as fp:
            json.dump(aggregate_result, fp, indent=2)
