About this project:

The user is able to choose a directory and view a list of all image files anywhere under that directory, and also show a list of images in that directory. When viewing an image, the user can select tags from the currently-existing tags, and the user can also add new tags and delete existing ones from the currently-existing ones. The application will rename the image file to include the tags, each prefixed with the "@" character. For example, if the user has tagged an image with "Aunt June" and "Samantha", then the file will be renamed to include "@Aunt June @Samantha". This allows the user to use their operating system to search for image files. The user should also be able to open (directly in their OS's file viewer) the directory containing the current image file.

The user is able to move a file to another directory.

The user is able to go back to older sets of tags for a particular file. Provided that an image has not been manually moved or renamed using the OS, the user can view all the names that a file has had. For example, if the user views the image with Aunt June and Samantha, they can choose to view both the original name and the name that includes "@Aunt June @Samantha". The user can choose to go back to an older name.

The list of available tags persists when the application is quit and reopened.

The user wants a log of all renaming ever done (old name, new name, and timestamp).

When the program is first run, it should create any configuration files that it needs, and if they are deleted it should recreate them the next time it is run.

The user is able to search the files with a particular tag under a directory.

