package farmyard;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

/** An egg that a farmer collects. */
public class Egg extends NonLiving{

  /**
   *
   * @param x the x coordinate for the Egg.
   * @param y the y coordinate for the Egg.
   */

  public Egg(int x, int y) {
    super("o", Color.ROSYBROWN.darker().darker().darker());
    setLocation(x, y);
  }

  /**
   * Draws this farm pen item.
   *
   * @param g the graphics context in which to draw this item.
   */
  public void draw(GraphicsContext g) {
    g.setFill(Color.ROSYBROWN);
    g.fillText(String.valueOf(appearance), x * 10, y * 6);
  }

}
