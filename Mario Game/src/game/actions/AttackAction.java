package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.weapons.Weapon;
import game.Status;
import game.ground.Fire;
import game.ground.Pipe;
import game.items.SuperMushroom;

import java.util.Random;

/**
 * Special Action for attacking other Actors.
 */
public class AttackAction extends Action {

	/**
	 * The Actor that is to be attacked
	 */
	protected Actor target;

	/**
	 * The direction of incoming attack.
	 */
	protected String direction;

	/**
	 * Random number generator
	 */
	protected Random rand = new Random();

	/**
	 * Constructor.
	 *
	 * @param target the Actor to attack
	 */
	public AttackAction(Actor target, String direction) {
		this.target = target;
		this.direction = direction;
	}


	@Override
	public String execute(Actor actor, GameMap map) {
		Weapon weapon = actor.getWeapon();
		int damage = weapon.damage();
		String result = actor + " " + weapon.verb() + " " + target + " for " + damage + " damage.";

		if (target.hasCapability(Status.STAR)){
			damage = 0;
		}

		if (actor.hasCapability(Status.STAR)){
			map.removeActor(target);
			result = "Target is instantly killed.";
		}

		if (!target.hasCapability(Status.DORMANT)){
			target.hurt(damage);}

		if (!(rand.nextInt(100) <= weapon.chanceToHit())) {
			return actor + " misses " + target + ".";
		}

		if(actor.hasCapability(Status.FIRE)){
			Location targetLoc = map.locationOf(target);
			Ground ground = map.locationOf(target).getGround();
			targetLoc.setGround(new Fire(ground));
		}




		if (!target.isConscious() && !target.hasCapability(Status.DORMANT)){
			ActionList dropActions = new ActionList();
			// drop all items
			for (Item item : target.getInventory())
				dropActions.add(item.getDropAction(actor));
			for (Action drop : dropActions)
				drop.execute(target, map);

			if(target.hasCapability(Status.PIRANHA)){
				map.removeActor(target);
				new DoNothingAction();
				return "Pipe open";
			}
			// remove actor
			if (!target.hasCapability(Status.HAS_SHELL)) {
				map.removeActor(target);
			}
			//}
			result += System.lineSeparator() + target + " is killed.";
		} else if (!target.isConscious() && target.hasCapability(Status.DORMANT) && weapon.toString().equals("Wrench")){
			ActionList dropActions = new ActionList();
			// drop all items
			target.addItemToInventory(new SuperMushroom());
			for (Item item : target.getInventory())
				dropActions.add(item.getDropAction(actor));
			for (Action drop : dropActions)
				drop.execute(target, map);
			result = actor + " breaks " + target + "'s shell.";
			map.removeActor(target);
		}

		char val = actor.getDisplayChar();
		if (Character.isUpperCase(val) && actor.hasCapability(Status.MUSHROOM)){
			actor.removeCapability(Status.MUSHROOM);}
		return result;
	}

	@Override
	public String menuDescription(Actor actor) {
		if (!target.isConscious() && target.hasCapability(Status.DORMANT) && actor.getWeapon().toString().equals("Wrench")){
			return actor + " destroys " + target + "'s shell at " + direction;
		} else if (actor.hasCapability(Status.FIRE)){
			return actor + " attacks " + target + " at " + direction + " with fire!";
		} return actor + " attacks " + target + " at " + direction;}
}