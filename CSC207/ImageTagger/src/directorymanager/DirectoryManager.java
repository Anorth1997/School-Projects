package directorymanager;

import imagemanager.ImageManager;
import imagemanager.ImageFile;

import javax.activation.MimetypesFileTypeMap;
import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.Arrays;


/**
 * A class that visits a directory and manages all images in or under ir.
 */
public class DirectoryManager extends SimpleFileVisitor<Path> {

    /**
     * The collection of images for a directory.
     */
    private ImageManager directoryImages = new ImageManager();
    /**
     * A list of all files inside a directory.
     */
    private ArrayList<File> fileList = new ArrayList<>();


    /**
     * Constructs a new Directory manager.
     */
    public DirectoryManager() {
        super();
    }

    @Override
    public FileVisitResult preVisitDirectory(Path path, BasicFileAttributes attrs) throws IOException {
        File f = new File(path.toString());
        this.fileList.add(f);
        return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult visitFile(Path path, BasicFileAttributes attrs) throws IOException {
        File f = new File(path.toString());
        this.fileList.add(f);
        return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult visitFileFailed(Path path, IOException exc) throws IOException {
        System.err.println(exc.getMessage());
        return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult postVisitDirectory(Path path, IOException exc) throws IOException {
        return FileVisitResult.CONTINUE;
    }

    /**
     * Gets images under a specific directory.
     *
     * @param file the directory file
     * @throws IOException the io exception
     */
    public void getFilesUnderDirectory(File file) throws IOException {
        String filePath = file.getPath();
        Path path = Paths.get(filePath);
        Files.walkFileTree(path, this);
    }

    /**
     * Get images in a specific directory.
     *
     * @param file the directory file
     */
    public void getFilesInDirectory(File file) {
        File[] fileArray = file.listFiles();
        if (fileArray != null && fileArray.length != 0) {
            this.fileList.addAll(Arrays.asList(fileArray));
        } else {
            System.out.println("Given Directory is empty.");
        }
    }

    /**
     * Add the images in fileList to the collection of images directoryImages.
     */
    public void addImagesDirectory() {
        for (File f: fileList) {
            if (isValidImage(f)) {
                try {
                    ImageFile im = new ImageFile(f);
                    directoryImages.addImage(im);
                } catch (Exception e) {
                    System.out.println("Image not Added!");
                }
            }
        }
    }

    /**
     * Returns whether a file is a valid image.
     *
     * @param file the file to check
     * @return whether a file is a valid Image
     */
    private boolean isValidImage(File file) {
        String mimeType = new MimetypesFileTypeMap().getContentType(file);
        String type = mimeType.split("/")[0];
        return type.equals("image");
    }

    /**
     * Return the collection of images directoryImages for a specific directory.
     *
     * @return the images stored in/under a directory
     * @see ImageManager
     */
    public ImageManager getDirectoryImages() {
        return directoryImages;
    }

    /**
     * Clear the list of all files in a directory fileList.
     */
    public void clearFilesList(){
        fileList.clear();
    }
}
