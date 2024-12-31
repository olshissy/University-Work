
package game;

import java.util.Arrays;
import java.util.List;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.FancyGroundFactory;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.World;
import game.actors.*;
import game.fountain.HealingFountain;
import game.fountain.PowerFountain;
import game.ground.*;
import game.items.PowerStar;
import game.items.SuperMushroom;
import game.trees.Sprout;

/**
 * The main class for the Mario World game.
 *
 */
public class Application {
	public static GameMap secondaryMap;
	public static GameMap primaryMap;

	public static void main(String[] args) {

		World world = new World(new Display());

		FancyGroundFactory groundFactory = new FancyGroundFactory(new Dirt(), new Wall(), new Floor(), new Sprout(), new HealingFountain(), new PowerFountain(), new Lava(), new Pipe());

		List<String> map = Arrays.asList(
				"..........................................##..........+.........................",
				"............+............+..................#...................................",
				"............................................#...................................",
				"..................................C..........##......................+..........",
				"...............................................#................................",
				"................................................#...............................",
				".................+................................#.....................C.......",
				".....................................H.........A.##.............................",
				"....................C...........................##..............................",
				".........+..............................+#____####.................+............",
				".......................................+#______###++.............................",
				".......................................+#______###..............................",
				"........................................+#_____###..............................",
				"........................+........................##.............+...............",
				"...........C.......................................#............................",
				"....................................................#...........................",
				"...................+.................................#..........................",
				"......................................................#.........................",
				".......................................................##.......................");

		GameMap gameMap = new GameMap(groundFactory, map);
		world.addGameMap(gameMap);


		List<String> Lavamap = Arrays.asList(
				"C.........LLLLLLLLLLLLLLLL......................................................",
				"............LLLLLLLLLLLLLLLLLLL.................................................",
				"................................................................................",
				".......................................................LLLLLLLLLLLLLL...........",
				"...........LLLLLLLLLLLLLLLLLL........................LLLLLLLLLLLLLLLLLLL........",
				".....LLLLLLLLLLLLLLL..................................LLLLLLLLL.................",
				"...........LLLLLLLLLLLLLLLL.....................................................",
				".................LLLLLLLLLLLLL..................................................",
				"..............LLLLLLLLLLLL......................A...............................",
				"..........LLLLLLLLLLLLLLLLLLLL..................................................",
				"................................................................................",
				"................................................................................",
				"...........................................H............LLLLLLLLLL..............",
				"............LLLLLLLLLLLLLLLLL........................LLLLLLLLLLLLLLLL...........",
				".........LLLLLLLLLLLLLLLLLLLLL..........................LLLLLLLLLL..............",
				"............LLLLLLLLLLLLL.......................................................",
				".............LLLLLLLLL..........................................................",
				"................................................................................",
				"................................................................................");

		secondaryMap = new GameMap(groundFactory, Lavamap);
		world.addGameMap(secondaryMap);

		Actor mario = new Player("Player", 'm', 10000);
		world.addPlayer(mario, gameMap.at(42, 10));
		gameMap.at(42,10).addItem(new PowerStar(mario));
		gameMap.at(42,10).addItem(new SuperMushroom());
		gameMap.at(43,11).addActor(new Toad());

		secondaryMap.at(72,8).addActor(new PrincessPeach());
		secondaryMap.at(70,8).addActor(new Bowser());

		world.run();

	}
}