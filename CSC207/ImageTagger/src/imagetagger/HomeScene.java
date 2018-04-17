package imagetagger;

import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.layout.*;
import javafx.scene.text.Font;

import java.io.File;

/**
 * The type Main window.
 * This is responsible for the appearance of Scene when the program is runned.
 */
class HomeScene {

    /**
     * The buttons to use in this scene
     */
    private ApplicationButtons appButtons = new ApplicationButtons();

    /**
     * The Scene to display in HomeScene
     */
    private static Scene sceneMain;

    /**
     * The pane will be use in sceneMain.
     */
    private BorderPane borderPane = new BorderPane(  );


    /**
     * Instantiates a new Home scene.
     */
    HomeScene(){}

    /**
     * Displays the main window of the Photo Tagger application.
     */
    void setMainScene() {

        // add layout into sceneMain, this is the initial window we have
        sceneMain = new Scene(layout(),950, 650);
        borderPane.prefHeightProperty().bind(sceneMain.heightProperty());
        borderPane.prefWidthProperty().bind(sceneMain.widthProperty());
    }

    /**
     * Get scene scene.
     *
     * @return the scene
     */
    static Scene getScene(){

        return sceneMain;
    }

    /**
     * Builds and returns the main layout of the user interface.
     *
     * @return layout A BorderPane layout of the interface.
     */
    private BorderPane layout() {

        VBox leftMenu = this.leftSideMenu();
        //ImageView welcome = this.backGround();

        MenuBar menuBar = this.topMenu();

        borderPane.setTop( menuBar );
        borderPane.setLeft( leftMenu );

        // Setting background image
        File file = new File(System.getProperty("user.dir") + File.separator + "WelcomeScene.jpg");
        Image image = new Image(file.toURI().toString());
        borderPane.setPrefSize( 666,1000 );
        BackgroundImage myBI= new BackgroundImage(image,
                BackgroundRepeat.NO_REPEAT, BackgroundRepeat.NO_REPEAT, BackgroundPosition.DEFAULT,
                BackgroundSize.DEFAULT);
        borderPane.setBackground(new Background(myBI));

        return borderPane;
    }

    /**
     * Builds and returns the left side menu with required tools.
     *
     * @return Vbox tool buttons to access the
     */
    private VBox leftSideMenu() {

        VBox vb = new VBox( 30 );
        vb.setPadding( new Insets( 20, 10, 200, 10 ) );
        vb.setPrefWidth( 200 );

        // Tools label for right menu
        final Label name = new Label( "Tools" );
        name.setFont(new Font("Times New Roman",20));

        // Buttons for the right menu of main window
        Button searchFileButton = appButtons.searchFileButton();
        searchFileButton.setMinSize( vb.getPrefWidth(), 100 );

        Button masterTagsButton = appButtons.masterTagsButton();
        masterTagsButton.setMinSize( vb.getPrefWidth(), 100 );

        Button viewLog = appButtons.masterLogButton();
        viewLog.setMinSize( vb.getPrefWidth(), 100 );

        vb.getChildren().addAll( name, searchFileButton , masterTagsButton,
                 viewLog);

        return vb;
    }

    /**
     * Builds and returns the right side menu with required tools.
     * @return VBox tool buttons to access the
     */
    private MenuBar topMenu() {

        MenuBar menuBar = new MenuBar();

        // Defining Menu
        Menu fileMenu = new Menu( "File" );
        Menu helpMenu = new Menu( "Help" );

        menuBar.getMenus().addAll( fileMenu, helpMenu );
        menuBar.setStyle("-fx-background-color: TransParent; -fx-padding: 10;");

        return menuBar;
    }


}