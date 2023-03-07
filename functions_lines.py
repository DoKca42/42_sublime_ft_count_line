import sublime
import sublime_plugin
import re

class FunctionLinesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		txt = self.view.substr(sublime.Region(0, self.view.size()))
		lines = txt.splitlines()

		a = 0
		while a <= len(lines):
			self.view.erase_phantoms("42_function_lines_total")
			a += 1
		all_res_regex = re.finditer(r"[a-zA-Z_][a-zA-Z_0-9]*\((?:[^()]|\((?:[^()]|\((?:[^()]+|\([^()]*\))*\))*\))*\)", txt)
		for res_regex in all_res_regex:
			if txt[res_regex.end()] == '\n' and txt[res_regex.end() + 1] == '{':
				i = res_regex.end() + 2
				brackets = 1
				while brackets != 0 and i < len(txt):
					if txt[i] == '{':
						brackets += 1
					elif txt[i] == '}':
						brackets -= 1
					i += 1
				size = 0
				start = res_regex.end() + 3
				end = i - 1
				while start < end:
					if txt[start] == '\n':
						size += 1
					start += 1
				if size > 25:
					html = '<body style="color:#bf2525;font-style:italic;margin-left:10px;">Function lines: ' + str(size) + '</body>'
				else:
					html = '<body style="color:#8d9090;font-style:italic;margin-left:10px;">Function lines: ' + str(size) + '</body>'
				self.view.add_phantom("42_function_lines_total",sublime.Region(i - 1, self.view.size()), html, sublime.LAYOUT_BLOCK)