import appdaemon.appapi as appapi
import datetime

# Will turn on configured light automatically after sundown if in Away Mode
# Will automatically turn off configured light at 00:30h
class AutoLights(appapi.AppDaemon):
  def initialize(self):
    # Turn on at sunset
    self.run_at_sunset(self.auto_light_on_cb)
    # Turn off at 00:30h
    time = datetime.time(00, 30, 0)
    self.run_daily(self.auto_light_off_cb, time)


  def auto_light_on_cb(self, kwargs):
    # Get Away Mode state
    away = self.get_state("switch.away_mode")
    if away == "on":
      self.turn_on(self.args["light"])

  def auto_light_off_cb(self, kwargs):
    self.turn_off(self.args["light"])
