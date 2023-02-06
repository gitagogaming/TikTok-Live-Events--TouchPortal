    
    
import asyncio
from typing import Optional, List, Callable, Dict
from TikTokLive import TikTokLiveClient
from TikTokLive.types import FailedConnection
from TikTokLive.types.events import CommentEvent, ConnectEvent, FollowEvent, ShareEvent, LikeEvent, JoinEvent, GiftEvent, ViewerCountUpdateEvent


import sys
import time


from entry import PLUGIN_ID, TP_PLUGIN_SETTINGS, TP_PLUGIN_ACTIONS, TP_PLUGIN_INFO, __version__, TP_PLUGIN_CONNECTORS
from TouchPortalAPI.logger import Logger
from argparse import ArgumentParser
import TouchPortalAPI as TP



### Need to figure out how to start TP Plugin and then connect to tiktok plugin AFTER using the username specified....

loop = asyncio.new_event_loop()

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





## def the_async_loop():
##     global loop
##     try:
##         asyncio.set_event_loop(loop)
##         loop.run_until_complete(tk.start_bot())
##     except Exception as e:
##         g_log.error(e)
##     finally:
##        pass


g_log = Logger(name = PLUGIN_ID)






def handleSettings(settings, on_connect=False):
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    
    tk.Username = settings['TikTok Username']
    if tk.Username != "":
       #startup = True
       #tk.run_the_thing(tk.Username)
       #run_tiktok_thread()
        print("Username: " + tk.Username)
    
   #if not on_connect:
   #    if (value := settings.get(TP_PLUGIN_SETTINGS['TikTok Username']['name'])) is not None:
   #        # this example doesn't do anything useful with the setting, just saves it
   #        TP_PLUGIN_SETTINGS['TikTok Username']['value'] = value
   #        
   #        print("ZOMG KEWL")
   #        
   #        print(TP_PLUGIN_SETTINGS['TikTok Username']['value'])


#--- On Startup ---#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)
        
    



#--- Settings handler ---#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)



@TPClient.on(TP.TYPES.onListChange)
def listChangeAction(data):
    print(data)




#--- Action handler ---#
@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    print(data)
    global startup
    g_log.debug(f"Action: {data}")
        ### Turning on/off lights
    if data['actionId'] == PLUGIN_ID + ".act.Connect":
        ## Checking to see if custom light wanted
        if data['data'][0]['value'] == "Disconnect":
            tk.tiktok.remove_all_listeners()
            tk.tiktok.stop()
            startup = False

            time.sleep(2)
            g_log.info("THE TIKTOK LIVE CHAT HS BEEN STOPPED")
       #     print("STOP STOP STOP STOP STOP IT NOW!!")
       
        if data['data'][0]['value'] == "Connect":

            startup = True
            tk.run_the_thing(tk.Username)
            run_tiktok_thread()



# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')
    # We do not need to disconnect manually because we used `autoClose = True`









from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, JoinEvent, LikeEvent, ShareEvent

import threading

class TikTok_Client:
    # Trying to put into its own class where auto connect crap class TikTok():
    def __init__(self,) -> None:
        self.tiktok: TikTokLiveClient = None
        self.isalive = False
        self.Username = None
        self.thread = None
        #self.thread.start()
      #  self.run_the_thing(tiktok_channel)


    def run_the_thing(self, tiktok_channel):
        
        
        self.tiktok = TikTokLiveClient(tiktok_channel, **{
            "process_initial_data": False  # Spams cached messages on start, must be disabled
        })
        
        g_log.info("Adding Listeners")
        #print("Adding Listeners")
        
        self.tiktok.add_listener("comment", on_comment)
        self.tiktok.add_listener("follow", on_follow)
        self.tiktok.add_listener("like", on_like)
        self.tiktok.add_listener("share", on_share)
        self.tiktok.add_listener("join", on_join)
        self.tiktok.add_listener("gift", on_gift)
        self.tiktok.add_listener("viewer_count_update", on_viewercountUpdate)
        self.tiktok.add_listener("connect", on_connect)
        self.tiktok.add_listener("disconnect", on_disconnect)
        
        
        g_log.info("Starting TikTok Live Chat")
        
        return self.tiktok



