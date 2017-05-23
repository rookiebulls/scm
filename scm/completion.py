# -*- coding: utf-8 -*-

import os
import json

__all__ = ('custom_completion', 'completions')

custom_completion = {
    'create-player': {
        'queryBody': {
            "name": "MyPlayer",
            "description": "DescriptionforPlayer",
            "unusedFilesCache": "24",
            "downloadThreads": "1",
            "type": "SCALA",
            "metadataValue": [{
                "value": "TRUE",
                "playerMetadata": {
                    "id": {"metadataid"},
                    "datatype": "BOOLEAN",
                    "valueType": "ANY"
                }
            }]
        }
    },
    'create-normal-playlist': {
        'queryBody': {
            'name': 'MynormalPlaylist',
            'description': 'DescriptionfornormalPlaylist',
            'playlistType': 'MEDIA_PLAYLIST',
            'healthy': 'true',
            'enableSmartPlaylist': 'false'
        }
    }
}


def get_completions(filename):
    with open(filename) as f:
        return json.load(f)


completions = get_completions(os.path.join(
    os.path.dirname(__file__), 'completions.json'))
