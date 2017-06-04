# About

> scm is a command line tool for operating Scala Content Manager's restful API.

![screenshot](http://olgvodd4s.bkt.clouddn.com/scm-screenshot.png)

## Installation
1. clone this repositry
2. `cd scm`
3. `pip install --editable .`

## Usage
Type `scm --help` for all the commands and options.

### Login
    scm login http://xxxx

scm use environ variable 'CM_URL' as the default Content Manager url. So if you don't want to specify the url in the command line, you can use command `export CM_URL=http://xxxx` (`set CM_URL=http://xxxx` on Windows) to set the environ variable first.
Then you can login like this.

    scm login

There will be prompts asking for username and password. You can skip this step by passing username and password.

    scm login -u xxx -p xxx

### API help message
Use `help apiname` to show the useful message of an API.
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

Options starts with `--path-param` means path parameters(key "pathParameters" of the api help message), `--qry-param` means query parameters, and `--qry-body` means query body.

Take the player CURD for example.

#### Create player

    scm create-player --qry-body.name=newplayer --qry-body.type=SCALA --qry-body.description="a new player"

```
200
{
  "id": 4,
  "name": "newplayer",
  "description": "a new player",
  "uuid": "62a2fa4b-77e5-412c-b750-cc780724c6ab",
  "previewPlayer": false,
  "enabled": true,
  "type": "SCALA",
  "playerDisplays": [
    {
      "id": 4,
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
  "lastModified": "2015-06-04 07:09:42"
}
```

#### Update player

    scm update-player --path-param.id=4 --qry-body.name=updatedplayer

```
200
{
  "value": "done"
}
```

#### Retrieve player

    scm find-player-by-id --path-param.id=4 --qry-param.fields=name,type,description

```
200
{
  "id": 4,
  "name": "updatedplayer",
  "description": "a new player",
  "type": "SCALA"
}
```

#### Delete player

    scm delete-player-by-id --path-param.id=4

```
204

```

#### Get all players

    scm list-players

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

    scm list-players --qry-param.fields=name,type

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
By default, scm only shows auto-completions, if you want every description of every completion, append `--display-meta` to your command line when login.

## Note
All the api informations, including methods, description, path parameters, query parameters, query body are pull from the api doc, there may be mistakes, so you might need to change the [completion.json](https://github.com/rookiebulls/scm/blob/master/scm/completions.json) on your own or make a pull request.

# License
[MIT](https://github.com/rookiebulls/scm/blob/master/LICENSE)

