package imagetagger;


import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.image.Image;
import javafx.scene.layout.*;

import java.io.File;
import java.util.ArrayList;


/**
 * The window that manage the tags of an image.
 */
class ImageTagScene {

    /**
     * The buttons to use in this scene
     */
    private ApplicationButtons appButtons = new ApplicationButtons();

    /**
     * The Scene to display in ImageTagScene.
     */
    private static Scene imageTagScene;

    /**
     * This is the ArrayList of all checkboxes in the left hand part of scene.
     */
    static ArrayList<CheckBox> checkBoxes = new ArrayList<>();

    /**
     * This is the appearance of all the checkboxes, and make them in vertical order.
     */
    static VBox leftBox = new VBox(20);


    /**
     * Instantiate an instance of ImageTagScene
     */
    ImageTagScene(){}


    /**
     * Sets up the scene.
     */
    void setImageTagScene(){

        BorderPane borderPane = layout();
        imageTagScene = new Scene(borderPane, 300, 600);
    }

    /**
     * Returns the scene.
     *
     * @return the scene
     */
    static Scene getScene(){
        return imageTagScene;
    }


    /**
     * This method produces the BorderPane that will be applied in imageTagScene
     * @return BorderPane the layout
     */
    private BorderPane layout(){
        BorderPane border = new BorderPane();
        VBox left = leftBox;
        VBox right = this.rightMenu();

        border.setLeft(left);
        border.setRight(right);

        border.setStyle("-fx-background-color: silver;");
        return border;
    }

    /**
     * This method produces the right hand part of imageTagScene. It will be added into
     * our BorderPane layout first.
     *
     * @return VBox that is the right menu
     */
    private VBox rightMenu(){
        Button back = appButtons.backButton();
        Button reset = appButtons.resetButton();
        Button remove = appButtons.removeImageFileTagsButton();
        VBox rightBox = new VBox(20);
        rightBox.setStyle("-fx-background-color: silver;");
        rightBox.getChildren().addAll(reset, remove, back);
        return rightBox;
    }

}
