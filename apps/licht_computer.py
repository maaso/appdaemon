import appdaemon.plugins.hass.hassapi as hass

class LichtComputerController(hass.Hass):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Check if we need to activate/deactivate the computer light when computer is turned off
    # Listen for changes in Computer switch
    self.listen_state(self.computer_light_check_cb, "switch.computer")

  def computer_light_check_cb(self, entity, attribute, old, new, kwargs):
    if new == "on":
      # Check state of the Rolluik Bureau input boolean
      blind_state = self.get_state("input_boolean.rolluik_bureau")
      if blind_state == "off":
        self.turn_on("light.licht_computer")
    if new == "off":
      # Check if the light is currently on, if it is, turn it off
      light_state = self.get_state("light.licht_computer")
      if light_state == "on":
        self.turn_off("light.licht_computer")
