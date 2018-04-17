package farmyard;

import javafx.scene.paint.Color;

public abstract class FarmObject {
  /** How this lovely FarmObject appears on the screen. */
  protected String appearance;

  /** This FarmObject's horizontal coordinates. */
  protected int x;

  /** This FarmObject's vertical coordinates. */
  protected int y;

  /** The color of this FarmObject which will be demonstrated on the simulator screen. */
  protected Color color;

  /** Construct a new FarmObject */
  public FarmObject(String appearance, Color color) {
    this.appearance = appearance;
    this.color = color;
  }

  /**
   * Set this FarmObject's location.
   *
   * @param x the first coordinate.
   * @param y the second coordinate.
   */
  public void setLocation(int x, int y) {
    // set x to a
    this.x = x;
    // set y to b
    this.y = y;
  }

  /**
   *
   * @return this object's x coordinate
   */
  public int getX() {
    return x;
  }

  /**
   *
   * @return this object's y coordinate
   */
  public int getY() {
    return y;
  }
}
