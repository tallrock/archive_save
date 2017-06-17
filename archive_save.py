"""
James De Rocher - May 2017 - jdd@tallrock.com

[This is a plug-in I wrote for myself. It works for me - running Sublime Text 3
under Windows 10. As of the date of this comment, I haven't ported this plug-in
over to my Linux machine yet. So I don't know if it will work there.]

This sublime text 3 plug-in makes a backup copy of every file you save,
everytime you save.

When I am slashing-and-burning through program code, I sometimes realize I need
to go back to before some previous code; perhaps to reset the whole program or to
grab a previous iteration of some code I just mangled. GIT is wonderful for saving
checkpoints but a bit heavy for what can be dozens (or many dozens) of file saves
done in a day. And at the end of the day, or week, all these intermediate saves
can be easily deleted (or archived for posterity). This plug-in just lets the
archive files pile up. You determine what to do with them.

I have set this plug-in up to run when I hit CTRL+ALT+S versus the usual CTRL+S.
I leave CTRL+S mapped to the regular save so I have the option of which kind of
save to do.

This plug-in reads a sublime settings file ("archive_save.sublime-settings") and
a setting ("archive_directory") to determine where to save the second "archive" copy
of your files. If the setting or settings file are not present, the program defaults
to saving the "archive" copies to the subdirectory "./archive_saved_files".

THE ARCHIVE FILENAME

I save the archive file with two changes in order to guarantee uniqueness:
(1) I slugify the filename (no spaces,slashes,colons)
(2) I prefix the filename with a time-stamped-to-the-millisecond code.

So a file like 'c:\goals\march list.txt' becomes 'j3jryh4g.c.goals.march.list.txt'


"""

import sublime
import sublime_plugin
import time
import os
import shutil

class ArchiveSaveCommand(sublime_plugin.TextCommand):

    settings_filename = 'archive_save.sublime-settings'
    settings = None

    def timecode(self):
        """ Return an alphanum_code for the current unix time plus milliseconds """
        unixtime = time.time()
        milltime = int(unixtime*1000)
        return( self.alphanum_encode(milltime) )

    def alphanum_encode(self,number, alphabet='0123456789abcdefghijklomnoprstuvwxyz'):
        """ Encode an integer into an alphanum_code """
        base36 = ''
        sign = ''
        if 0 <= number < len(alphabet):
            return sign + alphabet[number]
        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
        return sign + base36

    def slugname(self,filename):
        """ Create a slugname for the given filename """
        if filename is None:
            return 'unknown'
        return filename.replace('\\','.').replace('/','.').replace(' ','.').replace(':','')

    def get_archive_directory(self):
        """ Check for archive_directory settings file and parameter """
        default_new_directory = '\\archive_saved_files\\'
        settings = sublime.load_settings('archive_save.sublime-settings')
        new_directory = settings.get('archive_directory')
        if new_directory is None or new_directory == '':
            new_directory = default_new_directory
        if new_directory[-1] != '\\':
            new_directory += '\\'
        if os.path.isdir(new_directory) == False:
            print( 'mkdir:'+new_directory)
            os.mkdir(new_directory)
        return new_directory

    def run(self, view):
        """ Save the file, then save it a second time into the archive diretory"""
        self.view.run_command("save")
        # The following line is a hack to reset the "file modified icon" on the tab
        sublime.set_timeout(lambda: self.view.run_command("revert"), 10)
        # Retrieve the current file name and build the archive-save path-and-filename
        cur_filename = self.view.file_name()
        if cur_filename is None:
            return
        new_directory = self.get_archive_directory()
        new_filename = new_directory + self.timecode() + '.' + self.slugname( cur_filename )
        # Copy the current (just saved) file to the new archive-save file (with archive name)
        shutil.copy( cur_filename, new_filename )

# eof
