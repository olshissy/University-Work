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
import game.items.Key;
import game.reset.Resettable;

import java.util.*;

/**
 * Final boss character
 */
public class Bowser extends Enemy implements Resettable, SpeechCapable {
    private final Map<Integer, Behaviour> behaviours = new TreeMap<>(); // priority, behaviour
    private GameMap map;
    private int age = 1;
    private boolean resetGame;

    /**
     * Constructor.
     */
    public Bowser() {
        super("Bowser", 'B', 500);
        this.addItemToInventory(new Key());
        this.registerInstance();
        this.addCapability(Status.FIRE);
        resetGame = false;
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
        //this.behaviours.put(2, new FollowBehaviour(otherActor));
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
            System.out.println("Bowser: \"" + this.speak() + "\"");
        }
        age++;

        this.map = map;
        if(resetGame){
            map.removeActor(this);
            //add new bowser to the map
            Application.secondaryMap.at(70,8).addActor(this);

        }
        for(Behaviour Behaviour : behaviours.values()) {
            Action action = Behaviour.getAction(this, map);
            if (action != null)
                return action;
        }

        return new DoNothingAction();
    }

    @Override
    public IntrinsicWeapon getIntrinsicWeapon() { return new IntrinsicWeapon(80, "punches");}

    @Override
    public void resetInstance() {
        resetGame = true;

    }

    @Override
    public String speak() {
        Random rand = new Random();
        int randValue = rand.nextInt(4);
        String line;

        if(randValue == 0){
            line = "What was that sound? Oh, just a fire.";
        }
        else if(randValue == 1){
            line = "Princess Peach! You are formally invited... to the creation of my new kingdom!";
        }
        else if(randValue == 2){
            line = "Never gonna let you down!";
        } else{
            line = "Wrrrrrrrrrrrrrrrryyyyyyyyyyyyyy!!!!";
        }
        return line;
    }
}
