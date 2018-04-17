package imagetagger;


import imagemanager.ImageFile;
import tagmanager.Tag;
import tagmanager.TagManager;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;

import java.util.ArrayList;


/**
 * All the buttons in our application.
 */
class ApplicationButtons {

    /**
     * A controller for the Main Window.
     */
    private MainWindowController controller = MainWindowController.getInstance();


    /**
     * Instantiates a new Application buttons.
     */
    ApplicationButtons(){}

    /**
     * Return the Search file button that searches through a directory.
     *
     * @return the button to search file
     */
    Button searchFileButton() {
        Button selectDirectory = new Button( "Search Files" );
        selectDirectory.setOnAction(e -> controller.selectDirectory());
        selectDirectory.setStyle("-fx-background-color: silver;");
        return selectDirectory;
    }

    /**
     * Return the Master Tag button that displays all tags ever created.
     *
     * @return the button to display the master tag list
     */
    Button masterTagsButton() {
        Button viewAllTags = new Button( "Master Tag" );
        viewAllTags.setOnAction( e -> {
            controller.readAvailableTags();
            ProgramStage.getStage().setScene(MasterTagListScene.getScene());
        });
        viewAllTags.setStyle("-fx-background-color: silver;");

        return viewAllTags;
    }


    /**
     * Return the Image Tag button that displays all image tags.
     *
     * @return the button to display the image tag list
     */
    Button imageTagsButton() {
        Button viewImageTags = new Button( "View Image Tags" );
        viewImageTags.setOnAction( e -> {
            controller.leftMenuBuilder();
            ProgramStage.getStage().setScene(ImageTagScene.getScene());
        });
        viewImageTags.setStyle("-fx-background-color: silver;");
        return viewImageTags;
    }

    /**
     * Return a back button to let the user goes back to previous scene.
     *
     * @return the button to go back to the previous scene
     */
    Button backButton(){
        Button back = new Button("Back");
        back.setOnAction(e -> {
            controller.showImageNames();
            ProgramStage.getStage().setScene(CustomizeScene.getCustomizeScene());
        });
        back.setStyle("-fx-background-color: silver;");
        return back;
    }

    /**
     * Return the Master Log button that displays the log of all renaming.
     *
     * @return the button to display the master log
     */
    Button masterLogButton() {
        Button viewLog = new Button( "Master Log" );
        viewLog.setOnAction( e -> LogViewer.display());
        viewLog.setStyle("-fx-background-color: silver;");

        return viewLog;
    }

    /**
     * Return the Toggle view button. Sets the toggle action to view images in and under a
     * selected directory in tree view.
     *
     * @return the button to toggle between directory visits
     */
    Button toggleViewButton() {
        Button toggleView = new Button( "Toggle" );
        toggleView.setOnAction( e -> controller.showImageNames());
        toggleView.setStyle("-fx-background-color: silver;");
        return toggleView;
    }

    /**
     * Return the Back button. Sets the action to return to the main scene of the program.
     *
     * @return the button to return to the main scene
     */
    Button homeButton(){
        Button home = new Button("Home");
        home.setOnAction(e -> ProgramStage.getStage().setScene( HomeScene.getScene() ));
        home.setStyle("-fx-background-color: silver;");
        return home;
    }

    /**
     * Return the tag image button. Sets the action to tag the selected ImageFile with
     * the entered tag in tag field.
     *
     * @return the button to tag an image
     */

    Button tagButton(){
        Button tagImage = new Button("Tag Image");
        tagImage.setOnAction(e ->
        {if(!CustomizeScene.getTag().equals( "" )){
            controller.tagImage();
            controller.showImageNames();
            controller.showImageNames();}
        } );
        tagImage.setStyle("-fx-background-color: silver;");
        return tagImage;
    }

