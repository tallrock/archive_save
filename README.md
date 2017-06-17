# archive_save - Sublime Text 3 Plug-in


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

## THE ARCHIVE FILENAME

I save the archive file with two changes in order to guarantee uniqueness:  
(1) I slugify the filename (no spaces,slashes,colons)  
(2) I prefix the filename with a time-stamped-to-the-millisecond code.

So a file like 'c:\goals\march list.txt' becomes 'j3jryh4g.c.goals.march.list.txt'

## THE SUBLIME-SETTINGS FILE

Put this file in Sublime's Packages/User directory:

filename: Sublime Text 3/Packages/User/archive_save.sublime-settings

> {  
>     "archive_directory": "C:\\archive_saved_files\\"  
> }

## THE KEY BINDINGS FILE

> [  
>     { "keys": ["alt+ctrl+s"], "command": "archive_save" },  
>     { "keys": ["ctrl+s"], "command": "save" }  
> ]

(I have entries for the regular save as well because I'm a belts-and-suspenders guy).


