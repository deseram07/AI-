package game;

/**
 * Represents a percept, as seen by the tracker.
 * 
 * @author lackofcheese
 * 
 */
public class Percept {
	/** The turn number of the turn after which this percept was seen. */
	private int turnNo;
	/** The number of the agent that was seen. */
	private int agentNo;
	/** The state of the agent that was seen, at the time it was seen. */
	private AgentState agentState;

	/**
	 * Constructs a percept with the given parameters.
	 * 
	 * @param turnNo
	 *            the turn number.
	 * @param agentNo
	 *            the agent number.
	 * @param agentState
	 *            the agent state.
	 */
	public Percept(int turnNo, int agentNo, AgentState agentState) {
		this.turnNo = turnNo;
		this.agentNo = agentNo;
		this.agentState = agentState;
	}

	/**
	 * Returns the number of the turn after which this percept was seen.
	 * 
	 * @return the number of the turn after which this percept was seen.
	 */
	public int getTurnNo() {
		return turnNo;
	}

	/**
	 * Returns the number of the agent that was seen.
	 * 
	 * @return the number of the agent that was seen.
	 */
	public int getAgentNo() {
		return agentNo;
	}

	/**
	 * Returns the perceived state of the perceived agent after turn #turnNo.
	 * 
	 * @return the perceived state of the perceived agent after turn #turnNo.
	 */
	public AgentState getAgentState() {
		return agentState;
	}

	@Override
	public String toString() {
		return String.format("Turn %d: Saw agent %d in state %s", turnNo,
				agentNo, agentState);
	}
}
