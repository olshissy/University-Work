package game.trees;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.Location;
import game.*;
import game.actions.JumpAction;
import game.actors.FlyingKoopa;
import game.actors.Koopa;
import game.ground.Dirt;
import game.ground.Jumpable;
import game.reset.Resettable;

import java.util.List;
import java.util.Random;

/**
 * The oldest form of tree
 */
public class Mature extends Tree implements Jumpable, Resettable {
    private int matureAge;
    private static final int SUCCESS_RATE = 70;
    private static final int FALL_DAMAGE = 30;
    private Location location;

    /**
     * Constructor
     */
    public Mature() {
        super.setDisplayChar('T');
        setAge(0);
        this.addCapability(Status.HIGH_GROUND);

    }

    @Override
    public boolean setAge(int age) {
        boolean res = false;
        if (age > 0) {
            matureAge = age;
            res = true;
        }
        return res;
    }

    @Override
    public void tick(Location location) {
        this.location = location;
        this.spawn(location);
        matureAge++;

        if (Utils.rollChance() <= 20) {
            location.setGround(new Dirt());
        }

        if (this.matureAge % 5 == 0){
            growNew(location);
        }
    }

    /**
     * Spawns a Koopa at a 15% chance
     * @param location location of the mature
     */
    public void spawn(Location location) {
        int randVal = Utils.rollChance();
        int secondVal = Utils.rollChance();
        if (randVal <= 15) {
            if(!location.containsAnActor()){
                if(secondVal<=50){
                location.addActor(new Koopa());
                } else {
                    location.addActor(new FlyingKoopa());
                }
            }
        }
    }

    /**
     * Spawns a sprout in a random location around the mature every 5 turns
     * @param location location of the mature
     */
    public void growNew(Location location){
        List<Exit> exitList;
        exitList = location.getExits();
        Random r = new Random();
        boolean isPlanted = false;
        int counter = 0;

        while (isPlanted == false && counter < exitList.size()){
            int randint = r.nextInt(exitList.size() - 1);
            Exit newPlantingGround = exitList.get(randint);
            if(newPlantingGround.getDestination().getGround().hasCapability(Status.FERTILE)){
                newPlantingGround.getDestination().setGround(new Sprout());
                isPlanted = true;
            }
            counter++;}

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
