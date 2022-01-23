import threading
import time
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GObject

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

def app_main():
	builder = Gtk.Builder()
	builder.add_from_file("screengui.glade")
	builder.connect_signals(Handler())

	window = builder.get_object("window1")
	battery = builder.get_object("levelBar1")

	def update_bar(i):
		battery.set_value(i)	
		return False

	def wiggle_bar():
		current = 0.0
		while True:
			for i in range(100):
				current += 0.01
				GLib.idle_add(update_bar, current)
				time.sleep(0.2);	
			for i in range(100):
				current -= 0.01
				GLib.idle_add(update_bar, current)
				time.sleep(0.2);	
			
	window.show_all()

	thread = threading.Thread(target=wiggle_bar)
	thread.daemon = True
	thread.start()

if __name__ == "__main__":
	app_main();
	Gtk.main()
