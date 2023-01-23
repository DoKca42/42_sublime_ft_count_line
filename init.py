import sublime
import sublime_plugin
import re
import os

class EventDump(sublime_plugin.EventListener):
	def on_modified(self, view):
		view = sublime.active_window().active_view()
		file_name = view.file_name()

		file_extension = os.path.splitext(file_name)
		file_type = file_extension[1:]
		if str(file_type[0]) == ".c":
			view.run_command("function_lines")