__version__ = 103
PLUGIN_ID = "gitago.TikTokLive"
PLUGIN_NAME = "TikTokLive"
PLUGIN_FOLDER = "TikTokLive"
PLUGIN_ICON = ""


TP_PLUGIN_INFO = {
    'sdk': 6,
    'version': __version__,
    'name': f"{PLUGIN_NAME} Plugin",
    'id': PLUGIN_ID,
    "plugin_start_cmd_windows": f"%TP_PLUGIN_FOLDER%{PLUGIN_FOLDER}\\{PLUGIN_NAME}_Plugin.exe",
    "plugin_start_cmd_linux": f"sh %TP_PLUGIN_FOLDER%{PLUGIN_FOLDER}//start.sh {PLUGIN_NAME}_Plugin",
    "plugin_start_cmd_mac": f"sh %TP_PLUGIN_FOLDER%{PLUGIN_FOLDER}//start.sh {PLUGIN_NAME}_Plugin",
    'configuration': {
        "colorDark": "#23272a",
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
    },
    'AutoConnect': {
        'name': "Auto Connect",
        'type': "text",
        'default': "False",
        'readOnly': False,
        'value': None
    },
}




TP_PLUGIN_CATEGORIES = {
    "main": {
        'id': PLUGIN_ID + ".main",
        'name' : "TikTokLive",
        'imagepath': f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\{PLUGIN_ICON}",
    },
    "New Follower": {
        'id': PLUGIN_ID + ".newFollower",
        'name' : "TikTokLive New Follower",
    },
    "New Like": {
        'id': PLUGIN_ID + ".newLike",
        'name' : "TikTokLive New Like",
    },
    "New Share": {
        'id': PLUGIN_ID + ".newShare",
        'name' : "TikTokLive New Share",
    },
    "New Comment": {
        'id': PLUGIN_ID + ".newComment",
        'name' : "TikTokLive New Comment",
    },
    "New Gift": {
        'id': PLUGIN_ID + ".newGift",
        'name' : "TikTokLive New Gift",
    },
    "New Join": {
        'id': PLUGIN_ID + ".newJoin",
        'name' : "TikTokLive New Join",
    },
    "Message - 1": {
        'id': PLUGIN_ID + ".message_1",
        'name' : "TikTokLive Message 1",
    },
    "Message - 2": {
        'id': PLUGIN_ID + ".message_2",
        'name' : "TikTokLive Message 2",
    },
    "Message - 3": {
        'id': PLUGIN_ID + ".message_3",
        'name' : "TikTokLive Message 3",
    },
    "Message - 4": {
        'id': PLUGIN_ID + ".message_4",
        'name' : "TikTokLive Message 4",
    },
    "Message - 5": {
        'id': PLUGIN_ID + ".message_5",
        'name' : "TikTokLive Message 5",
    },
    'Top 5 Viewers': {
        'id': PLUGIN_ID + ".top_viewer",
        'name' : "TikTokLive Top 5 Viewers",
    }

}


