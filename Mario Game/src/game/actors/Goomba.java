package game.actors;


import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.*;
import game.actions.AttackAction;
import game.behaviours.AttackBehaviour;
import game.behaviours.Behaviour;
import game.behaviours.FollowBehaviour;
import game.behaviours.WanderBehaviour;
import game.reset.Resettable;

import java.util.*;

/**
 * A little fungus guy.
 */
public class Goomba extends Enemy implements Resettable, SpeechCapable {
	private final Map<Integer, Behaviour> behaviours = new TreeMap<>(); // priority, behaviour
	private GameMap map;
	private boolean resetGame = false;
	private int age = 1;

	/**
	 * Constructor.
	 */
	public Goomba() {
		super("Goomba", 'g', 20);
		this.behaviours.put(3, new WanderBehaviour());
		this.registerInstance();
	}

	/**
	 * Creates a list possible actions of the Goomba
	 * @param otherActor the Actor that might perform an action.
	 * @param direction  String representing the direction of the other Actor
	 * @param map        current GameMap
	 * @return list of actions
	 * @see Status#HOSTILE_TO_ENEMY
	 */
	@Override
	public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {

		ActionList actions = new ActionList();
		// it can be attacked only by the HOSTILE opponent, and this action will not attack the HOSTILE enemy back.
		if(otherActor.hasCapability(Status.HOSTILE_TO_ENEMY)) {
			actions.add(new AttackAction(this,direction));
		}
		this.behaviours.put(2, new FollowBehaviour(otherActor));
		this.behaviours.put(1, new AttackBehaviour());
		return actions;
	}

	/**
	 * Figure out what to do next.
	 * @see Actor#playTurn(ActionList, Action, GameMap, Display)
	 */
	@Override
	public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
		if(this.age % 2 == 0){
			System.out.println("Goomba: \"" + this.speak() + "\"");
		}
		age++;

		this.map = map;
		if (Utils.rollChance() <= 10){
			map.removeActor(this);
		} else if(resetGame){
			map.removeActor(this);
		}
		else{
			for(Behaviour Behaviour : behaviours.values()) {
				Action action = Behaviour.getAction(this, map);
				if (action != null)
					return action;
			}
		}

		return new DoNothingAction();
	}

	@Override
	public IntrinsicWeapon getIntrinsicWeapon() { return new IntrinsicWeapon(10, "kicks");}

	@Override
	public void resetInstance() {
		resetGame = true;
	}

	@Override
	public String speak() {
		Random rand = new Random();
		int randValue = rand.nextInt(3);
		String line;

		if(randValue == 0){
			line = "Mugga mugga!";
		}
		else if(randValue == 1){
			line = "Ugha ugha... (Never gonna run around and desert you...)";
		} else{
			line = "Ooga-Chaka Ooga-Ooga!";
		}
		return line;
	}
}
