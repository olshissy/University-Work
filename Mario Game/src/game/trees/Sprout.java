package game.trees;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.actions.JumpAction;
import game.ground.Jumpable;
import game.items.FireFlower;
import game.reset.Resettable;
import game.Status;
import game.Utils;
import game.actors.Goomba;
import game.ground.Dirt;

/**
 * The youngest version of the tree
 */
public class Sprout extends Tree implements Jumpable, Resettable {
    private int sproutAge;
    private static final int SUCCESS_RATE = 90;
    private static final int FALL_DAMAGE = 10;
    private Location location;
    private int resetGame;


    /**
     * Constructor
     */
    public Sprout(){
        super();
        setAge(0);
        this.addCapability(Status.HIGH_GROUND);
        this.registerInstance();

    }


    /**
     * A boolean setter for the age
     * @param sproutAge the age of the sprout
     * @return a boolean value checking whether the age is correct
     */
    public boolean setAge(int sproutAge){
        boolean res = false;
        if (sproutAge >= 0){
            this.sproutAge = sproutAge;
            res = true;
        }
        return res;
        
    }

    @Override
    //what happens every tick, it runs this for every tick
    public void tick(Location location) { //found at this location
        sproutAge++;
        this.spawn(location);
        this.location = location;
        //change form
        if(sproutAge == 10){
            if(Utils.rollChance()>=50){
                location.addItem(new FireFlower());
            }
            location.setGround(new Sapling());
        }

        if(resetGame == 1){
            if(Utils.rollChance() >= 50) {
                location.setGround(new Dirt());
                this.resetGame++;
            }
        }



    }

    /**
     * Randomly spawns a goomba at a 10% chance
     * @param location
     */
    public void spawn(Location location){
        int randVal = Utils.rollChance();
        if (randVal <= 10){
            if(!location.containsAnActor()){
           location.addActor(new Goomba());}
        }
    }

    @Override
    public int getSuccessRate() {
        return this.SUCCESS_RATE;
    }

    @Override
    public int getFallDamage(){
        return this.FALL_DAMAGE;
    }


    @Override
    public void resetInstance() {
        this.resetGame = 1;
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
