import appdaemon.plugins.hass.hassapi as hass

# Will turn on configured light automatically after sundown if in Away Mode
# Will automatically turn off configured light at 00:30h
class ZigbeeSwitch(hass.Hass):
  def initialize(self):
    # set listener
    self.listen_state(self.switch_cb, self.args["switch"])


  def switch_cb(self, kwargs): 
    # toggle coupled entity
    self.toggle(self.args["target"])
