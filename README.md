# Automation with Python - ACT Scores

This is a web application that downloads ACT score files using Encoura web API and uploads them to Technolutions FTP server.
> This script was created by refencing [Encoura API Documentation](https://helpcenter.encoura.org/hc/en-us/articles/360037582012-API-Documentation-for-Automating-Downloads-of-ACT-Score-Reports- "Encoura API Documentation")  and [nrccua sample script](https://github.com/nrccua/file_export_sample "Sample Script").

### Steps 
* Install `Python 3.7.2`
* Run `Pip install -r requirements.txt`
* Store your credentials in config.py file using following variables:
  `USERNAME, PASSWORD, ORGANIZATION_UID, API_KEY, FTP_USERNAME, TP_PASSWORD`
* Run `python main.py` in terminal or using a scheduler.  
