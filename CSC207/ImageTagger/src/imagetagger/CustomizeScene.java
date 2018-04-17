package imagetagger;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;

import java.io.File;

/**
 *
 */
class CustomizeScene {

    /**
     * A controller for the Main Window.
     */
    private MainWindowController controller = MainWindowController.getInstance();

    /**
     * The tree of strings.
     */
    static TreeItem<String> root = new TreeItem<>();

    /**
     * The Tree view to view the TreeItem root.
     */
    static TreeView<String> treeView = new TreeView<>(root);

    /**
     * The Image View to view images.
     */
    static ImageView imageView = new ImageView();

    /**
     * A text filed to display text.
     */
    private static TextField textField = new TextField();

    /**
     * The scene to customize.
     */
    private static Scene customizeScene;

    /**
     * The set of all buttons.
     */
    private ApplicationButtons appButtons = new ApplicationButtons();


    /**
     * Constructor for the CustomizeScene class
     */
    CustomizeScene(){}

    /**
     * Sets up scene.
     */
    void setCustomizeScene(){

        treeViewEvents();
        BorderPane borderPane = layout();

        customizeScene = new Scene(borderPane, 1000, 730);
        borderPane.prefHeightProperty().bind(customizeScene.heightProperty());
        borderPane.prefWidthProperty().bind(customizeScene.widthProperty());
    }

    /**
     * Returns the customized scene.
     *
     * @return the scene
     */
    static Scene getCustomizeScene(){
        return customizeScene;
    }

    /**
     * Returns the pane for the scene.
     *
     * @return the pane for the scene
     */
    private BorderPane layout(){
        BorderPane border = new BorderPane();
        // Adding Menu bar
        MenuBar top = topMenu();
        VBox left = leftMenu();
        GridPane center = center();


        border.setTop(top);

        border.setCenter(center);
        border.setLeft(left);
        border.setBottom(bottomMenu());
        border.setPadding( new Insets( 0,0,20,0 ) );

        File file = new File(System.getProperty("user.dir") + File.separator + "WelcomeScene.jpg");
        Image image = new Image(file.toURI().toString());
        BackgroundImage myBI= new BackgroundImage(image,
                BackgroundRepeat.NO_REPEAT, BackgroundRepeat.NO_REPEAT, BackgroundPosition.DEFAULT,
                BackgroundSize.DEFAULT);
        border.setBackground(new Background(myBI));

        border.setPrefSize( 666,1000 );

        return border;
    }

    /**
     * Return the VBox representing the left menu of the BorderPane.
     *
     * @return the VBox that represents the left menu of our the layout
     */
    private VBox leftMenu(){
        VBox vBox = new VBox(15);
        vBox.setPrefWidth( 300 );

        getTreeView();
        treeView.setMaxHeight( vBox.getPrefHeight() );

        Button toggleButton = appButtons.toggleViewButton();
        toggleButton.setMinWidth( 200 );

        Button searchFileButton = appButtons.searchFileButton();
        searchFileButton.setMinWidth( 200 );

        Button homeButton = appButtons.homeButton();
        homeButton.setMinWidth(200);

        Button moveToButton = appButtons.moveToButton();
        moveToButton.setMinWidth(200);

        Button showFilesContainsTag = appButtons.showFilesContainsTag();
        showFilesContainsTag.setMinWidth(200);

        vBox.setMaxHeight( 666 );
        vBox.getChildren().addAll(treeView , toggleButton, searchFileButton, homeButton, moveToButton,
                showFilesContainsTag);
        vBox.setAlignment( Pos.TOP_CENTER );
        vBox.setStyle("-fx-background-color: TransParent;");
        treeView.setStyle("-fx-background-color: TransParent;");

        return vBox;
    }

    /**
     * Return the HBox representing the bottom menu of the BorderPane.
     *
     * @return the HBox that represents the bottom menu of our the layout
     */
    private HBox bottomMenu(){
        HBox hBox = new HBox();
        hBox.setSpacing( 50 );
        hBox.getChildren().addAll( );
        hBox.setAlignment( Pos.CENTER );

        return hBox;
    }

    /**
     * Returns the GridPane containing the TextField, and the Tag buttons.
     *
     * @return the GridPane for the user interface
     */
    private GridPane center(){

        GridPane gridPane = new GridPane();

        getTextField();
        Button tagImageButton = appButtons.tagButton();
        Button imageTagsButton = appButtons.imageTagsButton();
        Button revertNameButton = appButtons.revertNameButton();
        tagImageButton.setMinWidth( 150 );
        StackPane stackPane = stackPane();

        gridPane.setPadding( new Insets( 10,20,20,20 ) );

        //First Row with column and row index 0.
        gridPane.getChildren().addAll(stackPane) ;
        GridPane.setConstraints( stackPane, 0, 0 );
        gridPane.setMaxSize( 700, 650 );

        //Second Row with column index 0 and row index 1.
        HBox secondRow = new HBox(tagImageButton, textField, imageTagsButton, revertNameButton);
        secondRow.setAlignment( Pos.CENTER );
        secondRow.setSpacing( 10 );
        gridPane.addRow(2, secondRow);

        gridPane.setVgap(5);

        return gridPane;
    }

    /**
     * Returns the StackPane containing ImageView.
     *
     * @return the StackPane for the user interface
     */
    private StackPane stackPane(){
        StackPane stackPane = new StackPane();
        stackPane.getChildren().add(imageView);
        imageView.setFitWidth( 600 );
        imageView.setFitHeight( 400 );
        stackPane.setMaxSize( 600, 400 );
        stackPane.setPrefSize( 600,400 );
        stackPane.setPadding( new Insets( 10,10,10,10 ) );


        File file = new File(System.getProperty("user.dir") + File.separator + "ViewImage.jpg");
        Image image = new Image(file.toURI().toString());
        stackPane.setPrefSize( 666,1000 );
        BackgroundImage myBI= new BackgroundImage(image,
                BackgroundRepeat.NO_REPEAT, BackgroundRepeat.NO_REPEAT, BackgroundPosition.DEFAULT,
                BackgroundSize.DEFAULT);
        stackPane.setBackground(new Background(myBI));

        return stackPane;
    }

    /**
     * Builds and returns the top menu of our BorderPane.
     *
     * @return the top menu of our layout
     */
    private MenuBar topMenu() {

        MenuBar menuBar = new MenuBar();
        menuBar.setPrefWidth( 600 );

        // Defining Menu
        Menu fileMenu = new Menu( "File" );
        Menu helpMenu = new Menu( "Help" );
        menuBar.setStyle("-fx-background-color: TransParent;");
        menuBar.getMenus().addAll( fileMenu, helpMenu );
        return menuBar;
    }

    /**
     * Builds and returns a TreeView to show the images files to be customized.
     *
     * @return TreeView with the directory and image files.
     */
    private TreeView<String> getTreeView() {

        root.setExpanded( true );
        treeView.setMinHeight( 450 );
        treeView.setStyle("-fx-background-color: transParent;");

        return treeView;
    }

    /**
     * Sets the default text and width to text field.
     */
    private void getTextField(){
        textField.setPromptText("Enter Tag");
        textField.setMaxWidth( 200 );
    }

    /**
     * Returns the text from the tag text field in the user interface.
     *
     * @return the string tag name.
     */
    static String getTag(){
        return textField.getText();
     }

    /**
     * Sets the tree view event for the mouse click.
     */
    private void treeViewEvents(){
        treeView.setOnMouseClicked(e -> controller.selectedImage() );
    }

}
