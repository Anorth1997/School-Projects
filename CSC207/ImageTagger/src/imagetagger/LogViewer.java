package imagetagger;

import javafx.scene.Scene;
import javafx.scene.control.TextArea;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * The Viewer to display the log.
 */
class LogViewer {

    /**
     * Reads and displays the log file log.txt
     */
    static void display(){
        Stage primaryStage =  new Stage();
        primaryStage.setTitle("Master Log");

       TextArea textArea = new javafx.scene.control.TextArea();
        textArea.setEditable(false);
        File file = new File(System.getProperty("user.dir") + File.separator + "log.txt");
        StringBuilder line = new StringBuilder();
        String curLine = "";
        try {
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);

            while (curLine != null) {
                curLine = br.readLine();
                if (curLine != null){
                line.append(curLine).append("\n");
                textArea.setText(line.toString());
                }
            }
        }catch (IOException e){
            e.getMessage();
        }

        StackPane layout = new StackPane();


        primaryStage.setResizable(true);
        layout.getChildren().add(textArea);

        Scene scene = new Scene(layout, 300, 250);
        primaryStage.setScene(scene);
        primaryStage.show();

    }
}
