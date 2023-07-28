## Tik Tok Live Events

import asyncio
from typing import Optional, List, Callable, Dict
from TikTokLive import TikTokLiveClient
from TikTokLive.types import FailedConnection, FailedParseUserHTML, FailedFetchRoomInfo, AlreadyConnecting
from TikTokLive.types.events import CommentEvent, ConnectEvent, FollowEvent, ShareEvent, MoreShareEvent, LikeEvent, JoinEvent, GiftEvent, LiveEndEvent, ViewerUpdateEvent
from TikTokLive import types
import threading

import sys
import time

from entry import PLUGIN_ID, TP_PLUGIN_INFO, __version__, PLUGIN_NAME
from TouchPortalAPI.logger import Logger
from argparse import ArgumentParser
import TouchPortalAPI as TP
from collections import deque
import base64
import requests
import webbrowser
from update_check import *


## should we add 'emote'.. or Envelope, ranking_update or user_rankingUpdate? would just say when a new top viewer is made..

## Need to add 'moreshareEvent' - Event that fires when a user shared the livestream more than 5 users or more than 10 users
## Consider adding 'EnvelopeEvent' - Event that fires when a user sends a envelope/treasurebox
## Consider adding 'MicBattleEvent & MicArmiesEvent' - Event that fires when a user starts a mic battle
loop = asyncio.new_event_loop()
g_log = Logger(name = PLUGIN_ID)

