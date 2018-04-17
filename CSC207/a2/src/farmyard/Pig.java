package farmyard;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public class Pig extends Species{

  private boolean full;
  /** Constructs a new Pig.
   *
   *
   * */
  public Pig(int x, int y) {
    super(":(8)", Color.PINK.darker().darker().darker());
    setLocation(x, y);
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
    g.setFill(color);
    g.fillText(s, x * 10, y * 6);
  }

  /**
   * Draws this farm pen item.
   *
   * @param g the graphics context in which to draw this item.
   */
  public void draw(GraphicsContext g) {
    drawString(g, appearance, x, y);
  }


  /** Causes this item to take its turn in the farm-pen simulation. */

  public void move() {
    // find the food
    if (target == null) {
      target = findTarget();
    }
    // found the food to go for
    if (target != null) {
      // Am I on an food?
      if (this.getX() == target. getX() && this.getY() == target.getY()) {
        this.full = true;
        FarmManager.food.remove(target);
        target = null;
      }

      else {
        // move toward the food
        if (this.getX() < target.getX()) {
          x += 1;
        } else if (this.getX() > target.getX()){
          x -= 1;
        }
        if (this.getY() < target.getY()) {
          y += 1;
        } else if (this.getY() > target.getY()){
          y -= 1;
        }
      }
    }

    // no food to eat, so move randomly
    randomlyMove();

    // Sometimes we digest.
    double d = Math.random();
    if (d < 0.03 && full) {
      poop("*");
    }
  }

}
