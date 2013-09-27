package geom;

import game.Action;

public interface ActionEncoder {
	/**
	 * Returns an action code corresponding to the given action.
	 * 
	 * @param a
	 *            the action to encode.
	 * @return the action code corresponding to the given action.
	 */
	public int encodeAction(Action a);
}
