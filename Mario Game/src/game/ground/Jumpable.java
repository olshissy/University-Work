package game.ground;

/**
 * Represents any ground that the player can jump to
 */
public interface Jumpable {

    /**
     * @return the damage done to the player if the jump is unsuccessful
     */
    int getFallDamage();

    /**
     * @return how often the jump will successful
     */
    int getSuccessRate();

}
