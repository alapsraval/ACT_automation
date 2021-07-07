# Automation with Python - ACT Scores

This is a web application that downloads ACT score files using Encoura web API and uploads them to Technolutions FTP server.
> This script was created by refencing [Encoura API Documentation](https://helpcenter.encoura.org/hc/en-us/articles/360037582012-API-Documentation-for-Automating-Downloads-of-ACT-Score-Reports- "Encoura API Documentation")  and [nrccua sample script](https://github.com/nrccua/file_export_sample "Sample Script").

## Installation
* Install `Python 3.7.2`
* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
`pip install -r requirements.txt`
* Store your credentials in config_sample.py file using following variables and save it as config.py: 
  `USERNAME, PASSWORD, ORGANIZATION_UID, API_KEY, FTP_USERNAME, TP_PASSWORD`
## Usage
* Run the following command in terminal/command prompt or using a scheduler. It will check for a latest ACT file on Encoura server and download it into configured SFTP folder (incoming/test_scores).

  `python main.py` 
