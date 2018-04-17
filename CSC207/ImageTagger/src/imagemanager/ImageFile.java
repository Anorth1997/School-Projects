package imagemanager;

import loggingsystem.ImageLogger;
import tagmanager.Tag;
import tagmanager.TagManager;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Observable;

/**
 * An image that can be viewed and get tagged.
 */
public class ImageFile extends Observable{

    /**
     * The image's name.
     */
    private String imageName;

    /**
     * The image file in a directory.
     */
    private File file;

    /**
     * A manager for the collection of tags an image has.
     */
    private TagManager tagManager;

    /**
     * A logger that will update whenever the image is renamed.
     */
    private ImageLogger logger = ImageLogger.getOurInstance();


    /**
     * Constructor for the ImageFile class.
     *
     * @param fileOfImage the file pathname of the image
     */
    public ImageFile(File fileOfImage) {
        imageName = fileOfImage.getName();
        file = fileOfImage;
        tagManager = scanNameForTags(imageName);
    }

    /**
     * Returns a manager for the collection of tags present in an image's name after scanning an
     * image for tags in its name.
     *
     * @param name the image file name
     * @return a manager of all tags
     * @see TagManager
     */
    private TagManager scanNameForTags(String name) {
        TagManager newTagManager = new TagManager();
        String[] nameSplit = name.split(" ");
        for (String word: nameSplit) {
            if (word.charAt(0) == '@') {
                Tag t = new Tag(word.substring(1, word.length()));
                newTagManager.addTag(t);
            }
        }
        return newTagManager;
    }

    /**
     * Tag an image.
     *
     * @param tag A tag to add to the image
     */
    public void tagImage(Tag tag) {
        if (!tagManager.containsTag(tag)) {
            tagManager.addTag(tag);
            String newName = tag.getTag() + " " + imageName;
            setName(newName);
        }
    }

    /**
     * Return the name of this ImageFile.
     *
     * @return the name of this ImageFile
     */
    public String getName() {
        return imageName;
    }


    public void changeName(String newName) {
        setName(newName);
    }
    /**
     * Set a new name for this ImageFile.
     *
     * @param newName the new name of this image
     */
    private void setName(String newName) {
        String oldName = this.getName();
        imageName = newName;
        String directory = file.getParent();
        File newFile = new File(directory + File.separator + imageName);
        if (file.renameTo(newFile)) {
            file = newFile;
            System.out.println("Image has been renamed");
        } else {
            System.err.println("Image could not be renamed!");
        }
        setChanged();
        notifyObserver(oldName);
    }

    /**
     * Return the file of this ImageFile.
     *
     * @return the file of this ImageFile
     */
    public File getFile() {
        return file;
    }

    /**
     * Return the list of tags this image has.
     *
     * @return the tags of this ImageFile
     */
    public ArrayList<Tag> getTags() {
        return tagManager.getTagList();
    }

    /**
     * Return whether two images share the same name and file location.
     *
     * @param otherImage an ImageFile to compare
     * @return whether two images are identical
     */
    boolean equals(ImageFile otherImage) {
        return imageName.equals(otherImage.imageName) && this.file.equals(otherImage.file);
    }

    /**
     * Return a string representation of an ImageFile.
     *
     * @return string representation of this image
     */
    @Override
    public String toString() {
        return imageName;
    }

    /**
     * Notify the observer of a change having occurred.
     *
     * @param oldName the old name of the image before the change
     */
    private void notifyObserver(String oldName) {
        logger.update(this, oldName);
    }

    /**
     * Clears all the image tags from the tagManager and image name.
     */
    public void resetImageTags() {
        tagManager.resetTags();
        String oldName = getName();
        String[] handleIt = oldName.split(" ");
        String newName = handleIt[(handleIt.length - 1)];
        setName(newName);
    }

    /**
     * Removes a list of tags from the image name.
     *
     * @param tagList the list of tags to remove
     */
    public void removeTag(ArrayList<String> tagList) {
        for (String tagText: tagList) {
            tagManager.removeTag(new Tag(tagText));
        }
        String oldName = getName();
        ArrayList<String> handleIt = new ArrayList<>(Arrays.asList(oldName.split(" ")));
        for (String word: tagList) {
            if (handleIt.contains("@" + word)) {
                handleIt.remove("@" + word);
            }
        }
        StringBuilder newName = new StringBuilder();
        for (String word: handleIt) {
            newName.append(" " + word);
        }

        setName(newName.toString().substring(1, newName.length()));
    }
}
