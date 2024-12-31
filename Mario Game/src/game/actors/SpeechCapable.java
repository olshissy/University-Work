package game.actors;

/**
 * Interface that represents actors who can speak
 */
public interface SpeechCapable {
    /**
     * Allows the actor to speak
     * @return the line the player says
     */
    public String speak();
}
