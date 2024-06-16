from obswebsocket import obsws, requests
import time

class ObsWebSocket:
    def __init__(self, address, port, password):
        self.address = address
        self.port = port
        self.password = password
        self.obs_client = None

    def obs_login(self):
        self.obs_client = obsws(self.address, self.port, self.password)
        try:
            self.obs_client.connect()
        except Exception as e:
            # Optionally log the error to a file or logging system
            print(f"Error connecting to OBS: {e}")

    def obs_logout(self):
        if self.obs_client:
            try:
                self.obs_client.disconnect()
                # print("Disconnected from OBS WebSocket")
            except Exception as e:
                print(f"Error disconnecting from OBS: {e}")
        else:
            print("Not connected to OBS WebSocket")

    def check_connection_status(self):
        if self.obs_client:
            print("Connected to OBS WebSocket")
        else:
            print("Not connected to OBS WebSocket")

    def setEmpty(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.EMPTY"))
    def setNeedOne(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.NEEDONE"))  
    def setPreGame(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.PREGAME"))            
    def setWarmUp(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.WARMUP"))    
    def setInGame(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.INGAME"))    
    def setTumer(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.TUMER"))    
    def setMisc(self):
        self.obs_client.call(requests.SetCurrentProgramScene(sceneName="QFNTV.MISC"))            
            