def on_disconnect(event: ConnectEvent):
    g_log.info("Disconnected from TikTok Live Chat")
    #print("Disconnected from TikTok Live Chat")
    
    
## Instantiate the client with the user's username
#client: TikTokLiveClient = TikTokLiveClient(unique_id="@amarifieldsofficial")
tk = TikTok_Client()





startup = False ## default runs as true, if user wants to disconnect they can and we set it to false. 

def start_tiktok():
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    attempt = None
    
    while not attempt:
        if startup:
            try:
                attempt = tk.tiktok.run()
               # attempt = await tk.tiktok.start()
               
            except FailedConnection:
                print("Failed to connect to TikTok. Restarting...")
            time.sleep(5)
        if not startup:
            print("... lets try again")
            time.sleep(5)
            start_tiktok()
         #   break



 # async def start_bot(self) -> bool:
 #     # Start TikTok
 #     try:
 #         await self.tiktok.start()
 #     except FailedConnection:
 #         print(f"TikTok Channel @{self._tiktok_channel} is offline. Bot will cycle restarts every {self.cycle_check} seconds until it is available.")
 #         self.tiktok = TikTokLiveClient(self._tiktok_channel)
 #         time.sleep(0.5)

 #     return True




from collections import deque
last_5_messages = deque(maxlen=5)

def update_message_states():
    for index, message in enumerate(last_5_messages):
        TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.Username", f"Message_{index + 1} - Username", str(message['nickname']))
        TPClient.createState(PLUGIN_ID + f".act.message_{index + 1}.Message", f"Message_{index + 1} - Message", str(message['comment']))





# Define how you want to handle specific events via decorator
async def on_connect(event: ConnectEvent):
    print("Connected to Room ID:", tk.tiktok.room_id)
    print("The Room Info", tk.tiktok.retrieve_room_info())



async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")
    #g_log.info(f"{event.user.nickname} -> {event.comment}")
    ## keeping only the last 5 messages in a variable at any given time.. 
    ## When message 0 comes in, wait for message 1 to come in, then delete message 0 and move message 1 to message 0, then wait for message 2 to come in, then delete message 1 and move message 2 to message 1, etc.
    last_5_messages.append({'nickname': event.user.nickname, 'comment':event.comment})
    update_message_states()
    



async def on_follow(event: FollowEvent):
    message: str = f"{event.user.uniqueId} followed!{event.user.uniqueId}"
    g_log.info(message)
    
   # print("FOLLOWWWWWEEEED   " *20)
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newFollower", "True")
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Follow.UserID", str(event.user.uniqueId))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Follow.Name", str(event.user.nickname))

    TPClient.stateUpdate(PLUGIN_ID + ".state.newFollower", "False")


async def on_like(event: LikeEvent):
    message: str = f"{event.user.uniqueId} liked the stream {event.likeCount} times, there is now {event.totalLikeCount} total likes!"
    g_log.info(message)
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newLike", "True")
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.like_count", str(event.totalLikeCount))
   # print(PLUGIN_ID + ".state.like_count", str(event.totalLikeCount))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Like.UserID", str(event.user.uniqueId))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Like.Name", str(event.user.nickname))
    ## add one for the total likes by the user..
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Like.Name.TimesLiked", str(event.likeCount))
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newLike", "False")


async def on_share(event: ShareEvent):
    message: str = f"{event.user.uniqueId} shared the streamer!"
    g_log.info(message)
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newShare", "True")
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Share.UserID", str(event.user.uniqueId))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Share.Name", str(event.user.nickname))
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newShare", "False")


async def on_join(event: JoinEvent):
  #  print(f"{event.user.uniqueId} joined!")
  #  g_log.info(f"{event.user.uniqueId} joined!")
    TPClient.stateUpdate(PLUGIN_ID + ".state.newJoin", "True")
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Join.UserID", str(event.user.uniqueId))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Join.Name", str(event.user.nickname))
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newJoin", "False")


