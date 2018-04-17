package farm_simulation;

import farmyard.*;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.stage.Stage;
import javafx.util.Duration;

/** Our take on the "classical" game Farm Ville */
public class Main extends Application {

  /** The width of a character. */
  public static final int charWidth = 6;
  /** The height of a character. */
  public static final int charHeight = 10;

  public static void main(String[] args) {
    launch(args);
  }

  @Override
  public void start(Stage primaryStage) {
    primaryStage.setTitle("FarmVille");

    Group root = new Group();
    Scene theScene = new Scene(root);
    primaryStage.setScene(theScene);
    Canvas canvas = new Canvas(1024, 720);
    root.getChildren().add(canvas);

    GraphicsContext gc = canvas.getGraphicsContext2D();

    // create instance of human and store it
    FarmManager.farmers.add(new Human(30, 30));

    // create instance of PoopCollector and store it
    FarmManager.collectors.add(new PoopCollector(30 , 40));

    // create instance of Chicken and store it.
    FarmManager.chickens.add(new Chicken(23, 18));
    FarmManager.chickens.add(new Chicken(6, 12));
    FarmManager.chickens.add(new Chicken(17, 4));
    FarmManager.chickens.add(new Chicken(15, 28));
    FarmManager.chickens.add(new Chicken(15, 36));

    // create instance of Pig and store it
    FarmManager.pigs.add(new Pig(10, 20));
    FarmManager.pigs.add(new Pig(20, 10));

    drawShapes(gc);

    Timeline gameLoop = new Timeline();
    gameLoop.setCycleCount(Timeline.INDEFINITE);
    final long timeStart = System.currentTimeMillis();

    KeyFrame kf =
        new KeyFrame(
            Duration.seconds(0.5),
            new EventHandler<ActionEvent>() {
              public void handle(ActionEvent ae) {
                double t = (System.currentTimeMillis() - timeStart) / 1000.0;
                // all PoopCollectors move.
                for (int e = 0; e < FarmManager.collectors.size(); e++) {
                  FarmManager.collectors.get(e).move();
                }

                // all human move
                for (int a = 0; a < FarmManager.farmers.size(); a++) {
                  FarmManager.farmers.get(a).move();
                }

                // all pigs move
                for (int b = 0; b < FarmManager.pigs.size(); b++) {
                  FarmManager.pigs.get(b).move();
                }

                // all chickens move
                for (int c = 0; c < FarmManager.chickens.size(); c++) {
                  FarmManager.chickens.get(c).move();
                }

                // the direction of wind at this moment.
                int xaixs = Wind.windBlowingRight();
                int yaixs = Wind.windBlowingUp();

                // all AnimalFood move due to the direction of wind.

                for (int d = 0; d < FarmManager.food.size(); d++) {
                  FarmManager.food.get(d).blown(xaixs, yaixs);
                }

                // Clear the canvas
                gc.clearRect(0, 0, 1024, 720);
                drawShapes(gc);
              }
            });

    gameLoop.getKeyFrames().add(kf);
    gameLoop.play();
    primaryStage.show();
  }

  private void drawShapes(GraphicsContext gc) {

    // draw all the human
    for (int a = 0; a < FarmManager.farmers.size(); a++) {
      FarmManager.farmers.get(a).draw(gc);
    }
    // draw all the PoopCollector
    for (int g = 0; g < FarmManager.collectors.size(); g++) {
      FarmManager.collectors.get(g).draw(gc);
    }

    // draw all the pigs
    for (int b = 0; b < FarmManager.pigs.size(); b++) {
      FarmManager.pigs.get(b).draw(gc);
    }

    // draw all the chickens
    for (int c = 0; c < FarmManager.chickens.size(); c++) {
      FarmManager.chickens.get(c).draw(gc);
    }

    // draw all the AnimalFoods
    for (int d = 0; d < FarmManager.food.size(); d++) {
      FarmManager.food.get(d).draw(gc);
    }

    // draw all the AnimalManure
    for (int e = 0; e < FarmManager.poop.size(); e++) {
      FarmManager.poop.get(e).draw(gc);
    }

    // draw all the Eggs
    for (int f = 0; f < FarmManager.eggs.size(); f++) {
      FarmManager.eggs.get(f).draw(gc);
    }
  }
}
