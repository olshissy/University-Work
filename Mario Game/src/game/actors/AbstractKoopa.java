package game.actors;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.Status;
import game.actions.AttackAction;
import game.behaviours.AttackBehaviour;
import game.behaviours.Behaviour;
import game.behaviours.FollowBehaviour;
import game.behaviours.WanderBehaviour;
import game.reset.Resettable;

import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

/**
 * Abstract class representing the base koopa
 */
public abstract class AbstractKoopa extends Enemy implements Resettable, SpeechCapable {
    private final Map<Integer, Behaviour> behaviours = new TreeMap<>(); // priority, behaviour
    private GameMap map;
    private boolean resetGame = false;
    private int age = 1;
    /**
     * Constructor.
     *
     * @param name        the name of the Actor
     * @param displayChar the character that will represent the Actor in the display
     * @param hitPoints   the Actor's starting hit points
     */
    public AbstractKoopa(String name, char displayChar, int hitPoints) {
        super(name, displayChar, hitPoints);
        this.behaviours.put(3, new WanderBehaviour());
        this.addCapability(Status.HAS_SHELL);
        this.registerInstance();
    }

    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {

        ActionList actions = new ActionList();
        // it can be attacked only by the HOSTILE opponent, and this action will not attack the HOSTILE enemy back.
        if (otherActor.hasCapability(Status.HOSTILE_TO_ENEMY)) {
            actions.add(new AttackAction(this, direction));
        }
        this.behaviours.put(2, new FollowBehaviour(otherActor));
        this.behaviours.put(1, new AttackBehaviour());
        return actions;
    }

    /**
     * Figure out what to do next.
     *
     * @see Actor#playTurn(ActionList, Action, GameMap, Display)
     */
    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        if (this.age % 2 == 0){
            System.out.println("Koopa: \"" + this.speak() + "\"");
        }
        age++;

        this.map = map;
        if (!this.isConscious()) {
            behaviours.clear();
            dormantBehaviour(this, map);
        }else if(resetGame){
            map.removeActor(this);
        }
        else {
            for (Behaviour Behaviour : behaviours.values()) {
                Action action = Behaviour.getAction(this, map);
                if (action != null)
                    return action;
            }
        }
        return new DoNothingAction();
    }

    public void dormantBehaviour(Actor actor, GameMap map){
        this.setDisplayChar('D');
        this.removeCapability(Status.HOSTILE_TO_ENEMY);
        this.removeCapability(Status.HAS_SHELL);
        this.addCapability(Status.DORMANT);
    }

    @Override
    public IntrinsicWeapon getIntrinsicWeapon() { return new IntrinsicWeapon(30, "punches");}

    @Override
    public void resetInstance() {
        resetGame = true;
    }

    @Override
    public String speak() {
        Random rand = new Random();
        int randValue = rand.nextInt(2);
        String line;
        if(randValue == 0){
            line = "Never gonna make you cry!";
        } else{
            line = "Koopi koopi koopii~!";
        }
        return line;
    }
}