#@tk.tiktok.on('gift')
async def on_gift(event: GiftEvent):
    # If it's type 1 and the streak is over
    ### there is a way to get cliet gift image and url etc?  
    ### https://www.youtube.com/watch?v=gubvklbZFTU 
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")
        
        
    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        message: str = f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\""
        g_log.info(message)
        ## and gift amount
        TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Gift.GiftName", str(event.gift.extended_gift.name))
        
        
    TPClient.stateUpdate(PLUGIN_ID + ".state.newGift", "True")
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Gift.UserID", str(event.user.uniqueId))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Gift.Name", str(event.user.nickname))
    TPClient.stateUpdate(PLUGIN_ID + ".state.Recent.Gift.GiftID", str(event.gift.giftId))
    
    TPClient.stateUpdate(PLUGIN_ID + ".state.newGift", "False")




async def on_viewercountUpdate(event: ViewerCountUpdateEvent):
    g_log.info(f"Received a new viewer count: {event.viewerCount}")
    TPClient.stateUpdate(PLUGIN_ID + ".state.viewer_count", str(event.viewerCount))
  #  print("viewer count", str(event.viewerCount))
  #  print(PLUGIN_ID + ".state.viewer_count")
































## main
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

    # his processes the actual command line and populates the `opts` dict.
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



def run_tiktok_thread():
    tk.thread = threading.Thread(target=start_tiktok)
    if tk.isalive:
        g_log.info("TikTok thread is already running.")
    else:
        g_log.info("Starting TikTok thread.")
        tk.thread.start()

if __name__ == "__main__":
 #   run_tiktok_thread()
    sys.exit(main())


# if __name__ == '__main__':
#     # Run the client and block the main thread
#     # await client.start() to run non-blocking
#     start_tiktok()
#     # tk.start_bot()







##  send msg from TikTokLive import TikTokLiveClient
##  send msg from TikTokLive.types.events import CommentEvent
##  send msg 
##  send msg client = TikTokLiveClient("@blainzz")
##  send msg 
##  send msg 
##  send msg 
##  send msg # created a signed url for http request to send a live message to tiktok
##  send msg 
##  send msg async def sign_url(raw_url: str, session_id: str):
##  send msg     """
##  send msg     
##  send msg     You will need to create your OWN function to modify the HTTP request to your liking so that it passes TikTok Auth.
##  send msg     TikTokLive cannot and will not provide signatures, but if you want this functionality, it's here.
##  send msg     
##  send msg     :param raw_url: The URL that requires signing
##  send msg     :param session_id: The sessionid sending the message
##  send msg     :return: None
##  send msg     
##  send msg     """
##  send msg     # generate a signed url
##  send msg     signed_url: str = raw_url + (
##  send msg         f"&msToken={'MUST_GENERATE_ME'}"
##  send msg         f"&X-Bogus={'MUST_GENERATE_ME'}"
##  send msg         f"&User-Agent={'MUST_GENERATE_ME'}"
##  send msg         f"&browserVersion={'MUST_GENERATE_ME'}"
##  send msg         f"&browserName={'MUST_GENERATE_ME'}"
##  send msg         f"&_signature={'MUST_GENERATE_ME'}"
##  send msg     )
##  send msg 
##  send msg     # You will need to supply your own headers
##  send msg     headers: dict = {
##  send msg         "Cookie": "ttwid=MUST_GENERATE_TTWID;",
##  send msg         **client._http.headers
##  send msg     }
##  send msg 
##  send msg     return signed_url, headers
##  send msg 
##  send msg 
##  send msg @client.on("message")
##  send msg async def on_ping(event: CommentEvent):
##  send msg     """
##  send msg     When someone runs the /ping command, choose how to react
##  send msg     :param event: Comment event
##  send msg     :return: None
##  send msg     """
##  send msg 
##  send msg     # If not ping, return
##  send msg     if event.comment.lower() != "/ping":
##  send msg         return
##  send msg 
##  send msg         # Reply with Pong
##  send msg     reply: str = f"{event.user.uniqueId} Pong!"
##  send msg     print(f"The bot will respond in chat with \"{reply}\"")
##  send msg 
##  send msg     await client.send_message(
##  send msg         text=reply,
##  send msg         sign_url_fn=sign_url,
##  send msg         session_id="SESSION_ID_HERE"
##  send msg     )
##  send msg 
##  send msg 
##  send msg if __name__ == '__main__':
##  send msg     """
##  send msg     An example showing you how you can send comments to your live
##  send msg     
##  send msg     """
##  send msg 
##  send msg     client.run()