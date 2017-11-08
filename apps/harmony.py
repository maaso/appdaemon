
import appdaemon.appapi as appapi
import datetime

class HarmonyController(appapi.AppDaemon):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Listen for changes in Harmony Activity switches
    self.listen_state(self.cast_audio_cb, "switch.harmony_remote__cast_audio")
    self.listen_state(self.spotify_cb, "switch.harmony_remote__spotify")
    self.listen_state(self.tv_cb, "switch.harmony_remote__tv")


  def cast_audio_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate cast audio activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "29225980")
      self.turn_off('switch.harmony_remote__spotify')
      self.turn_off('switch.harmony_remote__tv')
    if new == "off":
      # Check current harmony state
      harmony_state = self.get_state("remote.harmony_hub", "all")
      if harmony_state["attributes"]["current_activity"] == "Cast Audio":
        # Turn off
        self.call_service("remote/turn_off", entity_id = "remote.harmony_hub")



  def spotify_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate spotify activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25430094")
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__tv')
    if new == "off":
      # Check current harmony state
      harmony_state = self.get_state("remote.harmony_hub", "all")
      if harmony_state["attributes"]["current_activity"] == "Spotify":
        # Turn off
        self.call_service("remote/turn_off", entity_id = "remote.harmony_hub")



  def tv_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate tv activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25429995")
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__spotify')
    if new == "off":
      # Check current harmony state
      harmony_state = self.get_state("remote.harmony_hub", "all")
      if harmony_state["attributes"]["current_activity"] == "TV Kijken":
        # Turn off
        self.call_service("remote/turn_off", entity_id = "remote.harmony_hub")
