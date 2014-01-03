import sublime, sublime_plugin
import time

SETTINGS_FILE = 'TimeEntry.sublime-settings'

class TimeEntryCommand(sublime_plugin.ApplicationCommand):
    def run(self, pretext = ''):
        window = sublime.active_window()
        if window:
            window.show_input_panel("Log time:", pretext, self.save, None, None)
        else:
            sublime.error_message("Could not prompt for hostname because no window found.")

    def save(self, entry):
        global SETTINGS_FILE
        current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
        sublime.status_message(''.join(["Saved '", entry, "' at ", current_time]))
        settings = sublime.load_settings(SETTINGS_FILE)
        settings.set(current_time, entry)
        sublime.save_settings(SETTINGS_FILE)

class AskToStoreSavedFile(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        pretext = ''.join(["Saved file ", view.file_name()])
        sublime.run_command("time_entry", {"pretext": pretext})