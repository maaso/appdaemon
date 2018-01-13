
import appdaemon.plugins.hass.hassapi as hass
import datetime

class HarmonyController(hass.Hass):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Listen for changes in Harmony Activity switches
    self.listen_state(self.cast_audio_cb, "switch.harmony_remote__cast_audio")
    self.listen_state(self.spotify_cb, "switch.harmony_remote__spotify")
    self.listen_state(self.tv_cb, "switch.harmony_remote__tv")
    # Listen for changes in Harmony Activity Input Select
    self.listen_state(self.activity_handler, "input_select.harmony_activity")
    # Listen for changes to Harmony state to update buttons if triggered externally
    # Only fire if state remains the same for at least 60 seconds
    self.listen_state(self.harmony_cb, "remote.harmony_hub", attribute = "current_activity", new = "Cast Audio", duration = 60)
    self.listen_state(self.harmony_cb, "remote.harmony_hub", attribute = "current_activity", new = "Spotify", duration = 60)
    self.listen_state(self.harmony_cb, "remote.harmony_hub", attribute = "current_activity", new = "Tv Kijken", duration = 60)
    self.listen_state(self.harmony_cb, "remote.harmony_hub", attribute = "current_activity", new = "Power Off", duration = 60)



  ### Main activity handler
  def activity_handler(self, entity, attribute, old, new, kwargs):
    activityDictionary = { "Tv Kijken": 25429995, "Spotify": 25430094, "Cast Audio": 29225980 }
    if new == "Power Off":
      self.call_service("remote/turn_off", entity_id = "remote.harmony_hub")
    else:
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = activityDictionary[new])


  ### Harmony state handler
  def harmony_cb(self, entity, attribute, old, new, kwargs):
    self.log(attribute)
    self.log(new)
    if new == "Power Off":
      # Make sure all buttons are off
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__spotify')
      self.turn_off('switch.harmony_remote__tv')
    if new == "Cast Audio":
      self.turn_on('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__spotify')
      self.turn_off('switch.harmony_remote__tv')
    if new == "Spotify":
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_on('switch.harmony_remote__spotify')
      self.turn_off('switch.harmony_remote__tv')
    if new == "Tv Kijken":
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__spotify')
      self.turn_on('switch.harmony_remote__tv')


  ### Button handlers
  def cast_audio_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate cast audio activity
      self.select_option("input_select.harmony_activity", "Cast Audio")
      self.turn_off('switch.harmony_remote__spotify')
      self.turn_off('switch.harmony_remote__tv')
    if new == "off" and self.get_state("input_select.harmony_activity") == "Cast Audio":
      self.select_option("input_select.harmony_activity", "Power Off")

  def spotify_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate spotify activity
      self.select_option("input_select.harmony_activity", "Spotify")
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__tv')
    if new == "off" and self.get_state("input_select.harmony_activity") == "Spotify":
      self.select_option("input_select.harmony_activity", "Power Off")

  def tv_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate tv activity
      self.select_option("input_select.harmony_activity", "Tv Kijken")
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__spotify')
    if new == "off" and self.get_state("input_select.harmony_activity") == "Tv Kijken":
      self.select_option("input_select.harmony_activity", "Power Off")

