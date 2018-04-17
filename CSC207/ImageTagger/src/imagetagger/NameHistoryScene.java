package imagetagger;

import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;

import java.util.ArrayList;

/**
 * The Naming history scene
 */
class NameHistoryScene {

    /**
     * The set of all buttons for our application.
     */
    private ApplicationButtons appButtons = new ApplicationButtons();

    /**
     * The naming history scene.
     */
    private static Scene NameHistoryScene;

    /**
     * A list of checkboxes of all names.
     */
    static ArrayList<CheckBox> checkBoxes = new ArrayList<>();

    /**
     * The button box.
     */
    static VBox leftBox = new VBox(20);

    /**
     * Instantiates a new NameHistoryScene
     */
    NameHistoryScene() {}

    /**
     * Sets up the scene.
     */
    void setNameHistoryScene() {
        BorderPane borderPane = layout();
        NameHistoryScene = new Scene(borderPane, 600, 600);
    }

    /**
     * Returns the scene.
     *
     * @return the naming history scene
     */
    static Scene getScene(){
        return NameHistoryScene;
    }

    /**
     * Returns the layout of the scene.
     *
     * @return the BorderPane layout
     */
    private BorderPane layout(){
        BorderPane border = new BorderPane();
        VBox left = leftBox;
        VBox right = rightMenu();

        border.setLeft(left);
        border.setRight(right);
        return border;
    }

    /**
     * Returns the right menu of the BorderPane layout.
     *
     * @return the right menu of the layout
     */
    private VBox rightMenu(){
        Button back = appButtons.backButton();
        Button changeName = appButtons.changeNameButton();
        VBox rightBox = new VBox(20);
        rightBox.getChildren().addAll(changeName, back);
        return rightBox;
    }
}
