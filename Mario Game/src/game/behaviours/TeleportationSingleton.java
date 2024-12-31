package game.behaviours;

import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.items.ItemTradingInventory;

import java.lang.reflect.Array;
import java.util.ArrayList;

/**
 * Used to save last location before teleport for return
 */
public class TeleportationSingleton {
    private ArrayList<GameMap> mapArrayList = new ArrayList<>();
    private ArrayList<Location> locationArrayList = new ArrayList<>();
    private static TeleportationSingleton instance;

    /**
     * Returns the current instance of the class
     * @return current instance of the class
     */
    public static TeleportationSingleton getInstance(){
        if(instance == null){
            instance = new TeleportationSingleton();
        }
        return instance;
    }

    /**
     * Adds a new coordinate to the location list and the map to the map list
     * @param map the current game map
     * @param location the current location
     */
    public void addNewCoordinate(GameMap map, Location location){
        mapArrayList.add(map);
        locationArrayList.add(location);
    }


    /**
     * Grabs the first location teleported from
     * @return the location the player teleported from
     */
    public Location getEarliestLocation(){
        Location locationReturn;
        locationReturn = locationArrayList.get(0);
        locationArrayList.remove(0);
        return locationReturn;
    }

    /**
     * Grabs the first map teleported from
     * @return the map the player teleported from
     */
    public GameMap getEarliestMap(){
        GameMap mapReturn;
        mapReturn = mapArrayList.get(0);
        mapArrayList.remove(0);
        return mapReturn;
    }

    /**
     * Checks if the map list is empty
     * @return a boolean value
     */
    public boolean isWarped(){
        //check for coordinates
        return !mapArrayList.isEmpty();
    }
}
