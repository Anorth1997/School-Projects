package farmyard;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public abstract class Species extends FarmObject {

  protected NonLiving target;

  /** Indicates whether this living thing is moving right. */
  protected boolean goingRight;

  /** Construct a new Species */
  public Species(String appearance, Color color) {
    super(appearance, color);
    this.goingRight = true;
    this.target = null;
  }

  /** Build and initialize this human's forward and backward appearances. */
  private String reverseAppearance() {
    String reverse = "";
    for (int i = appearance.length() - 1; i >= 0; i--) {
      switch (appearance.charAt(i)) {
        case ')':
          reverse += '(';
          break;
        case '(':
          reverse += ')';
          break;
        case '>':
          reverse += '<';
          break;
        case '<':
          reverse += '>';
          break;
        case '}':
          reverse += '{';
          break;
        case '{':
          reverse += '}';
          break;
        case '[':
          reverse += ']';
          break;
        case ']':
          reverse += '[';
          break;
        default:
          reverse += appearance.charAt(i);
          break;
      }
    }

    return reverse;
  }

  /** Turns this Species around, causing it to reverse direction. */
  protected void turnAround() {
    goingRight = !goingRight;
    appearance = reverseAppearance();
  }

  /** Let this animal poop */
  protected void poop(String poopAppearance) {
    FarmManager.poop.add(new AnimalManure(poopAppearance, getX(), getY()));
  }

  /** Let this Species randomly moves without any purpose. */
  protected void randomlyMove() {
    if (goingRight) {
      // Figure out whether to move up or down, or neither.
      double d = Math.random();
      if (d < 0.1) {
        y += 1;
      } else if (d < 0.2) {
        y -= 1;
      }
    } else {
      // Figure out whether to move right or left, or neither.
      double d = Math.random();
      if (d < 0.1) {
        x += 1;
      } else if (d < 0.2) {
        x -= 1;
      }
    }
  }

  /**
   *
   * @return The Target that this Specie is looking for.
   */
  protected NonLiving findTarget() {
    // if this is a human, his target is egg.
    if (this instanceof Human) {
      for (int i = 0; i < FarmManager.eggs.size(); i++) {
        return FarmManager.eggs.get(i);
      }
      return null;
    }
    // if this is a PoopCollector, his target is AnimalManure.
      if (this instanceof PoopCollector) {
          for (int i = 0; i < FarmManager.poop.size(); i++) {
              return FarmManager.poop.get(i);
          }
          return null;
      }
    // if this is a pig or chicken, its target is food.
    else if (this instanceof Pig || this instanceof Chicken) {
      for (int i = 0; i < FarmManager.food.size(); i++) {
        return FarmManager.food.get(i);
      }
      return null;
    }
    return null;
  }
}
