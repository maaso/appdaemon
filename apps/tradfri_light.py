import appdaemon.plugins.hass.hassapi as hass

# IKEA Tradfri controller
class TradfriLight(hass.Hass):
  def initialize(self):
    # Listen to changes in a switch
    self.listen_state(self.switch_change_cb, self.args["switch"])

  def switch_change_cb(self, entity, attribute, old, new, kwargs):
    # toggle coupled entity
    self.log(new)
    if new == "on":
      self.call_service("zigate/raw_command", cmd = "0092", data = "02" + self.args["target"] + "010101")
    if new == "off":
      self.call_service("zigate/raw_command", cmd = "0092", data = "02" + self.args["target"] + "010100")