TP_PLUGIN_ACTIONS = {
    'Connect': {
        'category': "main",
        'id': PLUGIN_ID + ".act.Connect",
        'name': "TikTok | Connect / Disconnect",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Connect or Disconnect from your TikTok Live Chat",
        'format': "$[1] to or from the chat",
        'data': {
        'On/Off/Toggle': {
                'id': PLUGIN_ID + ".act.light.on.off.toggle",
                'type': "choice",
                'label': "Text",
                'default': "Connect",
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
    ## Follower Count
    'Follower Count': {
        'category': "main",
        'id': PLUGIN_ID + ".state.follower_count",
        'desc': "TikTok | Live Video Follower Count",
        'default': ""
    },

  # 
  # ## Follower
  # 'New Follower': {
  #     'category': "New Follower",
  #     'id': PLUGIN_ID + ".state.newFollower",
  #     'desc': "TikTok | New Follower Event",
  #     'default': ""
  # },
  # 'New Follower Name': {
  #     'category': "New Follower",
  #     'id': PLUGIN_ID + ".state.newFollower.Name",
  #     'desc': "TikTok | New Follower Name",
  #     'default': ""
  # },
  # 'New Follower ID': {
  #     'category': "New Follower",
  #     'id': PLUGIN_ID + ".state.newFollower.ID",
  #     'desc': "TikTok | New Follower ID",
  #     'default': ""
  # },
  # 'New Follower Avatar': {
  #     'category': "New Follower",
  #     'id': PLUGIN_ID + ".state.newFollower.Avatar",
  #     'desc': "TikTok | New Follower Avatar",
  #     'default': ""
  # },
  # 'New Follow Followers': {
  #     'category': "New Follower",
  #     'id': PLUGIN_ID + ".state.newFollower.Followers",
  #     'desc': "TikTok | New Follower Followers",
  #     'default': ""
  # },


  # ## Like
  # 'New Like Nickname': {
  #     'category': "New Like",
  #     'id': PLUGIN_ID + ".state.newLike.Name",
  #     'desc': "TikTok | New Like Nickname",
  #     'default': ""
  # },
   'New Likers Total Likes': {
       'category': "New Like",
       'id': PLUGIN_ID + ".state.newLike.TimesLiked",
       'desc': "TikTok | New Like Times Liked",
       'default': ""
   },
  # 'New Like Avatar': {
  #     'category': "New Like",
  #     'id': PLUGIN_ID + ".state.newLike.Avatar",
  #     'desc': "TikTok | New Like Avatar",
  #     'default': ""
  # },
  # 'New Like ID': {
  #     'category': "New Like",
  #     'id': PLUGIN_ID + ".state.newLike.UserID",
  #     'desc': "TikTok | New Like ID",
  #     'default': ""
  # },
  # 'New Like Followers': {
  #     'category': "New Like",
  #     'id': PLUGIN_ID + ".state.newLike.Followers",
  #     'desc': "TikTok | New Like Followers",
  #     'default': ""
  # },


    ## Gifts Extras
    'New Gift Total Gifts': {
        'category': "New Gift",
        'id': PLUGIN_ID + ".state.newGift.TotalGifts",
        'desc': "TikTok | New Gift: Total Gifts",
        'default': ""
    },
    'New Gift Gift ID': {
        'category': "New Gift",
        'id': PLUGIN_ID + ".state.newGift.GiftID",
        'desc': "TikTok | New Gift: Gift ID",
        'default': ""
    },
    'New Gift Gift Name': {
        'category': "New Gift",
        'id': PLUGIN_ID + ".state.newGift.GiftName",
        'desc': "TikTok | New Gift: Gift Name",
        'default': ""
    },





  # ## Share
  # 'Most Recent Share': {
  #     'category': "Most Recent",
  #     'id': PLUGIN_ID + ".state.newShare",
  #     'desc': "TikTok | Most Recent Share",
  #     'default': ""
  # },

  # 
  # 'Most Recent Comment': {
  #     'category': "Most Recent",
  #     'id': PLUGIN_ID + ".state.newComment",
  #     'desc': "TikTok | Most Recent Comment",
  #     'default': ""
  # },
  # 'Most Recent Gift': {
  #     'category': "Most Recent",
  #     'id': PLUGIN_ID + ".state.newGift",
  #     'desc': "TikTok | Most Recent Gift",
  #     'default': ""
  # },
  # 'Most Recent Join': {
  #     'category': "Most Recent",
  #     'id': PLUGIN_ID + ".state.newJoin",
  #     'desc': "TikTok | Most Recent Join",
  #     'default': ""
  #  },
  #  'Live Share URL': {
  #      'category': "Live Share URL",
  #      'id': PLUGIN_ID + ".state.ShareURL",
  #      'desc': "TikTok | Live Share URL",
  #      'default': ""
  #  },
    
}


## Creating states for Events details per user
action_types = ["message"]  # Add more action types if needed
ids = ['username', 'userID', 'message', 'followers', 'followerRole', 'avatar']  # Add more IDs as needed
newchatStates = {}
for index in range(6):
    for action_type in action_types:
        for identifier in ids:
            key = f'{action_type}_{index}.{identifier.capitalize()}'  # Generate the key
            desc = f'TikTok | {action_type.capitalize()} {index} - {identifier.capitalize()} '  # Generate the description

            configuration = {
                'category': f'{action_type.capitalize()} - {index}',
                'id': f'{PLUGIN_ID}.state.{key}',
                'desc': desc,
                'default': ""
            }
            newchatStates[key] = configuration
TP_PLUGIN_STATES.update(newchatStates)


## Creating states for Events details per user
action_types = ['Like', 'Gift', 'Share', 'Join', 'Comment', 'Follower']  # Add more action types if needed
ids = ['Name', 'UserID', 'Avatar', 'Followers', ""]  # Add more IDs as needed
configurations = {}
for action_type in action_types:
    for identifier in ids:
        if identifier == "":  # If the identifier is blank, skip it
            key = f'new{action_type.capitalize()}'  # Generate the key
        else:
            key = f'new{action_type.capitalize()}.{identifier}'  # Generate the key
        desc = f'TikTok | New {action_type}: {identifier}'  # Generate the description
        configuration = {
            'category': f'New {action_type}',
            'id': f'{PLUGIN_ID}.state.{key}',
            'desc': desc,
            'default': ""
        }
        configurations[key] = configuration
TP_PLUGIN_STATES.update(configurations)


## lets do one for top veiwers as action_type, since theres only one we shouldnt need to interate over it, right?
#  and then CoinsGiven & name would be the ids and we are gonna have a top 5..
action_type = "top_viewer"  # Only one action_type
# Define the IDs for the top viewers
ids = ['CoinsGiven', 'Name', 'UserID']
topfive = {}
for index in range(6):
    for identifier in ids:
        key = f'{action_type}_{index}.{identifier}'  # Generate the key
        desc = f'Top Viewer {index + 1} - {identifier.capitalize()} '  # Generate the description

        configuration = {
            'category': 'Top 5 Viewers',
            'id': f'{PLUGIN_ID}.state.{key}',
            'desc': desc,
            'default': ""
        }
        topfive[key] = configuration
TP_PLUGIN_STATES.update(topfive)




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

    
### - OBS STUFF import time
### - OBS STUFF 
### - OBS STUFF import obsws_python as obs
### - OBS STUFF 
### - OBS STUFF 
### - OBS STUFF class Observer:
### - OBS STUFF     def __init__(self):
### - OBS STUFF         self._client = obs.EventClient()
### - OBS STUFF         ## get the status of a source
### - OBS STUFF         
### - OBS STUFF         self._client.callback.register(
### - OBS STUFF             [
### - OBS STUFF                 self.on_current_program_scene_changed,
### - OBS STUFF                 self.on_scene_created,
### - OBS STUFF                 self.on_input_mute_state_changed,
### - OBS STUFF                 self.on_exit_started
### - OBS STUFF             ]
### - OBS STUFF         )
### - OBS STUFF         print(f"Registered events: {self._client.callback.get()}")
### - OBS STUFF         self.running = True
### - OBS STUFF 
### - OBS STUFF     def on_current_program_scene_changed(self, data):
### - OBS STUFF         """The current program scene has changed."""
### - OBS STUFF         print(f"Switched to scene {data.scene_name}")
### - OBS STUFF 
### - OBS STUFF     def on_scene_created(self, data):
### - OBS STUFF         """A new scene has been created."""
### - OBS STUFF         print(f"scene {data.scene_name} has been created")
### - OBS STUFF 
### - OBS STUFF     def on_input_mute_state_changed(self, data):
### - OBS STUFF         """An input's mute state has changed."""
### - OBS STUFF         print(f"{data.input_name} mute toggled")
### - OBS STUFF 
### - OBS STUFF     def on_exit_started(self, _):
### - OBS STUFF         """OBS has begun the shutdown process."""
### - OBS STUFF         print(f"OBS closing!")
### - OBS STUFF         self._client.unsubscribe()
### - OBS STUFF         self.running = False
### - OBS STUFF 
### - OBS STUFF     def get_source_visible(self, source_name):
### - OBS STUFF         """Get the visibility of a source."""
### - OBS STUFF         return req_client.get_source_active(source_name)
### - OBS STUFF    
### - OBS STUFF 
### - OBS STUFF if __name__ == "__main__":
### - OBS STUFF     req_client = obs.ReqClient()
### - OBS STUFF     observer = Observer()
### - OBS STUFF     response= observer.get_source_visible("TEST_TEXT")
### - OBS STUFF    # print(response.source_name)
### - OBS STUFF     print(response.video_active)
### - OBS STUFF     print(response.video_showing)
### - OBS STUFF     while observer.running:
### - OBS STUFF         time.sleep(0.1)