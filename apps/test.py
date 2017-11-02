import appdaemon.appapi as appapi
import datetime

class LightTest(appapi.AppDaemon):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Create a time object for 7pm
    on_time = datetime.time(18, 41, 30)
    off_time = datetime.time(18, 41, 40)
    # Schedule a daily callback that will call run_daily() at 7pm every night
    self.run_daily(self.on_cb, on_time)
    self.run_daily(self.off_cb, off_time)

   # Our callback function will be called by the scheduler every day at 7pm
  def on_cb(self, kwargs):
    # Call to Home Assistant to turn the porch light on
    self.turn_on("light.licht_computer")

  def off_cb(self, kwargs):
    self.turn_off("light.licht_computer")

  # test commit for integration