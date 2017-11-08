
import appdaemon.appapi as appapi
import datetime

class HarmonyController(appapi.AppDaemon):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Listen for changes in Harmony Activity switches
    self.listen_state(self.cast_audio_cb, "switch.harmony_remote__cast_audio")
    self.listen_state(self.spotify_cb, "switch.harmony_remote__spotify")
    self.listen_state(self.tv_cb, "switch.harmony_remote__tv")

    # Listen for changes in Harmony Remote state
    self.listen_state(self.harmony_hub_cb, "remote.harmony_hub")


  def cast_audio_cb(self, entity, attribute, old, new, kwargs):
    # Only react if new state is "on"
    if new == "on": 
      # Activate cast audio activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "29225980")

  def spotify_cb(self, entity, attribute, old, new, kwargs):
    # Only react if new state is "on"
    if new == "on": 
      # Activate spotify activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25430094")

  def tv_cb(self, entity, attribute, old, new, kwargs):
    # Only react if new state is "on"
    if new == "on": 
      # Activate tv activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25429995")

  def harmony_hub_cb(self, entity, attribute, old, new, kwargs):
    if new == "off":
      # All devices were turned off, deacitvate all switches
      switches = [ 'switch.harmony_remote__cast_audio', 'switch.harmony_remote__spotify', 'switch.harmony_remote__tv' ]
      for switch in switches:
        self.turn_off(switch)
    if new == "on":
      # New activity was started, figure out which one
      harmony_state = self.get_state("remote.harmony_hub", "all")
      if harmony_state["attributes"]["current_activity"] == "Cast Audio":
        # turn off others
        self.turn_off('switch.harmony_remote__spotify')
        self.turn_off('switch.harmony_remote__tv')
      if harmony_state["attributes"]["current_activity"] == "Spotify":
        # turn off others
        self.turn_off('switch.harmony_remote__cast_audio')
        self.turn_off('switch.harmony_remote__tv')
      if harmony_state["attributes"]["current_activity"] == "TV Kijken":
        # turn off others
        self.turn_off('switch.harmony_remote__cast_audio')
        self.turn_off('switch.harmony_remote__spotify')
