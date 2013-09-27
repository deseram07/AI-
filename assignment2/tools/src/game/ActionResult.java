package game;

/**
 * Represents an attempted action, and the actual result of executing this
 * action.
 * 
 * @author lackofcheese
 * 
 */
public class ActionResult {
	/** The desired action. */
	private Action desiredAction;
	/** The diverged action. */
	private Action divergedAction;
	/** The resulting new state. */
	private AgentState resultingState;
	/** The reward. */
	private double reward;

	/**
	 * Constructs an action result.
	 * 
	 * @param desiredAction
	 *            the action.
	 * @param divergedAction
	 *            the action, after divergence.
	 * @param resultingState
	 *            the resulting state.
	 * @param reward
	 *            the reward.
	 */
	public ActionResult(Action desiredAction, Action divergedAction,
			AgentState resultingState, double reward) {
		this.desiredAction = desiredAction;
		this.divergedAction = divergedAction;
		this.resultingState = resultingState;
		this.reward = reward;
	}

	/**
	 * Returns the desired action.
	 * 
	 * @return the desired action.
	 */
	public Action getDesiredAction() {
		return desiredAction;
	}

	/**
	 * Returns the diverged action.
	 * 
	 * @return the diverged action.
	 */
	public Action getDivergedAction() {
		return divergedAction;
	}

	/**
	 * Returns the resulting state.
	 * 
	 * @return the resulting state.
	 */
	public AgentState getResultingState() {
		return resultingState;
	}

	/**
	 * Returns the reward.
	 * 
	 * @return the reward.
	 */
	public double getReward() {
		return reward;
	}
}
