package imagetagger;

import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;

import java.util.ArrayList;

/**
 * This class is responsible for MasterTagList scene. It shows all the tags that user has ever had.
 */
class MasterTagListScene {

    /**
     * The buttons to use in this scene
     */
    private ApplicationButtons appButtons = new ApplicationButtons();

    /**
     * The Scene to display in masterTagListScene.
     */
    private static Scene masterTagListScene;

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
    MasterTagListScene(){}


    /**
     * Set imageTagScene
     */
    void setMasterTagListScene(){
        BorderPane borderPane = layout();
        masterTagListScene = new Scene(borderPane, 300, 600);
    }

    /**
     * Get scene.
     *
     * @return the scene
     */
    static Scene getScene(){
        return masterTagListScene;
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
        return border;
    }


    /**
     * This method produces the right hand part of imageTagScene. It will be added into our BorPane layout first.
     * @return VBox
     */
    private VBox rightMenu(){
        Button home = appButtons.homeButton();
        Button remove = appButtons.removeMasterTagButton();
        VBox rightBox = new VBox(20);
        rightBox.getChildren().addAll(home, remove);
        return rightBox;
    }
}
