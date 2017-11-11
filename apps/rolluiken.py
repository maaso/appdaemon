import appdaemon.appapi as appapi
import datetime
import math

class RolluikController(appapi.AppDaemon):
  bureau_open_time = 15

  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Check if blinds need to open at sunrise
    self.run_at_sunrise(self.open_at_sunrise_cb, offset = 60*60)
    self.run_at_sunset(self.close_at_sunset_cb, offset = 30*60)

    # Listen for changes in Rolluiken swtich
    self.listen_state(self.rolluik_control_cb, "switch.rolluiken")

    # Listen for changes in individual Rolluik switches
    self.listen_state(self.rolluik_bureau_cb, "switch.rolluik_bureau")
    self.listen_state(self.rolluik_living_cb, "switch.rolluik_living")
    self.listen_state(self.rolluik_slaapkamer_cb, "switch.rolluik_slaapkamer")

    # Automatically turn off the Living blinds after a certain number of seconds
    self.listen_state(self.rolluik_living_open_cb, "switch.rolluik_living_openen")
    self.listen_state(self.rolluik_living_close_cb, "switch.rolluik_living_sluiten")

    # SLIDERS
    self.listen_state(self.slider_cb, "sensor.rolluik_bureau_command")


  def slider_cb(self, entity, attr, old, new, kwargs):
    self.log(entity)
    self.log(attr)
    self.log(old)
    self.log(new)
    current = self.get_state("sensor.rolluik_bureau_status")
    self.log(current)

    if new != current:
      # should always be true but check just in case
      # determine if we need to open or close
      move = int(new) - int(current)
      if move < 0:
        self.close(abs(move), new)
      else:
        self.open(abs(move), new)


  def close(self, toMove, resultingPercentage):
    time = math.floor((toMove / 100) * 15)
    self.run_in(self.close_finished, time, result = resultingPercentage)
    self.turn_on("switch.rolluik_bureau_sluiten")

  def close_finished(self, kwargs):
    self.turn_on("switch.rolluik_bureau_sluiten")
    self.call_service("mqtt/publish", topic = "stat/rolluiken/bureau_slider", payload = kwargs['result'], qos = 1, retain = True)


  def open(self, toMove, resultingPercentage):
    time = math.ceil((toMove / 100) * 15)
    self.run_in(self.open_finished, time, result = resultingPercentage)
    self.turn_on("switch.rolluik_bureau_openen")

  def open_finished(self, kwargs):
    self.turn_off("switch.rolluik_bureau_openen")
    self.call_service("mqtt/publish", topic = "stat/rolluiken/bureau_slider", payload = kwargs['result'], qos = 1, retain = True)


  ## MAIN LOGIC
  def rolluik_control_cb(self, entity, attribute, old, new, kwargs):
    self.rolluik_controller(new, None)

  def open_at_sunrise_cb(self, kwargs):
    # Check if we are in away mode
    # Get away mode boolean state
    state = self.get_state("switch.away_mode")
    # If on, open the blinds
    if state == "on":
      self.rolluik_controller("on", [None])

  def close_at_sunset_cb(self, kwargs):
    self.rolluik_controller("off", None)



  ## INTERNAL HANDLERS
  def rolluik_controller(self, desired, subset):
    all_blinds = ["switch.rolluiken", "switch.rolluik_bureau", "switch.rolluik_living", "switch.rolluik_slaapkamer"]
    if subset is None:
      for blind in all_blinds:
        self.action_handler(blind, desired)
    else:
      for blind in subset:
        self.action_handler(blind, desired)


  def action_handler(self, blind, desiredState):
    if desiredState == "on": 
      # Open blinds
      self.turn_on(blind)
    if desiredState == "off":
      # Close blinds
      self.turn_off(blind)



  ## SWITCH LISTENERS
  def rolluik_bureau_cb(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.turn_on("switch.rolluik_bureau_openen")
    if new == "off":
      self.turn_on("switch.rolluik_bureau_sluiten")

  def rolluik_living_cb(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.turn_on("switch.rolluik_living_openen")
    if new == "off":
      self.turn_on("switch.rolluik_living_sluiten")

  def rolluik_slaapkamer_cb(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.turn_on("switch.rolluik_slaapkamer_openen")
    if new == "off":
      self.turn_on("switch.rolluik_slaapkamer_sluiten")

  def rolluik_living_open_cb(self, entity, attr, old, new, kwargs):
    # When activated, turn it off after 22 seconds
    if new == "on":
      self.run_in(self.rolluik_living_open_auto_off_cb, 22)

  def rolluik_living_open_auto_off_cb(self, kwargs):
    self.turn_off("switch.rolluik_living_openen")

  def rolluik_living_close_cb(self, entity, attr, old, new, kwargs):
    # When activated, turn it off after 18 seconds
    if new == "on":
      self.run_in(self.rolluik_living_close_auto_off_cb, 18)

  def rolluik_living_close_auto_off_cb(self, kwargs):
    self.turn_off("switch.rolluik_living_sluiten")
