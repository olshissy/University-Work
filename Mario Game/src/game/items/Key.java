package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.items.PickUpItemAction;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;

/**
 * Key dropped by bowser to release peach
 */
public class Key extends Item {
    public Key() {
        super("Key", 'k', true);
        this.addCapability(Status.HAS_KEY);
    }
}
