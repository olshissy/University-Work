package game.ground;

import edu.monash.fit2099.engine.positions.Ground;
import game.Status;

/**
 * A class that represents bare dirt.
 */
public class Dirt extends Ground {

	/**
	 * Constructor
	 */
	public Dirt() {
		super('.');
		this.addCapability(Status.FERTILE);
		this.addCapability(Status.LOW_GROUND);
	}
}
