import sublime
import sublime_plugin
import re
import os
import time

class EventDump(sublime_plugin.EventListener):
	last_modified = 0

	def on_modified(self, view):
		current_time = time.time()
		if current_time - self.last_modified >= 0.2:
			self.last_modified = current_time

			view = sublime.active_window().active_view()
			file_name = view.file_name()

			if file_name != None:
				file_extension = os.path.splitext(file_name)
				file_type = file_extension[1:]
				if str(file_type[0]) == ".c":
					view.run_command("function_lines")