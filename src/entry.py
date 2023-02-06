__version__ = 100
PLUGIN_ID = "tp.plugin.TikTokLive"
PLUGIN_NAME = "TikTokLive"


TP_PLUGIN_INFO = {
    'sdk': 6,
    'version': __version__,  # TP only recognizes integer version numbers
    'name': f"{PLUGIN_NAME} Plugin",
    'id': PLUGIN_ID,
    "plugin_start_cmd_windows": f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\{PLUGIN_NAME}_Plugin.exe",
  # "plugin_start_cmd_linux": "sh %TP_PLUGIN_FOLDER%YouTube_Plugin//start.sh TP_YouTube_Plugin",
 #   "plugin_start_cmd_mac": f"sh %TP_PLUGIN_FOLDER%{PLUGIN_NAME}//start.sh {PLUGIN_NAME}_Plugin",
    'configuration': {
        "colorDark": "#23272a", ##23272a
        "colorLight": "#57ad72" 
    }
}



TP_PLUGIN_SETTINGS = {
    
    'Username': {
        'name': "TikTok Username",
        'type': "text",
        'default': "",
        'readOnly': False,
        'value': None  
    }
}




TP_PLUGIN_CATEGORIES = {
    "main": {
        'id': PLUGIN_ID + ".main",
        'name' : "TikTokLive",
        'imagepath': f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\TikTokLive.png",
    },
    "Most Recent": {
        'id': PLUGIN_ID + ".recent",
        'name' : "TikTokLive Recents",
    }
}


TP_PLUGIN_ACTIONS = {
    'Connect': {
        'category': "main",
        'id': PLUGIN_ID + ".act.Connect",
        'name': "TikTok | Connect / Disconnect / Reconnect",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Connect / Disconnect / Reconnect from your TikTok Live Chat",
        'format': "$[1] to or from the chat",
        'data': {
        'On/Off/Toggle': {
                'id': PLUGIN_ID + ".act.light.on.off.toggle",
                'type': "choice",
                'label': "Text",
                'default': "Toggle",
                "valueChoices": ["Connect", "Disconnect"]
        }
        }
    },
    
    
}


TP_PLUGIN_STATES = {
    'Status': {
        'category': "main",
        'id': PLUGIN_ID + ".state.plugin_status",
        'desc': "TikTok | Plugin Status",
        'default': ""
    },
    'Like Count': {
        'category': "main",
        'id': PLUGIN_ID + ".state.like_count",
        'desc': "TikTok | Live Video Like Count",
        'default': ""
    },
    'Viewer Count': {
        'category': "main",
        'id': PLUGIN_ID + ".state.viewer_count",
        'desc': "TikTok | Live Video Viewer Count",
        'default': ""
    },
    
    
    'Most Recent Follower': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.newFollower",
        'desc': "TikTok | Most Recent Follower",
        'default': ""
    },
    
    'Most Recent Like Name': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.Recent.Like.Name",
        'desc': "TikTok | Most Recent Like Name",
        'default': ""
    },
    
    'Most Recent Likers Total Likes': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.Recent.Like.Name.TimesLiked",
        'desc': "TikTok | Most Recent Like Times Liked",
        'default': ""
    },
    
    
    'Most Recent Share': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.newShare",
        'desc': "TikTok | Most Recent Share",
        'default': ""
    },
    'Most Recent Comment': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.newComment",
        'desc': "TikTok | Most Recent Comment",
        'default': ""
    },
    'Most Recent Gift': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.newGift",
        'desc': "TikTok | Most Recent Gift",
        'default': ""
    },
    'Most Recent Join': {
        'category': "Most Recent",
        'id': PLUGIN_ID + ".state.newJoin",
        'desc': "TikTok | Most Recent Join",
        'default': ""
    },
    
}


TP_PLUGIN_CONNECTORS = {}


TP_PLUGIN_EVENTS = {
    "0": {
        'id': PLUGIN_ID + ".event.newFollower",
        'name':"TikTok | New Follower",
        'category': "main",
        "format":"When receiving a new follower $val ",
        "type":"communicate",
        "valueType":"choice",
        "valueChoices": [
        "True",
        "False"
    ],
    "valueStateId": PLUGIN_ID + ".state.newFollower",
    },
    "1": {
        'id': PLUGIN_ID + ".event.newLike",
        'name':"TikTok | New Like",
        'category': "main",
        'format':"When receiving a new like $val ",
        'type':"communicate",
        'valueType':"choice",
        'valueChoices': ['True'],
        'valueStateId': PLUGIN_ID + ".state.newLike",
    },
    "2": {
        'id': PLUGIN_ID + ".event.newShare",
        'name':"TikTok | New Share",
        'category': "main",
        'format':"When receiving a new share $val ",
        'type':"communicate",
        'valueType':"choice",
        'valueChoices': ['True'],
        'valueStateId': PLUGIN_ID + ".state.newShare",
    },
    "3": {
        'id': PLUGIN_ID + ".event.newComment",
        'name':"TikTok | New Comment",
        'category': "main",
        'format':"When receiving a new comment $val ",
        'type':"communicate",
        'valueType':"choice",
        'valueChoices': ['True'],
        'valueStateId': PLUGIN_ID + ".state.newComment",
    },
    "4": {
        'id': PLUGIN_ID + ".event.newGift",
        'name':"TikTok | New Gift",
        'category': "main",
        'format':"When receiving a new gift $val ",
        'type':"communicate",
        'valueType':"choice",
        'valueChoices': ['True'],
        'valueStateId': PLUGIN_ID + ".state.newGift",
    },
    "5": {
        'id': PLUGIN_ID + ".event.newJoin",
        'name':"TikTok | New Join",
        'category': "main",
        'format':"When receiving a new join $val ",
        'type':"communicate",
        'valueType':"choice",
        'valueChoices': ['True'],
        'valueStateId': PLUGIN_ID + ".state.newJoin",
    }
}
