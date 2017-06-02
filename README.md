# About

> scm is a command line tool for operating Scala Content Manager's restful API.

## Installation
1. clone this repositry
2. `cd scm`
3. `pip install --editable .`

## Usage
Type `scm --help` for all the commands and options.

### Login
    scm login http://xxxx

scm use environ variable 'CM_URL' as the default Content Manager url. So if you don't want to specify the url in the command line, you can use command `export CM_URL=http://xxxx` (`set CM_URL=http://xxxx` on Windows) to set the environ variable first.
Then you can login like this:

    scm login

There will be prompts asking for username and password.
If you don't want to enter username and password, you can also login like this:

    scm login -u xxx -p xxx

### API help message
Use `help apiname` to check the parameters and descriptions of an API.
For example, `help find-player-by-id`.
```
{
  "path": "/api/rest/players/{id}",
  "description": "Returns information about the player.",
  "operation": "GET",
  "pathParameters": [
    {
      "id": 9310,
      "name": "id",
      "description": "ID of the player to be fetched",
      "datatype": "INTEGER"
    }
  ],
  "queryParameters": [
    {
      "id": 9311,
      "name": "fields",
      "description": "A comma separated list of fields you want to include on the response object.<b>Note:</b> the field <i>id</i> will always be included as a part of the response object.Remember to URL encode your fields.",
      "datatype": "STRING"
    }
  ],
  "queryBody": null
}
```

### Operates API
Use `scm apiname [options]` to operate the API.
For example, list all the players.

    scm list-players

Here's the result.
```
200
{
  "list": [
    {
      "id": 2,
      "name": "SCALA",
      "uuid": "36deba9c-c97d-48c8-a301-bfe3e795243b",
      "previewPlayer": false,
      "enabled": true,
      "type": "SCALA",
      "distributionServer": {
        "id": 1,
        "name": "Main",
        "driver": "IP_P2P"
      },
      "playerDisplays": [
        {
          "id": 2,
          "name": "Display 1",
          "screenCounter": 1
        }
      ],
      "requestLogs": false,
      "downloadThreads": 1,
      "unusedFilesCache": 24,
      "planDeliveryMethod": "CONTENT_MANAGER_DIRECT",
      "pollingInterval": 1,
      "pollingUnit": "MINUTES",
      "logLevel": "normal",
      "active": "UNKNOWN",
      "lastModified": "2015-05-18 21:52:16"
    },
    {
      "id": 1,
      "name": "test",
      "uuid": "fb9a7df1-f972-4460-a2c2-1c09dbf655f0",
      "previewPlayer": false,
      "enabled": true,
      "type": "SCALA",
      "distributionServer": {
        "id": 1,
        "name": "Main",
        "driver": "IP_P2P"
      },
      "playerDisplays": [
        {
          "id": 1,
          "name": "Display 1",
          "screenCounter": 1
        }
      ],
      "requestLogs": false,
      "downloadThreads": 1,
      "unusedFilesCache": 24,
      "planDeliveryMethod": "CONTENT_MANAGER_DIRECT",
      "pollingInterval": 1,
      "pollingUnit": "MINUTES",
      "logLevel": "normal",
      "active": "UNKNOWN",
      "lastModified": "2015-05-18 21:48:22"
    }
  ],
  "offset": 0,
  "count": 2
}
```
To only show some fields.

    scm list-players --qry-param.fields=namd,type

And the result looks like:
```
200
{
  "list": [
    {
      "id": 2,
      "name": "SCALA",
      "type": "SCALA"
    },
    {
      "id": 1,
      "name": "test",
      "type": "SCALA"
    }
  ],
  "offset": 0,
  "count": 2
}
```
To filter players.

    scm list-players --qry-param.filters.name.values=test --qry-param.filters.comparator=like

Here you need to know that `--qry-param.filters.name.values=test --qry-param.filters.comparator=like` is equal to `filters={'name': {'values': test}, 'comparator': 'like'}`, the options will be recursively merged.
```
200
{
  "list": [
    {
      "id": 1,
      "name": "test",
      "uuid": "fb9a7df1-f972-4460-a2c2-1c09dbf655f0",
      "previewPlayer": false,
      "enabled": true,
      "type": "SCALA",
      "distributionServer": {
        "id": 1,
        "name": "Main",
        "driver": "IP_P2P"
      },
      "playerDisplays": [
        {
          "id": 1,
          "name": "Display 1",
          "screenCounter": 1
        }
      ],
      "requestLogs": false,
      "downloadThreads": 1,
      "unusedFilesCache": 24,
      "planDeliveryMethod": "CONTENT_MANAGER_DIRECT",
      "pollingInterval": 1,
      "pollingUnit": "MINUTES",
      "logLevel": "normal",
      "active": "UNKNOWN",
      "lastModified": "2015-05-18 21:48:22"
    }
  ],
  "offset": 0,
  "count": 1
}
```

### Display description
By default, scm only shows auto-completions, if you want every description of every completion, append `--display-meta` to your command line when you login.

## Note
All the api informations, including methods, description, path parameters, query parameters, query body are pull from the api doc, there may be mistakes, so you might need to change the `completion.json` on your own or just make a pull request.

# License
[MIT](https://github.com/rookiebulls/scm/blob/master/LICENSE)

