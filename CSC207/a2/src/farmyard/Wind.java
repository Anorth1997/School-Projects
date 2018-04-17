package farmyard;

/** If the iwnd was last blowing up then it is likely to keep blowing up. Same for left/right. */
public class Wind {

  // Which way was the windod last blowing up or down?
  private static int lastUp = 0;

  // Which way was the windod last blowing left or right?
  private static int lastRight = 0;

  /**
   *
   * The wind keep blowing the same direction in 30% of the time; turn to the opposite direction in 10% of the time;
   * and 60% of the time stops in up or down direction. If the wind is not blowing, it keeps still in 50% of the time,
   * and 25% of the time to blow in one direction and 25% of the time to blow in the other direction.
   *
   * @param direction The direction of wind at this moment of time.
   *
   * @return 1 or -1 or 1 which represents the same direction, opposite direction and stop, respectively.
   */

  public static int windRule(int direction) {
    if (direction != 0) {
      double chance = Math.random();
      if (chance >= 0 && chance < 0.3) {
        return direction;
      } else if (chance >= 0.3 && chance < 0.4) {
        direction = -direction;
        return direction;
      } else {
        direction = 0;
        return direction;
      }
    } else {
      double chance = Math.random();
      if (chance >= 0 && chance < 0.5) {
        return direction;
      } else if (chance >= 0.5 && chance < 0.75) {
        direction = 1;
        return direction;
      } else {
        direction = -1;
        return direction;
      }
    }
  }

  /**
   *
   * The method returns 1 if the wind is blowing up; returns -1 if the wind is blowing down; and returns 0 if the wind
   * isn't blowing in up or down direction.
   *
   * @return 1 or -1 or 0 which represent the direction of wind in up direction or down direction or neither,
   * respectively.
   */

  public static int windBlowingUp() {
    lastUp = windRule(lastUp);
    return lastUp;
  }


  /**
   *
   * The method returns 1 if the wind is blowing right; returns -1 if the wind if blowing left; and returns 0 if the
   * wind isn't blowing in up or down direction.
   *
   * @return 1 or -1 or 0 which represent the direction of wind in right direction or left direction or neither,
   * respectively.
   */
  public static int windBlowingRight() {
    lastRight = windRule(lastRight);
    return lastRight;
  }
}
