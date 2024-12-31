package game.trees;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.*;
import game.actions.JumpAction;
import game.ground.Dirt;
import game.ground.Jumpable;
import game.items.Coin;
import game.items.FireFlower;
import game.reset.Resettable;

/**
 * The second stage in the growth of tree
 */
public class Sapling extends Tree implements Jumpable, Resettable {
    private int saplingAge;
    private static final int SUCCESS_RATE = 80;
    private static final int FALL_DAMAGE = 20;
    private Location location;

    /**
     * Constructor
     */
    public Sapling(){
        super.setDisplayChar('t');
        setAge(0);
        this.addCapability(Status.HIGH_GROUND);
        this.registerInstance();
    }

    /**
     * A boolean setter to check the age
     * @param saplingAge the age of sapling
     * @return a boolean value to check is age is correct
     */
    public boolean setAge(int saplingAge){
        boolean res = false;
        if (saplingAge >= 0){
            this.saplingAge = saplingAge;
            res = true;
        }
        return res;

    }


    @Override
    public void tick(Location location) {
        this.location = location;
        saplingAge++;
        this.spawn(location);
        if(saplingAge == 10){
            if(Utils.rollChance()>=50){
                location.addItem(new FireFlower());
            }
            location.setGround(new Mature());
        }

    }

    /**
     * Spawns a coin on the tree at a 10% chance
     * @param location location of the sapling
     */
    public void spawn(Location location){
        int randVal = Utils.rollChance();
        if (randVal <= 10){
            location.addItem(new Coin(20, location));
        }

    }

    /**
     * @return the success rate of the jump
     */
    public int getSuccessRate() {
        return this.SUCCESS_RATE;
    }

    /**
     * @return the fall damage if jump is unsuccessful
     */
    public int getFallDamage(){
        return this.FALL_DAMAGE;
    }

    @Override
    public void resetInstance() {
        if(Utils.rollChance() >= 50) {
            location.setGround(new Dirt());
        }
    }

    /**
     * Adds the available actions to a list
     * @param otherActor the actor that might be performing the action
     * @param direction String representing the direction of the other actor
     * @param location
     * @return the action list
     */
    @Override
    public ActionList allowableActions(Actor otherActor, Location location, String direction){
        ActionList actions = new ActionList();
        if(otherActor.hasCapability(Status.CAN_FLY) && !location.containsAnActor()){
            actions.add(new MoveActorAction(location, direction));
        } else if(!location.containsAnActor()){
            actions.add(new JumpAction(this, direction, location));
        }
        return actions;
    }

}
