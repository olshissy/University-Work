package game.items;

import edu.monash.fit2099.engine.weapons.WeaponItem;

/**
 * A wrench to be used as a weapon
 */
public class Wrench extends WeaponItem implements TradeableItem {
    /**
     * Constructor
     */
    public Wrench() {
        super("Wrench", 'w', 50, "whacks", 80);
        this.addItemToInventory();
    }

    @Override
    public int getPrice(){return 200;}
}
