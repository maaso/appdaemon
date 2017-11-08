
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


  def speakers_living_cb(self, entity, attribute, old, new, kwargs):
    # Get full state of the Harmony Remote component
    harmony_state = self.get_state("remote.harmony_hub", "all")

    if new == "playing" and harmony_state["attributes"]["current_activity"] == "PowerOff":
      # Activate downstairs speakers
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25430094")

    # If state changes to idle, see if we are still idle in 5 minutes and turn off
    if new == "idle" and harmony_state["attributes"]["current_activity"] == "Spotify":
      self.run_in(self.paused_auto_off_cb, 300)



  def paused_auto_off_cb(self, kwargs):
    # Get full state of the Spotify component
    player_state = self.get_state("media_player.living", "all")
    # Get full state of the Harmony Remote component
    harmony_state = self.get_state("remote.harmony_hub", "all")
    # Check if still paused and turn off if this is the case
    if player_state["state"] == "idle" and harmony_state["attributes"]["current_activity"] == "Spotify":
      self.call_service("remote/turn_off", entity_id = "remote.harmony_hub")