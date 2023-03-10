import sublime
import sublime_plugin
import re

def RegexFunction(txt):
	out = []
	i = 0
	while i < len(txt):
		start = 0
		temp = 0
		parentheses = 0
		while i < len(txt) and not txt[i].isalnum() and not txt[i] == '_':
			i += 1
		start = i
		while i < len(txt) and (txt[i].isalnum() or txt[i] == '_'):
			i += 1
		if i < len(txt) and txt[i] == '(':
			parentheses = 1
			i += 1
			temp = i
			while i < len(txt) and parentheses > 0 and txt[i] != ';':
				if txt[i] == '(':
					parentheses += 1
				if txt[i] == ')':
					parentheses -= 1
				i += 1
			if i < len(txt) and parentheses == 0:
				out.append((start, i, txt[start:i]))
			i = temp
	return out

class FunctionLinesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		txt = self.view.substr(sublime.Region(0, self.view.size()))
		lines = txt.splitlines()

		a = 0
		while a <= len(lines):
			self.view.erase_phantoms("42_function_lines_total")
			a += 1

		all_res_regex = RegexFunction(txt)
		for res_regex in all_res_regex:
			if txt[res_regex[1]] == '\n' and txt[res_regex[1] + 1] == '{':
				i = res_regex[1] + 2
				brackets = 1
				while brackets != 0 and i < len(txt):
					if txt[i] == '{':
						brackets += 1
					elif txt[i] == '}':
						brackets -= 1
					i += 1
				size = 0
				start = res_regex[1] + 3
				end = i - 1
				while start < end:
					if txt[start] == '\n':
						size += 1
					start += 1
				if size > 25:
					html = '<body style="color:#bf2525;font-style:italic;margin-left:10px;">Function lines: ' + str(size) + '</body>'
				else:
					html = '<body style="color:#8d9090;font-style:italic;margin-left:10px;">Function lines: ' + str(size) + '</body>'
				self.view.add_phantom("42_function_lines_total", sublime.Region(i - 1, self.view.size()), html, sublime.LAYOUT_BLOCK)