    /**
     * Return the button that clears out all the tags of a selected image file.
     *
     * @return the button to reset all tags an image has
     */
    Button resetButton(){
        Button resetButton = new Button("Reset");
        resetButton.setOnAction(e -> {
            ImageFile toDelete = controller.getSelectedImageFile();
            toDelete.resetImageTags();
            controller.leftMenuBuilder();
            ProgramStage.getStage().setScene(ImageTagScene.getScene());
        });
        resetButton.setStyle("-fx-background-color: silver;");
        return resetButton;
    }

    /**
     * Return the button to remove a tag from an image.
     *
     * @return the button to delete an image tag
     */
    Button removeImageFileTagsButton(){
        Button removeButton = new Button("Remove");
        removeButton.setOnAction(e -> {
            ImageFile toModify = controller.getSelectedImageFile();
            ArrayList<String> toDelete = new ArrayList<>();
            for (CheckBox box: ImageTagScene.checkBoxes) {
                if (box.isSelected()) {
                    toDelete.add(box.getText());
                }
            }
            toModify.removeTag(toDelete);
            controller.showImageNames();
            controller.leftMenuBuilder();
            ProgramStage.getStage().setScene(ImageTagScene.getScene());

        });
        removeButton.setStyle("-fx-background-color: silver;");
        return  removeButton;
    }

    /**
     * Return the button to revert the name of this ImageFile back to the selected old name.
     *
     * @return the button to revert an image name
     */
    Button changeNameButton(){
        Button changeNameButton = new Button("Change Name");
        changeNameButton.setOnAction(e -> {
            ImageFile toRename = controller.getSelectedImageFile();
            for (CheckBox box: NameHistoryScene.checkBoxes) {
                if (box.isSelected()) {
                    toRename.changeName(box.getText());
                }
            }
        });
        changeNameButton.setStyle("-fx-background-color: silver;");
        return changeNameButton;
    }

    /**
     * Return the button that pops up the window demonstrating all the past names of this
     * imageFile
     *
     * @return the button to switch scene to revert name
     */
    Button revertNameButton() {
        Button revertNameButton = new Button("Revert Name");
        revertNameButton.setOnAction(e -> {
            controller.leftNameMenuBuilder();
            ProgramStage.getStage().setScene(NameHistoryScene.getScene());
        });
        revertNameButton.setStyle("-fx-background-color: silver;");
        return revertNameButton;
    }

    /**
     * Return the button to remove the tags from MasterTagList, modify the file
     * availableTags.txt at the same time.
     *
     * @return the button to remove the tags from MasterTagList
     */
    Button removeMasterTagButton() {
        Button removeMasterTagButton = new Button("Remove Tag");
        removeMasterTagButton.setOnAction(e -> {
            ArrayList<Tag> toDelete = new ArrayList<>();
            for (CheckBox box: MasterTagListScene.checkBoxes) {
                if (box.isSelected()) {
                    toDelete.add(new Tag(box.getText()));
                }
            }

            for (Tag tag: toDelete) {
                TagManager.deleteTagFromCurrentTags(tag);
            }
            controller.readAvailableTags();
            ProgramStage.getStage().setScene(MasterTagListScene.getScene());
        });
        removeMasterTagButton.setStyle("-fx-background-color: silver;");
        return removeMasterTagButton;
    }

    /**
     * Return the button to move an image to a new directory.
     *
     * @return the button to move an image
     */
    Button moveToButton() {
        Button moveToButton = new Button("Move To");
        moveToButton.setOnAction(e -> controller.moveDirectory());
        moveToButton.setStyle("-fx-background-color: silver;");
        return moveToButton;
    }

    /**
     * Return the button to show all files containing a specific tag.
     *
     * @return the button to show images under a certain tag
     */
    Button showFilesContainsTag() {
        Button showFilesContainsTag = new Button("Show Files With Tag");
        showFilesContainsTag.setOnAction(e -> {
            if (!CustomizeScene.getTag().equals("")) {
                InterestingFeatureWindow.display(CustomizeScene.getTag());
            }
        });
        showFilesContainsTag.setStyle("-fx-background-color: silver;");
        return showFilesContainsTag;
    }
}