try:
    TPClient = TP.Client(
        pluginId = PLUGIN_ID,  # required ID of this plugin
        sleepPeriod = 0.05,    # allow more time than default for other processes
        autoClose = True,      # automatically disconnect when TP sends "closePlugin" message
        checkPluginId = True,  # validate destination of messages sent to this plugin
        maxWorkers = 4,        # run up to 4 event handler threads
        updateStatesOnBroadcast = False,  # do not spam TP with state updates on every page change
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")





def handleSettings(settings, on_connect=False):
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    autoConnect = settings.get('Auto Connect', False)
    tk.Username = settings.get('TikTok Username')
    if autoConnect == "True":
        if tk.Username != "":
            tk.startup = True
            tk.set_client(tk.Username)
            run_tk()
            tk.isalive = True
    

#--- On Startup ---#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)

        ## Checking for Updates
    try:
        github_check, message = plugin_update_check(str(data['pluginVersion']))
        if github_check == True:
            TPClient.showNotification(
                notificationId= f"{PLUGIN_ID}.TP.Plugins.Update_Check",
                title=f"{PLUGIN_NAME} {github_check} is available",
                msg=f"A new version of {PLUGIN_NAME} is available and ready to Download.\nThis may include Bug Fixes and or New Features\n\nPatch Notes\n{message} ",
                options= [{
                "id":f"{PLUGIN_ID}.tp.update.download",
                "title":"Click to Update!"
            }])
    except:
        print("Error Checking for Updates")
        
    

#--- Settings handler ---#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)



@TPClient.on(TP.TYPES.onListChange)
def listChangeAction(data):
    print(data)

@TPClient.on(TP.TYPES.onNotificationOptionClicked)
def onNoticationClicked(data):
    if data['optionId'] == f'{PLUGIN_ID}.tp.update.download':
        github_check = TouchPortalAPI.Tools.updateCheck(GITHUB_USER_NAME, GITHUB_PLUGIN_NAME)
        url = f"https://github.com/{GITHUB_USER_NAME}/{GITHUB_PLUGIN_NAME}/releases/tag/{github_check}"
        webbrowser.open(url, new=0, autoraise=True)


#--- Action handler ---#
@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    g_log.debug(f"Action: {data}")
    if data['actionId'] == PLUGIN_ID + ".act.Connect":
        if data['data'][0]['value'] == "Disconnect":         
            tk.stop_TikTok_Thread()
       
        if data['data'][0]['value'] == "Connect":
            if tk.Username != "":
                tk.startup = True
                tk.set_client(tk.Username)
                run_tk()
                tk.isalive = True


# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')
    # We do not need to disconnect manually because we used `autoClose = True`










class TikTok_Client:
    def __init__(self,) -> None:
        self.tiktok: TikTokLiveClient = None
        self.isalive = False
        self.startup = False
        self.Username = None
        self.thread = None
        self.prev_viewer_count = 0
        self.last_5_messages = deque(maxlen=5)


    def set_client(self, tiktok_channel):
        self.tiktok = TikTokLiveClient(tiktok_channel, **{
            "process_initial_data": False  # Spams cached messages on start, must be disabled   
        })
        g_log.info("Adding Listeners")
        
        self.tiktok.add_listener("comment", self.on_comment)
        self.tiktok.add_listener("follow", self.on_follow)
        self.tiktok.add_listener("like", self.on_like)
        self.tiktok.add_listener("share", self.on_share)
        self.tiktok.add_listener("join", self.on_join)
        self.tiktok.add_listener("gift", self.on_gift)
        self.tiktok.add_listener("viewer_update", self.on_viewercountUpdate)
        self.tiktok.add_listener("connect", self.on_connect)
        self.tiktok.add_listener("disconnect", self.on_disconnect)
        self.tiktok.add_listener("live_end", self.on_disconnect)
        g_log.info("Starting TikTok Live Chat")
        return self.tiktok
    

    def start_tiktok(self):
        max_retry_interval = 45  # Maximum retry interval in seconds
        min_retry_interval = 2   # Minimum retry interval in seconds
        retry_interval = min_retry_interval
        retry_attempt = 0

        while True:
            if self.startup:
                try:
                    attempt = tk.tiktok.run()
                    if attempt:
                        break  # Break out of the loop if the connection is successful
                except FailedConnection:
                    g_log.info("Failed to connect to TikTok. Trying Again...")
                except FailedParseUserHTML as e:
                    g_log.info("Failed to parse user HTML (User might be offline). Trying Again...")
                    g_log.info(f"Error message: {e}")
                except FailedFetchRoomInfo as e:
                    g_log.info("Failed to fetch room info. Trying Again...")
                except AlreadyConnecting as e:
                    g_log.info("Attempting to Connect, Trying Again...")            
            retry_attempt += 1
            retry_interval = min_retry_interval + retry_attempt 
            retry_interval = min(retry_interval, max_retry_interval)
            time.sleep(retry_interval)


    def stop_TikTok_Thread(self):
        try:
            self.startup = False
            self.tiktok.remove_all_listeners()
            self.tiktok.stop()
            time.sleep(2)
            tk.isalive = False
            g_log.info("THE TIKTOK LIVE CHAT HAS BEEN STOPPED")
        except AttributeError:
            g_log.info("TikTok thread is not running.")
            self.startup = False
            tk.isalive = False
            pass
        
    def update_userAvatar(self, event, type):
        try:
            for x in event.user.avatar.urls:
                if "shrink" not in x.lower():
                    base64_data = convert_image_to_base64(x)
                    if base64_data:
                        TPClient.stateUpdate(PLUGIN_ID + f".state.new{type}.Avatar", base64_data)
                        break  # Break out of the loop once a valid image URL is found
        except TypeError as e:
            print(e)
    
    def update_message_states(self,event):
        for index, message in enumerate(self.last_5_messages):
            TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.Username", f"Message_{index + 1} - Username", str(message['nickname']))
            TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.Message", f"Message_{index + 1} - Message", str(message['comment']))
            TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.UserID", f"Message_{index + 1} - UserID", str(event.user.user_id))
            TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.Followers", f"Message_{index + 1} - Followers", str(event.user.info.followers))
            TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.FollowerRole", f"Message_{index + 1} - FollowerRole", str(event.user.info.follow_role))

            ## do avatar later
            #  TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.Avatar", f"Message_{index + 1} - Avatar", str(event.user.avatar.urls[0]))

    
    async def update_states_from_events(self, event, eventType):        
        if eventType == "Like":
            TPClient.stateUpdate(PLUGIN_ID + ".state.newLike", "True")
            TPClient.stateUpdate(PLUGIN_ID + f".state.{eventType}_count", str(event.total_likes))
            TPClient.stateUpdate(PLUGIN_ID + ".state.newLike.TimesLiked", str(event.likes))
            TPClient.stateUpdate(PLUGIN_ID + ".state.like_count", str(event.total_likes))
            TPClient.stateUpdate(PLUGIN_ID + ".state.newLike", "False")
            self.update_userStates(event, eventType)

        
        if eventType == "Gift":
            TPClient.stateUpdate(PLUGIN_ID + ".state.newGift", "True")
            TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Gift.GiftID", str(event.gift.id))
            TPClient.stateUpdate(PLUGIN_ID + ".state.newGift.TotalGifts", str(event.gift.count))
            TPClient.stateUpdate(PLUGIN_ID + ".state.newGift.GiftName", str(event.gift.info.name))
            TPClient.stateUpdate(PLUGIN_ID + ".state.newGift", "False")
            self.update_userStates(event, eventType)

          #base_64_gift = convert_image_to_base64(event.gift.info.urls[0])
          #if base_64_gift:
          #    TPClient.stateUpdate(PLUGIN_ID + ".state.newGift.Avatar", base_64_gift)

        
        if eventType == "Follower":
           # print("Follow event", event)
            TPClient.stateUpdate(PLUGIN_ID + ".state.newFollower", "True")
            TPClient.stateUpdate(PLUGIN_ID + ".state.follower_count", str(event.total_followers))
            TPClient.stateUpdate(PLUGIN_ID + ".state.newFollower", "False")
            self.update_userStates(event, eventType)

        if eventType == "Share":
            TPClient.stateUpdate(PLUGIN_ID + ".state.newShare", "True")
            TPClient.stateUpdate(PLUGIN_ID + ".state.newShare", "False")
            self.update_userStates(event, eventType)

        if eventType == "Join":
            #print("Join event", event)
            ## Do we care about join events?
            pass


    def update_userStates(self, event, type):
        """ Updates the basic user info for specified event & userAvatar """
        TPClient.stateUpdate(PLUGIN_ID + f".state.new{type}.Name", str(event.user.nickname))
        TPClient.stateUpdate(PLUGIN_ID + f".state.new{type}.UserID", str(event.user.user_id))
        TPClient.stateUpdate(PLUGIN_ID + f".state.new{type}.Followers", str(event.user.info.followers))
        self.update_userAvatar(event, type)





    async def on_connect(self, event: ConnectEvent):
        """ 
        When the Streamer connects to TikTok Live Chat
        """
        g_log.info("Connected to Room ID: %s", tk.tiktok.room_id)
        room_info = await tk.tiktok.retrieve_room_info()
        TPClient.stateUpdate(PLUGIN_ID + ".state.ShareURL", str(room_info['share_url']))


    def on_disconnect(eself, event: LiveEndEvent):
        """ 
        When the Streamer disconnects from TikTok Live Chat
        """
        g_log.info("Disconnected from TikTok Live Chat")
        tk.stop_TikTok_Thread()



    async def on_comment(self, event: CommentEvent):
        """ 
        Called when a comment is received
        - Updates associated TouchPortal States
        """
        g_log.debug(f"{event.user.nickname} -> {event.comment}")
        #keeping only the last 5 messages in a variable at any given time.. 
        tk.last_5_messages.append({'nickname': event.user.nickname, 'comment':event.comment})
        tk.update_message_states(event)




    async def on_follow(self, event: FollowEvent):
        """
        When a user follows the stream
        """
        message: str = f"{event.user.user_id} followed!{event.user.user_id}"
        g_log.debug(message)
        await tk.update_states_from_events(event, "Follower")



    async def on_like(self, event: LikeEvent):
        """ 
        When a user likes the stream
        - Updates associated TouchPortal States
        """
        message: str = f"{event.user.user_id} liked the stream {event.likes} times, there is now {event.total_likes} total likes!"
        g_log.debug(message)
        await tk.update_states_from_events(event, "Like")



    async def on_share(self, event: ShareEvent):
        """ 
        When a user shares the stream
        - Updates associated TouchPortal States
        """
        message: str = f"{event.user.user_id} shared the streamer!"
        g_log.debug(message)
        await tk.update_states_from_events(event, "Share")



    async def on_join(self, event: JoinEvent):
        """ 
        When a user joins the room
        - Updates associated TouchPortal States
        """
        await tk.update_states_from_events(event, "Join")



    async def on_gift(self, event: GiftEvent):
        """ 
        When a gift is sent to user
        - Updates associated TouchPortal States
        """
        if event.gift.info.type == 1 and event.gift.repeat_end == 1:
            g_log.debug(f"{event.user.user_id} sent {event.gift.count}x \"{event.gift.info.name}\"")

        # It's not type 1, which means it can't have a streak & is automatically over
        elif event.gift.info.type != 1:
            message: str = f"{event.user.user_id} sent \"{event.gift.info.name}\""
            g_log.debug(message)
            TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Gift.GiftName", str(event.gift.info.name))

        await tk.update_states_from_events(event, "Gift")




    async def on_viewercountUpdate(self, event: ViewerUpdateEvent):
        """
        Called when the viewer count changes
        - Updates associated TouchPortal States
        """
        TPClient.stateUpdate(PLUGIN_ID + ".state.viewer_count", str(event.viewer_count))
        for x in event.top_viewers[0:5]:
            TPClient.createState(PLUGIN_ID + f".act.top_viewer_{event.top_viewers.index(x) + 1}.Name",
                                f"Top Viewer {event.top_viewers.index(x) + 1} - Name",
                                str(x.user.nickname),
                                "Top 5 Viewers")
            TPClient.createState(PLUGIN_ID + f".act.top_viewer_{event.top_viewers.index(x) + 1}.UserID",
                                f"Top Viewer {event.top_viewers.index(x) + 1} - UserID",
                                str(x.user.user_id),
                                "Top 5 Viewers")
            TPClient.createState(PLUGIN_ID + f".act.top_viewer_{event.top_viewers.index(x) + 1}.CoinsGiven",
                                f"Top Viewer {event.top_viewers.index(x) + 1} - CoinsGiven",
                                str(x.coins_given),
                                "Top 5 Viewers")
    

## Main
def main():
    global TPClient, g_log
    ret = 0  # sys.exit() value

    # default log file destination
    logFile = f"./{PLUGIN_ID}.log"
    # default log stream destination
    logStream = sys.stdout
    
    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>",
                        help=f"Log file name (default is '{logFile}'). Use 'none' to disable file logging.")
    parser.add_argument("-s", metavar="<stream>",
                        help="Log to output stream: 'stdout' (default), 'stderr', or 'none'.")

    # this processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else 'none'
    opts.s = opts.s.strip().lower() if opts.s else 'stdout'

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q: logLevel = None
    elif opts.d: logLevel = "DEBUG"
    elif opts.w: logLevel = "WARNING"

    # set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr": logStream = sys.stderr
        elif opts.s == "stdout": logStream = sys.stdout
        else: logStream = None
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(f"Starting {TP_PLUGIN_INFO['name']} v{__version__} on {sys.platform}.")

    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

    g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret



def convert_image_to_base64(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_bytes = response.content
            base64_data = base64.b64encode(image_bytes).decode('ascii')
            return base64_data
        else:
            print(f"Failed to download image from {image_url}. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None



def run_tk():
    """
    Started when the plugin is loaded and username is present in Plugin Settings
    - Also Can be Started Manually by User
    """
    tk.thread = threading.Thread(target=tk.start_tiktok)
    if tk.isalive:
        g_log.info("TikTok thread is already running.")
    else:
        g_log.info("Starting TikTok thread.")
        tk.thread.start()



if __name__ == "__main__":
    tk = TikTok_Client()
    tk.stop_TikTok_Thread()
    sys.exit(main())








