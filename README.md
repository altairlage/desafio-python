# desafio-python

My solution for python challenge.


# Coding challenge

The main goal of the coding challenge is to exercise Python development skills while also improving the knowledge of the broad variety of technologies from Docker to AWS as well as features from Python itself.

## Pre-requirements

- Python 3.7
- Pip
- An IDE (PyCharm, VSCode, VIM, etc)

## Challenge

Given you are working on a telecom company you were tasked to create a CLI tool that generates a charging report based on a billing report.

The CLI tool will check out a DynamoDB Table to check for the customer's information as well as to fetch information from pricing of the calls. The billing report will be provided by an argument to the tool `--billing-file the_billing_file.json`.

### Customer DynamoDB Table

| customerId (str UUID)           | name (str) | address (str)                     | offerId (str UUID)               | number (str)        |
| ------------------------------- | ---------- | --------------------------------- | -------------------------------- | ------------------- |
| 789o987-9878987-8768987-9876789 | Potato     | Mashed st, 45. 9191 - Ipuiuna. MG | 789o987-9878987-8768987-98712312 | +55 35 9 9988 90 30 |


### Pricing DynamoDB Table

| offerId (str UUID)               | offerName (str) | price (number) |
| -------------------------------- | --------------- | -------------- |
| 789o987-9878987-8768987-98712312 | Potato          | 0.014          |


### Billing report file

The report file schema is:

```json
{
  "definitions": {},
  "$schema": "",
  "$id": "http://my.tele.com/billing/UUID",
  "type": "array",
  "title": "billing report",
  "default": [],
  "readOnly": true,
  "items": {
    "$id": "#/items",
    "type": "object",
    "title": "billing item",
    "default": {},
    "required": [
      "callerNumber",
      "targetNumber",
      "startedTime",
      "duration"
    ],
    "properties": {
      "callerNumber": {
        "$id": "#/items/properties/callerNumber",
        "type": "string",
        "title": "The caller number",
        "default": "",
        "examples": [
          "+55 35 9 8850 2030"
        ]
      },
      "targetNumber": {
        "$id": "#/items/properties/targetNumber",
        "type": "string",
        "title": "The target number",
        "default": "",
        "examples": [
          "+55 35 9 8851 4020"
        ]
      },
      "startedTime": {
        "$id": "#/items/properties/startedTime",
        "type": "integer",
        "title": "The started time",
        "description": "Epoch time (milliseconds) of when the call started",
        "default": 0,
        "examples": [
          1566839534000
        ]
      },
      "duration": {
        "$id": "#/items/properties/duration",
        "type": "integer",
        "title": "The duration",
        "description": "The duration (in milliseconds) of the given call",
        "default": 0,
        "examples": [
          1304000
        ]
      }
    }
  }
}
```

An example of the report is:

```json
[
  {
    "callerNumber": "+55 35 9 8850 2030",
    "targetNumber": "+55 35 9 8851 4020",
    "startedTime": 1566839534000,
    "duration": 1304000
  },
  {
    "callerNumber": "+55 35 9 8850 2030",
    "targetNumber": "+55 35 9 8853 4026",
    "startedTime": 1566839584000,
    "duration": 4000
  }
]
```

### The report to be generated

Print a report like the one below

```
Total price for the billing period is: R$ 1,241

Please find the details below:

╔═══════════════╤══════════════╤═══════════════════════════╤══════════════════════════╗
║ Caller        │ Target       │ Started time              │ Duration     | Price     ║
╠═══════════════╪══════════════╪═══════════════════════════╪══════════════════════════╣
║ Mashed potato │ Fried potato │ 2016-12-01 00:00:00-06:00 │ 00:00:46:59  |  R$ 1,15  ║
║ Mashed potato │ Unknown      │ 2016-12-01 00:00:00-06:30 │ 00:00:01:59  |  R$ 0,09  ║
║ Mashed potato │ Baked potato │ 2016-12-01 00:00:00-05:43 │ 00:00:00:30  |  R$ 0,001 ║
╚═══════════════╧══════════════╧═══════════════════════════╧══════════════╧═══════════╝
```
