
import appdaemon.appapi as appapi
import datetime

class SpeakerController(appapi.AppDaemon):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Listen for changes to Bureau media player
    self.listen_state(self.speakers_boven_cb, "media_player.bureau_cca")
    # Listen for changes to Living media player
    self.listen_state(self.speakers_living_cb, "media_player.living")


  def speakers_boven_cb(self, entity, attribute, old, new, kwargs):
    if new == "playing" and self.get_state("switch.speakers_boven") == "off": 
      # Activate upstairs speakers
      self.turn_on("switch.speakers_boven")
    if new == "off":
      # Deactivate upstairs speakers
      self.turn_off("switch.speakers_boven")


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



