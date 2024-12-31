package game.actors;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.displays.Menu;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.Wallet;
import game.actions.DrinkWaterAction;
import game.ground.Dirt;
import game.items.*;
import game.reset.ResetAction;
import game.reset.Resettable;
import game.Status;

/**
 * Class representing the Player.
 */
public class Player extends Actor  implements Resettable {
	private final Menu menu = new Menu();
	private boolean resetGame;
	private int damage = 5000;

	/**
	 * Constructor.
	 *
	 * @param name        Name to call the player in the UI
	 * @param displayChar Character to represent the player in the UI
	 * @param hitPoints   Player's starting number of hitpoints
	 */
	public Player(String name, char displayChar, int hitPoints) {
		super(name, displayChar, hitPoints);
		this.addCapability(Status.HOSTILE_TO_ENEMY);
		this.addCapability(Status.CAN_TRADE);
		this.addCapability(Status.CAN_SPEAK);
		this.addCapability(Status.CAN_ENTER);
		addItemToInventory(Bottle.getInstance());
		this.registerInstance();

	}



	@Override
	public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
		Location location = map.locationOf(this);

		if(!this.isConscious()){
			char replacementChar = location.getGround().getDisplayChar();
			this.setDisplayChar(replacementChar);
			map.removeActor(this);
			return new DoNothingAction();
		}

		for (int i = 0; i<this.getInventory().size(); i++){
			if (this.getInventory().get(i).hasCapability(Status.FIRE)){
				this.addCapability(Status.FIRE);
				System.out.println("Mario is now under the effects of a Fire Flower!");
			} else if(this.getInventory().get(i).hasCapability(Status.STAR) && !this.hasCapability(Status.STAR)){
				this.addCapability(Status.STAR);
				System.out.println("Mario is now under the effects of a Power Star!");
			} else if(this.getInventory().get(i).hasCapability(Status.MUSHROOM) && !this.hasCapability(Status.MUSHROOM)){
				System.out.println("Mario is now under the effects of a Super Mushroom");
			}
		}

		if (this.hasCapability(Status.MUSHROOM)){
			this.setDisplayChar(Character.toUpperCase(this.getDisplayChar()));
		}
		char val = this.getDisplayChar();
		if (Character.isUpperCase(val) && !this.hasCapability(Status.MUSHROOM)){
			this.setDisplayChar(Character.toLowerCase(this.getDisplayChar()));
		}

		if(this.hasCapability(Status.STAR) && location.getGround().hasCapability(Status.HIGH_GROUND)){
			location.setGround(new Dirt());
			location.addItem(new Coin(5, location));
		}

		System.out.println("Player coin value: $" + "" + Wallet.getInstance().getValue());
		System.out.println("Player health: " + this.printHp());


		// Handle multi-turn Actions
		if (lastAction.getNextAction() != null)
			return lastAction.getNextAction();

		if(!resetGame){//added reset action
			actions.add(new ResetAction());
		}



		if(!Bottle.getInstance().isEmpty()){
			actions.add(new DrinkWaterAction());
		}

		if(this.hasCapability(Status.POWER_UP)){
			this.damage += 15;
			this.getIntrinsicWeapon();
			this.removeCapability(Status.POWER_UP);
		}


		// return/print the console menu
		return menu.showMenu(this, actions, display);
	}

	@Override
	public char getDisplayChar(){
		return this.hasCapability(Status.TALL) ? Character.toUpperCase(super.getDisplayChar()): super.getDisplayChar();
	}

	@Override
	public void resetInstance() {
		//reseet status effects
		if(this.hasCapability(Status.STAR)){
			this.removeCapability(Status.STAR);
		}else if(this.hasCapability(Status.MUSHROOM)){
			this.removeCapability(Status.MUSHROOM);
		} else if(this.hasCapability(Status.FIRE)){
			this.removeCapability(Status.FIRE);
		}
		//reset max hp
		this.resetMaxHp(100);
		//stop resettable action
		this.resetGame = true;
	}

	@Override
	public IntrinsicWeapon getIntrinsicWeapon(){
		return new IntrinsicWeapon(this.damage, "punches");
	}
	}
