package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;

/**
 * Represents a magical item that can be consumed by a player to get it's abilities
 */
public class SuperMushroom extends Item implements Consumables, TradeableItem {
   // private Action consumeSuperMushroom = new ConsumeAction(this);
    /**
     * Constructor
     */
    public SuperMushroom() {
        super("Super Mushroom", '^', true);
        this.addCapability(Status.MUSHROOM);
        this.addItemToInventory();
    }

    @Override
    public String getEffects(Actor actor, GameMap map) {
        if (!actor.getInventory().contains(this)){
            actor.addItemToInventory(this);
        }

        this.togglePortability();

        map.locationOf(actor).removeItem(this);
        actor.removeItemFromInventory(this);
        actor.increaseMaxHp(50);

        return "Mario is now under the effects of a Super Mushroom";
    }

    @Override
    public int getPrice(){return 400;}
}
