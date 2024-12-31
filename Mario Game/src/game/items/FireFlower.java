package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;

/**
 * A special item that can be consumed to get it's effects
 */
public class FireFlower extends Item implements Consumables{
    private int turns = 0;

    /**
     * Constructor
     */
    public FireFlower() {
        super("Fire Flower", 'f', true);
        this.addCapability(Status.FIRE);
    }

    @Override
    public String getEffects(Actor actor, GameMap map) {
        if (!actor.getInventory().contains(this)) {
            actor.addItemToInventory(this);
            turns = 0;
        }
        this.togglePortability();
        map.locationOf(actor).removeItem(this);
        return "Mario is now under the effects of a Fire Flower!";
    }

    @Override
    public void tick(Location location, Actor actor){
        if (turns>=20){
            actor.removeItemFromInventory(this);
            actor.removeCapability(Status.FIRE);
        } else if (actor.getInventory().contains(this)) {
            System.out.println("The Fire effect will last for " + (20-turns) + " turn/s.");
        } turns++;
    }
}
