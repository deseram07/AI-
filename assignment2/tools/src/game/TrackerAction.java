package game;

/**
 * Represents an action taken by the tracker.
 * 
 * @author lackofcheese
 * 
 */
public class TrackerAction extends Action {
	/** Whether this action is an HQ call */
	private boolean isHQCall;

	/**
	 * Creates a tracker action that stands still, and may call HQ if desired.
	 * 
	 * @param startState
	 *            the starting state - the tracker will remain in this state.
	 * @param isHQCall
	 *            true iff the tracker should call HQ.
	 */
	public TrackerAction(AgentState startState, boolean isHQCall) {
		super(startState);
		this.isHQCall = isHQCall;
	}

	/**
	 * Creates a camera adjustment action.
	 * 
	 * @param startState
	 *            the starting state.
	 * @param newCameraArmLength
	 *            the new camera arm length.
	 */
	public TrackerAction(AgentState startState, double newCameraArmLength) {
		super(startState, newCameraArmLength);
		this.isHQCall = false;
	}

	/**
	 * Creates a movement action.
	 * 
	 * @param startState
	 *            the starting state.
	 * @param heading
	 *            the direction in which to move.
	 * @param distance
	 *            the distance to move; a value of 0 will cause the tracker to
	 *            stand still, while any other value will result in a movement
	 *            of 1/m units forwards, as per the A2 specifications.
	 */
	public TrackerAction(AgentState startState, double heading, double distance) {
		super(startState, heading, distance);
		this.isHQCall = false;
	}

	/**
	 * Returns true iff this action calls HQ.
	 * 
	 * @return true iff this action calls HQ.
	 */
	public boolean isHQCall() {
		return isHQCall;
	}
}
