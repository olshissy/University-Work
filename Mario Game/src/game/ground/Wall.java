package game.ground;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.actions.JumpAction;

import java.util.List;

/**
 * A wall
 */
public class Wall extends Ground implements Jumpable {
	private static final int SUCCESS_RATE = 80;
	private static final int FALL_DAMAGE = 20;

	/**
	 * Constructor
	 */
	public Wall() {
		super('#');
		this.addCapability(Status.HIGH_GROUND);
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
	public boolean canActorEnter(Actor actor) {
		return false;
	}
	
	@Override
	public boolean blocksThrownObjects() {
		return true;
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
