import sublime
import sublime_plugin
import re

class FunctionLinesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = sublime.active_window().active_view()
		raw_lst = self.view.substr(sublime.Region(0, self.view.size()))
		lines = raw_lst.splitlines()

		a = 0
		while a <= len(lines):
			view.erase_phantoms("ee")
			a += 1
		i = 0
		while i < len(lines):
			line = lines[i]
			res = re.search(r"[a-zA-Z_][a-zA-Z_0-9]*\(.*\)", line)
			if res:
				if res.end() == len(line):
					i += 1
					line = lines[i]
					if line == "{":
						bracket = 1
						size = 0
						i += 1
						while bracket != 0 and i < len(lines):
							line = lines[i]
							bracket += line.count("{")
							bracket -= line.count("}")
							size += 1
							i += 1
						if size - 1 > 25:
							html = '<body style="color:#bf2525;font-style:italic;margin-left:10px;">Function lines: ' + str(size - 1) + '</body>'
						else:
							html = '<body style="color:#8d9090;font-style:italic;margin-left:10px;">Function lines: ' + str(size - 1) + '</body>'
						a = 0
						chara = 0
						while a < i:
							line = lines[a]
							chara += len(line) + 1
							a += 1
						view.add_phantom("ee", sublime.Region(chara - 1, self.view.size()), html, sublime.LAYOUT_BLOCK)
			i += 1
