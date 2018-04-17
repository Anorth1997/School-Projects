package farmyard;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public class PoopCollector extends Species {
  public PoopCollector(int x, int y) {
    super("robot", Color.BLUE);
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
  public void move() {
      // find the poop
      if (target == null) {
          target = findTarget();
      }
      // found the poop to go for
      if (target != null) {

          // Am I on a poop?
          if (this.getX() == target. getX() && this.getY() == target.getY()) {
              FarmManager.poop.remove(target);
              target = null;
          }

          else {
              // move toward the poop
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

      // no poop to pick up, ran
      randomlyMove();


  }




}
