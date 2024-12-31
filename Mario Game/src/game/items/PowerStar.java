package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;

/**
 * A magical item that gives the player certain values
 */
public class PowerStar extends Item implements Consumables, TradeableItem {

    private int turns = 0;
    //private Action consumePowerStar = new ConsumeAction(this);

    /**
     * Constructor
     */
    public PowerStar(Actor actor) {
        super("Power Star", '*', true);
        this.addItemToInventory();
        this.addCapability(Status.STAR);
    }

    public PowerStar() {
        super("Power Star", '*', true);
        this.addItemToInventory();
        this.addCapability(Status.STAR);
    }

    @Override
    public String getEffects(Actor actor, GameMap map) {
        if (!actor.getInventory().contains(this))
            actor.addItemToInventory(this);

        this.togglePortability();

        map.locationOf(actor).removeItem(this);

        actor.removeItemFromInventory(this);

        actor.heal(200);

        return "Mario is now under the effects of a Power Star!";
    }

    @Override
    public void tick(Location location, Actor actor){
        if (turns>=10){
            actor.removeItemFromInventory(this);
            actor.removeCapability(Status.STAR);
        } else if (actor.getInventory().contains(this)) {
            System.out.println("The Power Star's effects will last for " + (10-turns) + " turn/s.");
        } turns++;
    }

    @Override
    public int getPrice(){return 600;}
}
