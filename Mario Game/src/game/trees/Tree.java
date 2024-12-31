package game.trees;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.actions.JumpAction;

/**
 * Abstract tree class for the forms of tree
 */
public abstract class Tree extends Ground {

    /**
     * abstract method grow
     */
    public abstract void tick(Location location);

    /**
     * Constructor
     */
    public Tree() {
        super('+');

    }

    abstract boolean setAge(int age);

    abstract void spawn(Location location);

    @Override
    public boolean canActorEnter(Actor actor) {
        return false;
    }


    /**
     * Adds the available actions to a list
     * @param otherActor the actor that might be performing the action
     * @param direction String representing the direction of the other actor
     * @param location
     * @return the action list
     */
    @Override
    public abstract ActionList allowableActions(Actor otherActor, Location location, String direction);
}



