package imagetagger;

import directorymanager.DirectoryManager;
import imagemanager.ImageFile;
import tagmanager.Tag;
import javafx.scene.control.CheckBox;
import javafx.scene.control.TreeItem;
import javafx.scene.image.Image;
import javafx.stage.DirectoryChooser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

/**
 * The controller for our main Window.
 */
class MainWindowController{

    /**
     * The controller for our main Window.
     */
    private static MainWindowController controller = new MainWindowController();

    /**
     * The directory manager that searches images in a directory.
     */
    private DirectoryManager directoryManager = new DirectoryManager();

    /**
     * The selected image file.
     */
    private ImageFile selectedImageFile;

    /**
     * Checks whether toggle is pressed or not.
     */
    private boolean toggleChecker = true;

    /**
     * The selected file.
     */
    private File file;


    /**
     * Constructor for MainWindowController
     */
    private MainWindowController() {}

    /**
     * Gets instance of this singleton.
     *
     * @return the instance of a MainWindowController
     */
    static MainWindowController getInstance() {
        return controller;
    }

    /**
     * Updates the directoryManager attribute.
     */
    void selectDirectory() {
        DirectoryChooser dcDialog = new DirectoryChooser();
        file = dcDialog.showDialog(null);
        if (file != null) {
            this.showImageNames();
            ProgramStage.getStage().setScene(CustomizeScene.getCustomizeScene());
        }
    }

    /**
     * Loads all the image files from the directory manager to image manager and then loads
     * all the image files in the javaFx TreeView in the CustomizeScene of the application.
     */
    void showImageNames(){
        toggleView();
        try {
            directoryManager.getDirectoryImages().clearImageList();
            directoryManager.addImagesDirectory();
            directoryManager.clearFilesList();
        } catch (Exception e) {
            System.out.println("There was an error");
        }

        CustomizeScene.root.getChildren().clear();
        for (ImageFile img : directoryManager.getDirectoryImages().getImageList()){
            if (!CustomizeScene.root.getChildren().contains(img.getName())){
                TreeItem<String> treeItem = new TreeItem<>(img.getName());
                CustomizeScene.root.getChildren().add( treeItem );
            }
        }

    }

    /**
     * Assigns the selected ImageFile to the class instance variable selectedImageFile.
     * Creates the Image object of javaFx from ImageFile data and loads it in the ImageView
     * in customize window.
     */
    void selectedImage(){
        try{
            TreeItem<String> item = CustomizeScene.treeView.getSelectionModel().getSelectedItem();

            for (ImageFile imageFile: directoryManager.getDirectoryImages().getImageList()) {

                if (item.getValue().equals( imageFile.getName() )) {
                    selectedImageFile = imageFile;
                    Image image = new Image(imageFile.getFile().toURI().toString());
                    CustomizeScene.imageView.setImage( image );
                }
            }
        }
        catch (Exception e){
            System.out.println("No directory chosen yet!");
        }
    }

    /**
     * Tags the selected Image in the Customize Scene's tree view with the text in the tag field.
     */
    void tagImage(){
        if (CustomizeScene.getTag() != null){
            String tagRepresentation = CustomizeScene.getTag();
            Tag tag = new Tag(tagRepresentation);
            selectedImageFile.tagImage( tag );
        }
        else{
            System.out.println( "Enter a tag" );
        }
    }

    /**
     * returns the selected image file/
     *
     * @return the image file hat has been selected
     */
    ImageFile getSelectedImageFile() {return selectedImageFile;}

    /**
     * Toggles between the getFilesInDirectory and getFilesUnderDirectory methods of the
     * directory manager.
     */
    private void toggleView(){
        if (file != null){
            CustomizeScene.root.setValue(file.getName());
            if (toggleChecker){ directoryManager.getFilesInDirectory(file);
                toggleChecker = false;
            } else {
                try {
                    directoryManager.getFilesUnderDirectory(file);
                } catch (Exception e) {
                    System.err.println("Images not Added.");
                }
                toggleChecker = true;
            }
        }
    }

