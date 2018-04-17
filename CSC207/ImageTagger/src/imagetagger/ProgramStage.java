package imagetagger;

import javafx.stage.Stage;

/**
 * Program the stage.
 */
class ProgramStage {

    /**
     * The main stage.
     */
    private static Stage primaryStage = new Stage();

    /**
     * The Home scene.
     */
    private HomeScene mainScene = new HomeScene();

    /**
     * The customized scene.
     */
    private CustomizeScene customizeScene = new CustomizeScene();

    /**
     * The Image Tagging Scene.
     */
    private ImageTagScene imageTagScene = new ImageTagScene();

    /**
     * The Naming History Scene
     */
    private NameHistoryScene nameHistoryScene = new NameHistoryScene();

    /**
     * The Master Tag list Scene/
     */
    private MasterTagListScene masterTagListScene = new MasterTagListScene();

    /**
     * Instantiates a new Program stage.
     */
    ProgramStage(){}

    /**
     * Display the main window of the application.
     */
    void display(){

        setScenes();
        primaryStage.setTitle( "Image Tagger" );
        primaryStage.setScene( HomeScene.getScene() );
        primaryStage.setResizable( false );

        //show the window
        primaryStage.show();
    }

    /**
     * Get stage to run the JavaFX application.
     *
     * @return the stage
     */
    static Stage getStage(){
        return primaryStage;
    }

    /**
     * Loads all the scenes in the application.
     */
    private void setScenes(){
        customizeScene.setCustomizeScene();
        mainScene.setMainScene();
        imageTagScene.setImageTagScene();
        nameHistoryScene.setNameHistoryScene();
        masterTagListScene.setMasterTagListScene();
    }

}
