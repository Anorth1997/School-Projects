package tagmanager;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * A manager for a collection of tags.
 */
public class TagManager {

    /**
     * The collection of all tags an image has.
     */
    private ArrayList<Tag> tagList = new ArrayList<>();

    /**
     * The Master tag list, a collection of all tags ever created.
     */
    private static ArrayList<Tag> allAvailableTags = new ArrayList<>();

    /**
     * The path of the configuration file which shows all the master tag list.
     */
    private final static String filePath = System.getProperty("user.dir") + File.separator + "availableTags.txt";


    /**
     * Constructor for the TagManager.
     */
    public TagManager() {}

    /**
     * Updates the Master tag list.
     */
    private void updateCurrentTags() {
        readAvailableTagsFile();
        for (Tag t: tagList) {
            if (!masterTagListContainsTag(t)) {
                TagManager.allAvailableTags.add(t);
            }
        }
        clearFile();
        writeFile();
    }

    /**
     * Returns whether a tag is present in the Master tag list.
     *
     * @param tag the Tag to check
     * @return whether tag is in allAvailableTags
     */
    private static boolean masterTagListContainsTag(Tag tag) {
        for (Tag tg: allAvailableTags) {
            if (tg.equals(tag)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Delete tags from the list of all available tags.
     *
     * @param tag The tag to delete
     */
    public static void deleteTagFromCurrentTags(Tag tag){
        readAvailableTagsFile();
        if (TagManager.masterTagListContainsTag(tag)) {
            System.out.println("goes here yo");
            int indexOfTag = -1;
            for (int i = 0; i < TagManager.allAvailableTags.size(); i++) {
                if (TagManager.allAvailableTags.get(i).equals(tag)) {
                    indexOfTag = i;
                }
            }
            if (indexOfTag != -1) {
                TagManager.allAvailableTags.remove(indexOfTag);
            }
            clearFile();
            writeFile();
        }

    }

    /**
     * Adds the tag in tagList if the tag doesn't exist in the tagList otherwise throws an exception.
     *
     * @param tag A new Tag to be added to tagList
     */
    public void addTag(Tag tag) {
        if (tag.isValidTag() && !this.containsTag(tag)) {
            tagList.add(tag);
        }
        updateCurrentTags();
    }

    /**
     * Removes the given tag from the collection of tags.
     *
     * @param tag the Tag to remove from tagList
     */
    public void removeTag(Tag tag) {
        if (this.containsTag(tag)) {
            int indexOfTag = -1;
            for (int i = 0; i < tagList.size(); i++) {
                if (tagList.get(i).equals(tag)) {
                    indexOfTag = i;
                }
            }
            if (indexOfTag != -1) {
                tagList.remove(indexOfTag);
            }
        }
    }

    /**
     * Deletes all tags of an image.
     */
    public void resetTags() {
        tagList = new ArrayList<>();
    }

    /**
     * Checks if the tagList contains the given tag or not.
     *
     * @param tag A tag to be checked
     * @return whether Tag is in tagList
     */
    public boolean containsTag(Tag tag) {
        for (Tag tg: tagList) {
            if (tg.equals(tag)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Returns the list of all the tags for an image..
     *
     * @return the list of all tags tagList
     */
    public ArrayList<Tag> getTagList() {
        return tagList;
    }

    /**
     * Returns the String representation of the collection of tags.
     *
     * @return a String representation of the tagList.
     */
    public String toString() {
        if (tagList.size() == 0) {
            return "The tag manager is empty.";
        } else {
            StringBuilder tags = new StringBuilder();
            for (Tag t : tagList) {
                tags.append(t.toString()).append("\n");
            }
            return tags.toString();
        }
    }

    /**
     * All the tags in availableTag.txt are derived into allAvailableTags.
     */
    private static void readAvailableTagsFile(){
        try {
            File file = new File(filePath);
            if (!file.exists()) {
                System.out.println("Creating new Master Tag List!");
                file.createNewFile();
            } else {
                Scanner sc = new Scanner(file);
                ArrayList<Tag> textTags = new ArrayList<>();
                while (sc.hasNextLine()) {
                    String tagRepresentation = sc.nextLine();
                    if (!tagRepresentation.equals("")) {
                        textTags.add(new Tag(tagRepresentation));
                    }
                }
                for (Tag t : textTags) {
                    if (!masterTagListContainsTag(t)) {
                        allAvailableTags.add(t);
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("couldn't read the file");
        }
    }

    /**
     * Clears the content of a text file.
     */
    private static void clearFile() {
        try {
            FileWriter f = new FileWriter(filePath);
            f.write("");
            f.close();
        } catch (IOException e) {
            System.err.println("Failed to clear the file!");
        }
    }

    /**
     * Write all the tags in allAvailableTags into availableTag.txt.
     */
    private static void writeFile() {
        try {
            FileWriter fileWriter = new FileWriter(filePath, true);
            for (Tag tag : allAvailableTags) {
                fileWriter.write(tag.getRepresentation() + "\n");
                fileWriter.flush();
            }
        } catch (IOException e) {
            System.err.println("Failed to write into the file!");
        }
    }

}
