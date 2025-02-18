# Import helper

This application helps with the setup of data imports via the Data Import Application.

- Create your data mappings in Viedoc Designer - Global Design Settings.
- Publish your Global Design Settings and download the mapping files.
- Create one main folder for your imports and place all your mapping files in it.
- Create a WCF API client in Viedoc Admin. Copy the GUID.
- Run this application (requires [python installation](https://www.python.org/downloads/)).
  - Open a terminal in the directory containing importHelper.py.
  - run the application using `python importHelper.py`
  - input the information as requested
- Download the Data Import Application from Viedoc Designer.
- Place your CSV data files in the correct subfolders.
- Run the Data Import Application.
- (Optional) Set up Task Scheduler: https://help.viedoc.net/l/5b5c16/en/'''
