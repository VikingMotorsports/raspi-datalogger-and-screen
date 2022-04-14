import threading
import time
import gi
#import temptest
#import acceltest

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GObject, Gdk

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

def app_main():
	#Get builder
	builder = Gtk.Builder()
	builder.add_from_file("screengui.glade")
	builder.connect_signals(Handler())

	#Get styling
	cssProvider = Gtk.CssProvider()
	cssProvider.load_from_path("screen.css")
	context = Gtk.StyleContext()
	screen = Gdk.Screen.get_default()
	context.add_provider_for_screen(screen,cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	#Get objects in window
	window = builder.get_object("window1")
	battery = builder.get_object("levelBar1")

	coolTempDisplay = builder.get_object("coolantTempDisplay")
	batTempDisplay = builder.get_object("batTempDisplay")
	motorTempDisplay = builder.get_object("motorTempDisplay")
	mphDisplay = builder.get_object("mphDisplay")

	coolFrame = builder.get_object("coolTempFrame")
	batFrame = builder.get_object("batTempFrame")
	motorFrame = builder.get_object("motorTempFrame")
	
	rat = builder.get_object("rat")

	cfStyleContext = coolFrame.get_style_context()
	bfStyleContext = batFrame.get_style_context()
	mfStyleContext = motorFrame.get_style_context()
	ratContext = rat.get_style_context()

	lapDisplay = builder.get_object("lapDisplay")

	last_lap = time.perf_counter()
	cssFile = open("screen.css", "r")
	minutes = 0; 
	coolTemp = 0;

	def update_bar(i): 
		battery.set_value(i) 

	def update_displays(): 
		mphDisplay.set_text(str(acceltest.getAccel()))
		coolTemp = temptest.getTemp()	
		coolTempDisplay.set_text("{} C".format(coolTemp))
		update_background_color(cfStyleContext, coolTemp)
		

	def format_seconds(f, n):
		return int((f%60)*pow(10, n))/pow(10,n)
		


	def update_lap(time_lapsed):
		minutes = int(time_lapsed // 60)	
		seconds = format_seconds(time_lapsed, 5)
		lapDisplay.set_text("{}:{}".format(minutes, seconds))


	def lap_timer():
		while True:	
			GLib.idle_add(update_lap, time.perf_counter() - last_lap)
			time.sleep(0.1)

	def update_text_color(styleContext, value):
		if value < 33:
			styleContext.remove_class("red")
			styleContext.remove_class("yellow")
			styleContext.add_class("green")	
		elif value < 66:
			styleContext.remove_class("green")
			styleContext.remove_class("red")
			styleContext.add_class("yellow")
		else:
			styleContext.remove_class("yellow")
			styleContext.remove_class("green")
			styleContext.add_class("red")

	def update_background_color(styleContext, value):
		if value < 33:
			styleContext.remove_class("back-red")
			styleContext.remove_class("back-yellow")
			styleContext.add_class("back-green")	
		elif value < 66:
			styleContext.remove_class("back-green")
			styleContext.remove_class("back-red")
			styleContext.add_class("back-yellow")
		else:
			styleContext.remove_class("back-yellow")
			styleContext.remove_class("back-green")
			styleContext.add_class("back-red")

	def update(percent, integer):
		update_bar(percent)
		update_displays(integer)
		update_color(cfStyleContext, integer)
		update_color(bfStyleContext, integer)
		update_color(mfStyleContext, integer)
		update_color(ratContext, integer)

		#update_background_color(cfStyleContext, integer)

	def update(percent, integer):
		update_bar(percent)
		update_displays(integer)
		update_text_color(ratContext, integer)
		update_background_color(cfStyleContext, integer)
		update_background_color(bfStyleContext, integer)
		update_background_color(mfStyleContext, integer)

	def wiggle():
		current = 0.0
		displays = 0	
		while True:	
			for i in range(100):
				current += 0.01
				displays += 1	
				GLib.idle_add(update, current, displays)
				time.sleep(0.1)
			for i in range(100):
				current -= 0.01
				displays -= 1
				GLib.idle_add(update, current, displays)
				time.sleep(0.1)

	def update_loop():
		while True:
			GLib.idle_add(update_displays)
			time.sleep(0.1)
			
	
	window.show_all()
	window.fullscreen()

#	sensor_thread = threading.Thread(target=update_loop)	
#	sensor_thread.daemon = True
#	sensor_thread.start()

#	wiggle_thread = threading.Thread(target=wiggle)	
#	wiggle_thread.daemon = True
#	wiggle_thread.start()

#	lap_thread = threading.Thread(target=lap_timer)
#	lap_thread.daemon = True
#	lap_thread.start()

if __name__ == "__main__":
	app_main();
	Gtk.main()
