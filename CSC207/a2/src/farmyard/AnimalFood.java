package farmyard;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

/** Animal Food */
public class AnimalFood extends NonLiving{

  /**
   * Constructs a new bubble at the specified cursor location (x, y).
   *
   * @param x the x co-ordinate of the food's cursor location.
   * @param y the y co-ordinate of the food's cursor location.
   */
  public AnimalFood(int x, int y) {
    super("%", Color.GRAY.darker().darker().darker());
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

  /**
   * Causes this item to take its turn in the farm-pen simulation, blown due to strong winds. Up in
   * this case
   */

  public void blown(int xdir, int ydir) {
    // blown Right or Left
    if (xdir == 1) {
      x++;
    } else if (xdir == -1) {
      x--;
    }

    // blown Up or Down.
    if (ydir == 1) {
      y++;
    } else if (ydir == -1) {
      y--;
    }
  }
}