    /**
     * Assigns the left menu for ImageTagScene.
     */
    void leftMenuBuilder() {
        try{
            ArrayList<Tag> tags = selectedImageFile.getTags();
            ImageTagScene.checkBoxes.clear();
            for (Tag tag: tags) {
                ImageTagScene.checkBoxes.add(new CheckBox(tag.getTag().substring(1, tag.getTag().length())));
            }
            ImageTagScene.leftBox.getChildren().clear();
            ImageTagScene.leftBox.getChildren().addAll(ImageTagScene.checkBoxes);
        }
        catch (Exception e){
            System.out.println("No directory chosen yet!");
        }
    }

    /**
     * Assigns the left menu for NameHistoryScene.
     */
    void leftNameMenuBuilder() {
        try{
            ArrayList<String> oldNames = findOldNames();
            NameHistoryScene.checkBoxes.clear();
            for (String oldName: oldNames) {
                NameHistoryScene.checkBoxes.add(new CheckBox(oldName));
            }
            NameHistoryScene.leftBox.getChildren().clear();
            NameHistoryScene.leftBox.getChildren().addAll(NameHistoryScene.checkBoxes);
        }
        catch (Exception e){
            System.out.println("No directory chosen yet!");
        }
    }

    /**
     * Returns a list of all old names an image had.
     *
     * @return the list of previous names an image had
     */
    private ArrayList<String> findOldNames() {
        ArrayList<String> oldNames = new ArrayList<>();
        try {
            File file = new File(System.getProperty("user.dir") + File.separator + "log.txt");
            Scanner sc = new Scanner(file);
            String[] selectedImageName = selectedImageFile.getName().split(" ");
            String pureName = selectedImageName[selectedImageName.length - 1];
            while (sc.hasNextLine()) {
                String curLine = sc.nextLine();
                String[] curLineSplitted = curLine.split(" ");
                if (curLineSplitted[0].equals("Old") && curLineSplitted[curLineSplitted.length - 1].equals(pureName)) {
                    if (! oldNames.contains(curLine.substring(9, curLine.length())))
                        oldNames.add(curLine.substring(9, curLine.length()));
                }
            }

        } catch (IOException e) {
            System.err.println("failed find old names");
        }
        return oldNames;
    }

    /**
     * Reads through all tags in our Master tag list.
     */
    void readAvailableTags(){
        try {
            File file = new File(System.getProperty("user.dir") + File.separator + "availableTags.txt");
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);


            String curLine = br.readLine();
            MasterTagListScene.checkBoxes = new ArrayList<>();
            while (curLine != null && !curLine.equals("")) {
                MasterTagListScene.checkBoxes.add(new CheckBox(curLine));
                curLine = br.readLine();
            }
            MasterTagListScene.leftBox.getChildren().clear();
            MasterTagListScene.leftBox.getChildren().addAll(MasterTagListScene.checkBoxes);


        } catch (IOException e) {
            e.getMessage();
        }
    }

    /**
     * Moves a specific image to a new directory.
     */
    void moveDirectory() {
        DirectoryChooser dcDialog = new DirectoryChooser();
        file = dcDialog.showDialog(null);
        if (file != null) {
            String filename = selectedImageFile.getName();
            File moveToFile = new File(file + File.separator + filename);
            selectedImageFile.getFile().renameTo(moveToFile);
            showImageNames();
        }
    }

    /**
     * Returns a list of all images containing a specific tag.
     *
     * @param tag the tag string representation to search images
     * @return the list of all images containing the tag
     */
    ArrayList<String> findImageFileWithTags(String tag) {
        ArrayList<String> toReturn = new ArrayList<>();
        ArrayList<ImageFile> allFiles = directoryManager.getDirectoryImages().getImageList();
        for (ImageFile imageFile: allFiles) {
            if (Arrays.asList(imageFile.getName().split(" ")).contains(tag)) {
                toReturn.add(imageFile.getName());
            }
        }
        return toReturn;
    }

}
