package imagemanager;

import java.util.ArrayList;


/**
 * A manager for a collection of images for a specific a directory.
 */
public class ImageManager {

    /**
     * A list of images to manage.
     */
    private ArrayList<ImageFile> imageList = new ArrayList<>();

    /**
     * Constructor for the ImageManager class.
     */
    public ImageManager() {}

    /**
     * Adds an image to the collection of images imageList.
     *
     * @param image The ImageFile to add to imageList
     */
    public void addImage(ImageFile image) {
        if (!this.containsImage(image)) {
            imageList.add(image);
        }
    }

    /**
     * Deletes an image in the collection of images imageList.
     *
     * @param image The ImageFile to delete from imageList
     */
    public void removeImage(ImageFile image) {
        if (this.containsImage(image)) {
            imageList.remove(image);
        }
    }

    /**
     * Checks if the imageList contains the given image.
     *
     * @param image An ImageFile to be checked
     * @return whether image is in imageList
     */
    private boolean containsImage(ImageFile image) {
        for (ImageFile im: imageList) {
            if (im.equals(image)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Return the list of images in directory.
     *
     * @return the images in directory imageList
     */
    public ArrayList<ImageFile> getImageList() {
        return imageList;
    }

    /**
     * Clears imageList.
     */
    public void clearImageList() {
        imageList.clear();
    }

}
