package game.items;

import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Location;
import game.actions.PickUpCoinAction;
import game.reset.Resettable;

/**
 * In game currency
 */
public class Coin extends Item implements Resettable {
    private int value;
    private Location coinLocation;

    /**
     * Constructor
     * @param value the value the coin adds to the users wallet
     */
    public Coin(int value, Location location) {
        super("Coin", '$', false);
        this.value = value;
        this.addAction(new PickUpCoinAction(this));
        this.registerInstance();
        this.coinLocation = location;
    }

    /**
     * Returns the coins value
     * @return the value of the coin
     */
    public int getValue(){
        return this.value;
    }

    @Override
    public void resetInstance() {
        coinLocation.removeItem(this);
    }
}
