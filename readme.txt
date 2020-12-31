STRUCTURE
ROOT_FOLDER/copy_date/img_folders

OUTPUT FOLDER: ROOT_FOLDER/OUTPUT_FOLDER


WORKING

give ROOT_FOLDER, without '/' ending.

run the program.
i - check the files without rendering - only for checking the files list and the correct working.


RENDER IMAGES INTO VIDEOS
start the rendering process with folders.
render files into videos_done folder with _temp_ starting.
After the rendering is done, rename the file: remove the _temp_ starting.


APPEND VIDEOS INTO ONE VIDEO
start rendering one by one videos, and create a file with starting '_temp__done_until_'.
after the rendering is done, rename the file to '_done_until_' + the last added videos name.


RESTART
The app recognise the interrupted rendering and appending. It looks for '_temp_' naming.
After restart, the app will continue the process from the point where it was interrupted.

