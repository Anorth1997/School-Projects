package farmyard;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

import java.util.ArrayList;

/** A Human */
public class Human extends Species {

  private ArrayList<Egg> myBasket = new ArrayList<Egg>();

  private GraphicsContext g;

  /** Constructs a new Human. */
  public Human(int x, int y) {
    super("ziyao", Color.MEDIUMPURPLE);
    setLocation(x, y);
  }

  /** Causes human to drop down 4 piece s of food all around. */
  protected void dropFood() {
    FarmManager.food.add(new AnimalFood(x - 1, y - 1));
    FarmManager.food.add(new AnimalFood(x - 1, y + 1));
    FarmManager.food.add(new AnimalFood(x + 1, y - 1));
    FarmManager.food.add(new AnimalFood(x + 1, y + 1));
  }

  /**
   * Draws the given string in the given graphics context at at the given cursor location.
   *
   * @param g the graphics context in which to draw the string.
   * @param s the string to draw.
   * @param x the x-coordinate of the string's cursor location.
   * @param y the y-coordinate of the string's cursor location.
   */
  void drawString(GraphicsContext g, String s, int x, int y) {
    g.fillText(s, x * 10, y * 6);
    g.fillText("Eggs: " + myBasket.size(), 2 * 10, 2 * 6);
  }

  /**
   * Draws this farm pen item.
   *
   * @param g the graphics context in which to draw this item.
   */
  public void draw(GraphicsContext g) {
    this.g = g;
    g.setFill(Color.SANDYBROWN.darker());
    drawString(g, appearance, x, y);
  }

  /** Causes this item to take its turn in the farm-pensimulation. */
  public void move() {

    if (target == null) {
      target = findTarget();
    }

    if (target != null) {
      // Am I on an egg?
      if (this.getX() == target.getX() && this.getY() == target.getY()) {

        this.myBasket.add((Egg) target);
        FarmManager.eggs.remove(target);
        target = null;
        if (myBasket.size() % 12 == 0) {

          g.fillText("Eggs: " + myBasket.size(), 1 * 10, 1 * 6);
        }

      } else {

        // move toward the egg
        if (this.getX() < target.getX()) {
          x += 1;
        } else if (this.getX() > target.getX()) {
          x -= 1;
        }
        if (this.getY() < target.getY()) {
          y += 1;
        } else if (this.getY() > target.getY()) {
          y -= 1;
        }
      }
    }
    // no egg to pick up, so randomly move.
    randomlyMove();

    // Figure out whether I should drop food.
    double d = Math.random();
    if (d < 0.05) {
      dropFood();
    }

    // Figure out whether I turn around.
    d = Math.random();
    if (d < 0.1) {
      turnAround();
    }
  }
}
