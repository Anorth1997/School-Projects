package imagetagger;

import javafx.application.Application;
import javafx.stage.Stage;

/**
 * The ImageTagger Application
 */
public class ImageTagger extends Application{

    /**
     * Main method to run the application.
     * @param args A default input parameter.
     */
    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception {

        // Create the main window.
        ProgramStage window = new ProgramStage();

        // Display the main window.
        window.display();
    }
}