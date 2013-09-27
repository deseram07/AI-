package game;

import java.util.List;

/**
 * Represents an agent (tracker or target) within the game.
 * 
 * @author lackofcheese
 * 
 */
public interface Agent {
	/**
	 * Returns the action the agent will attempt to take.
	 * 
	 * @param turnNo
	 *            the turn number.
	 * @param previousResult
	 *            the result of the previous action.
	 * @param scores
	 *            the current scores.
	 * @param newPercepts
	 *            the percepts acquired since the agent's last turn.
	 * @return the action this agent will attempt to take.
	 */
	public Action getAction(int turnNo, ActionResult previousResult,
			double[] scores, List<Percept> newPercepts);
}
