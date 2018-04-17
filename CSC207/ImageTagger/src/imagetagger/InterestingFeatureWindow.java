package imagetagger;

import javafx.scene.Scene;
import javafx.scene.control.TextArea;
import javafx.scene.layout.StackPane;
import javafx.stage.Modality;
import javafx.stage.Stage;

import java.util.ArrayList;

/**
 * This is our project's interesting feature. It shows all the files in current directory that contains the
 * user input tag.
 */
class InterestingFeatureWindow {

    /**
     * This window will need the assistance of MainWindowController's methods.
     * This controller instance is instantiated to allow this class get access with
     * MainWindowController.
     */
    private static MainWindowController controller = MainWindowController.getInstance();


    /**
     * To display this window
     *
     * @param tag The user input tag.
     */
    static void display(String tag) {
        Stage window = new Stage();

        window.initModality(Modality.APPLICATION_MODAL);
        window.setTitle("The Images contains " + tag + "in this directory");
        window.setMinWidth(300);

        TextArea textArea = new javafx.scene.control.TextArea();
        textArea.setEditable(false);
        ArrayList<String> toAdd = controller.findImageFileWithTags("@" + tag);
        StringBuilder line = new StringBuilder();
        for (String name: toAdd) {
            line.append(name).append("\n");
            textArea.setText(line.toString());
        }

        StackPane layout = new StackPane();
        layout.getChildren().add(textArea);

        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();
    }
}
