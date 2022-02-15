import threading
import time
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GObject

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

def app_main():
	#Get builder
	builder = Gtk.Builder()
	builder.add_from_file("screengui.glade")
	builder.connect_signals(Handler())

	#Get styling
	screen = Gtk.Screen()
	cssProvider = Gtk.CssProvider()
	cssProvider.load_from_path("screen.css")

	#Get objects in window
	window = builder.get_object("window1")
	battery = builder.get_object("levelBar1")

	coolTemp = builder.get_object("coolantTempDisplay")
	batTemp = builder.get_object("batTempDisplay")
	motorTemp = builder.get_object("motorTempDisplay")
	mph = builder.get_object("mphDisplay")

	lap = builder.get_object("lapDisplay")

	last_lap = time.perf_counter()
	cssFile = open("screen.css", "r")
	minutes = 0; 

	def update_bar(i): 
		battery.set_value(i) 

	def update_displays(i): 
		mph.set_text(str(i)) 
		coolTemp.set_text(str(i)) 
		batTemp.set_text(str(i)) 
		motorTemp.set_text(str(i)) 

	def format_seconds(f, n):
		return int((f%60)*pow(10, n))/pow(10,n)
		

	def update_lap(time_lapsed):
		minutes = int(time_lapsed // 60)	
		seconds = format_seconds(time_lapsed, 5)
		lap.set_text("{}:{}".format(minutes, seconds))


	def lap_timer():
		while True:	
			GLib.idle_add(update_lap, time.perf_counter() - last_lap)
			time.sleep(0.1)

			

	def wiggle():
		current = 0.0
		displays = 0	
		while True:	
			for i in range(100):
				current += 0.01
				displays += 1
				GLib.idle_add(update_bar, current)
				GLib.idle_add(update_displays, displays)
				time.sleep(0.1);	
			for i in range(100):
				current -= 0.01
				displays -= 1
				GLib.idle_add(update_bar, current)
				GLib.idle_add(update_displays, displays)
				time.sleep(0.1);	
	
	window.add_provider(cssProvider, 0);
	window.show_all()
	window.fullscreen()

	wiggle_thread = threading.Thread(target=wiggle)	
	wiggle_thread.daemon = True
	wiggle_thread.start()

	lap_thread = threading.Thread(target=lap_timer)
	lap_thread.daemon = True
	lap_thread.start()

if __name__ == "__main__":
	app_main();
	Gtk.main()
