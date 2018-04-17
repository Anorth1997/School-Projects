package tagmanager;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * A tag that can be added to an image name.
 */
public class Tag {

    /**
     * The string representation of the tag.
     */
    private String representation;

    /**
     * The representation of the tag with the "@" symbol in front.
     */
    private String tagRepresentation;

    /**
     * The time the tag was created.
     */
    private String timeStamp;


    /**
     * Constructor for the Tag class.
     *
     * @param rep the string representation of the tag.
     */
    public Tag(String rep) {
        this.representation = rep.trim();
        this.tagRepresentation = "@" + this.representation;
        this.timeStamp = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date());
    }

    /**
     * Returns the string tag representation of the Tag with '@' sign added to its front.
     *
     * @return the representation of the tag with the "@" symbol
     */
    public String getTag(){
        return tagRepresentation;
    }

    /**
     * Returns the string representation of the Tag.
     *
     * @return string representation
     */
    String getRepresentation() {
        return representation;
    }

    /**
     * Returns the time stamp of the creation of the Tag.
     *
     * @return timestamp the time stamp of a given tag.
     */
    public String getTimeStamp(){
        return timeStamp;
    }

    /**
     * Returns a string representation of the tag to print.
     *
     * @return a string representation of the Tag.
     */
    public String toString(){
        return "Tag: " + getTag() + " Created at : " + timeStamp;
    }

    /**
     * Returns whether two tags have the same string representation
     *
     * @param otherTag Other tag to compare with.
     * @return whether two tags are equal
     */
    public boolean equals(Tag otherTag){
        return this.representation.equals(otherTag.representation);
    }

    /**
     * Returns whether the tag does not contain the "@" symbol.
     *
     * @return whether a tag is valid
     */
    boolean isValidTag(){
        return !this.representation.contains("@");
    }
}
