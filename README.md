# API Scripts Repository

## Purpose and scope
Welcome to the Scripts repository for the Viedoc organization. This repository is dedicated to hosting various scripts that interact with Viedoc EDC APIs to automate tasks and facilitate data management.

## Overview of the repository
- [Import helper](./import-helper/README.md): 
  - Python script to assist with local setup when using the [Viedoc Data Import Application](https://help.viedoc.net/c/331b7a/cf6a45/en/) (requires a Viedoc WCF API client).
- [Viedoc site & user import tool](./add-sites-and-users/README.md): 
  - Python script that allows for sites and users to be imported from an Excel file, using a [Viedoc Web API client](https://help.viedoc.net/c/331b7a/6fd31a/en/). 
  - To be used during initial study setup when many sites and users need to be added to the study. Has Excel template generating feature.
- [Viedoc export](./viedoc-export/README.md): Python and R scripts to trigger and downloads exports from Viedoc EDC using a Viedoc Web API client.

## Changelog
- 2024 May: initial repo creation, upload of export script.
- 2025 Feb: Addition of site/user import tool & import helper scripts from internal archive

