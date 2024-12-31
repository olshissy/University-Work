package game;

/**
 * Represents the money value the player has access to
 */
public class Wallet {
    private int value = 0;
    private static Wallet instance;

    /**
     * Gets a singleton instance of the class
     * @return the instance
     */
    public static Wallet getInstance(){
        if(instance == null){
            instance = new Wallet();
        }
        return instance;
    }

    /**
     * @return the money value the player has access to
     */
    public int getValue(){
        return this.value;
    }

    /**
     * Increases the player's wallet value
     * @param value the value to be increased by
     */
    public void increaseWalletValue(int value){
        this.value += value;
    }

    /**
     * Decreases the player's wallet value
     * @param value the value to be decreased by
     */
    public void decreaseWalletValue(int value){
        this.value -= value;
    }

}
