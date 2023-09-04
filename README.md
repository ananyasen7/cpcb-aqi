# Air Quality Data Fetcher from CPCB

## Description

This Python script fetches air quality data for a given city within a specified date range. It utilizes the requests library to retrieve the data and saves it in JSON format. It fetches the
data from cpcbccr site.

## Features

- Fetch air quality data for a specific city and date range
- Ability to aggregate data (optional)
- Output the data in JSON format

## Prerequisites

- Python 3.x
- `requests` library

## Installation

First, clone the repository:

\`\`\`
git clone https://github.com/yourusername/air-quality-data-fetcher.git
\`\`\`

Navigate to the project directory:

\`\`\`
cd air-quality-data-fetcher
\`\`\`

Install the required packages as needed.

## Setting the Cookie

To run this script, you'll need to manually set the 'ccr_public' cookie obtained from the browser after completing the captcha.

1. Navigate to https://app.cpcbccr.com/AQI_India/ in your web browser.
2. Complete the captcha if required.
3. Inspect the browser and go to the 'Cookies' section in 'Applications' to find the 'ccr_public' cookie.
4. Copy the value of the 'ccr_public' cookie in the code (run.py).

In the Python script, find the line where the `cookies` dictionary is defined and set the 'ccr_public' cookie value:

\`\`\`python
cookies = {'ccr_public': 'your_cookie_value_here'}
\`\`\`

Replace `'your_cookie_value_here'` with the value you copied.
If the cookie expires, repeat the same process.

## Usage

Set granularity and required parameters in run.py before running the script.
You can refer to stations and parameters json files in the repo.
Run the script using the following command:

\`\`\`
python run.py --from_date "01-01-2023 T00:00:00Z" --to_date "04-01-2023 T12:00:00Z" --city "Jind" --output_json "out.json" --aggregate True
\`\`\`

### Command Line Arguments

- `--from_date`: The start date (required).
- `--to_date`: The end date (required).
- `--city`: The city for which to fetch air quality data (required).
- `--output_json`: The name of the output JSON file (required).
- `--aggregate`: Whether to aggregate data (optional, default is False).

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.