
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



  ### Main activity handler
  def activity_handler(self, entity, attribute, old, new, kwargs):
    self.log(new)


  def cast_audio_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate cast audio activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "29225980")
      self.turn_off('switch.harmony_remote__spotify')
      self.turn_off('switch.harmony_remote__tv')
    if new == "off":
      # give Harmony activity some time to update
      self.run_in(self.power_off_check, 15, activityName = 'Cast Audio')



  def spotify_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate spotify activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25430094")
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__tv')
    if new == "off":
      # give Harmony activity some time to update
      self.run_in(self.power_off_check, 15, activityName = 'Spotify')



  def tv_cb(self, entity, attribute, old, new, kwargs):
    # Immediately react if new state is "on"
    if new == "on": 
      # Activate tv activity
      self.call_service("remote/turn_on", entity_id = "remote.harmony_hub", activity = "25429995")
      self.turn_off('switch.harmony_remote__cast_audio')
      self.turn_off('switch.harmony_remote__spotify')
    if new == "off":
      # give Harmony activity some time to update
      self.run_in(self.power_off_check, 15, activityName = 'TV Kijken')


  def power_off_check(self, kwargs):
    # Check current harmony state
    harmony_activity = self.get_state(entity="remote.harmony_hub", attribute="current_activity")
    if harmony_activity == kwargs['activityName']:
      # Turn off
      self.call_service("remote/turn_off", entity_id = "remote.harmony_hub")
