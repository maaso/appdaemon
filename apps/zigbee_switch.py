import appdaemon.plugins.hass.hassapi as hass

# Will toggle the specified target each time the switch changes state
class ZigbeeSwitch(hass.Hass):
  def initialize(self):
    # set listener
    self.listen_state(self.switch_cb, self.args["switch"])


  def switch_cb(self, entity, attribute, old, new, kwargs):
    # toggle coupled entity
    self.toggle(self.args["target"])
