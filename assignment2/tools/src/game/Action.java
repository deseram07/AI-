package game;

import geom.Vector2D;

import java.awt.geom.Point2D;

/**
 * Represents an action attempted by one of the agents in the game.
 * 
 * @author lackofcheese
 * 
 */
public class Action {
	/** Whether this action is a movement action. */
	private boolean isMovement;
	/** Whether this action is a camera adjustment. */
	private boolean isCameraAdjustment;

	/** The new heading for the agent, in radians. */
	private double heading;
	/** The distance to travel. */
	private double distance;

	/** The initial state. */
	private AgentState startState;
	/** The expected resulting state after this action. */
	private AgentState resultingState;

	/**
	 * The simplest action - stay still and do nothing.
	 * 
	 * @param startState
	 *            the starting state.
	 */
	public Action(AgentState startState) {
		this.isMovement = false;
		this.isCameraAdjustment = false;

		this.startState = startState;
		this.heading = startState.getHeading();
		this.distance = 0;
		this.resultingState = startState;
	}

	/**
	 * A camera adjustment action - keep position and heading, but change the
	 * length of the camera arm.
	 * 
	 * @param startState
	 *            the starting state.
	 * @param newCameraArmLength
	 *            the new camera arm length.
	 */
	public Action(AgentState startState, double newCameraArmLength) {
		this.isMovement = false;
		this.isCameraAdjustment = true;

		this.startState = startState;
		this.heading = startState.getHeading();
		this.distance = 0;
		this.resultingState = new AgentState(startState.getPosition(),
				startState.getHeading(), startState.hasCamera(),
				newCameraArmLength);
	}

	/**
	 * A movement with the given heading and distance. To stay in the same place
	 * while changing heading, simply use a distance of 0.
	 * 
	 * @param startState
	 *            the starting state.
	 * @param heading
	 *            the new heading.
	 * @param distance
	 *            the distance to travel.
	 */
	public Action(AgentState startState, double heading, double distance) {
		this.isMovement = true;
		this.isCameraAdjustment = false;

		this.startState = startState;
		this.heading = heading;
		this.distance = distance;
		Point2D startPos = startState.getPosition();
		Point2D endPos;
		if (distance == 0) {
			if (heading == startState.getHeading()) {
				this.isMovement = false;
			}
			endPos = startPos;
		} else {
			endPos = new Vector2D(distance, heading).addedTo(startPos);
		}
		this.resultingState = new AgentState(endPos, heading,
				startState.hasCamera(), startState.getCameraArmLength());
	}

	/**
	 * A movement to the given desired position.
	 * 
	 * @param startState
	 *            the starting state.
	 * @param desiredPos
	 *            the position to travel towards.
	 */
	public Action(AgentState startState, Point2D desiredPos) {
		this.isCameraAdjustment = false;
		this.isMovement = true;

		this.startState = startState;
		Point2D startPos = startState.getPosition();
		if (startPos.equals(desiredPos)) {
			this.isMovement = false;
			this.heading = startState.getHeading();
			this.distance = 0;
		} else {
			Vector2D motion = new Vector2D(startPos, desiredPos);
			this.heading = motion.getDirection();
			this.distance = motion.getMagnitude();
		}
		this.resultingState = new AgentState(desiredPos, heading,
				startState.hasCamera(), startState.getCameraArmLength());
	}

	/**
	 * Returns true iff this action involves a heading change or movement.
	 * 
	 * @return true iff this action involves a heading change or movement.
	 */
	public boolean isMovement() {
		return isMovement;
	}

	/**
	 * Returns true iff this action is a camera adjustment.
	 * 
	 * @return true iff this action is a camera adjustment.
	 */
	public boolean isCameraAdjustment() {
		return isCameraAdjustment;
	}

	/**
	 * Returns the heading taken for this action.
	 * 
	 * @return the heading taken for this action.
	 */
	public double getHeading() {
		return heading;
	}

	/**
	 * Returns the distance travelled for this action.
	 * 
	 * @return the distance travelled for this action.
	 */
	public double getDistance() {
		return distance;
	}

	/**
	 * Returns the displacement vector for this action.
	 * 
	 * @return the displacement vector for this action.
	 */
	public Vector2D getDisplacement() {
		return new Vector2D(distance, heading);
	}

	/**
	 * Returns the initial state before this action.
	 * 
	 * @return the initial state before this action.
	 */
	public AgentState getStartState() {
		return startState;
	}

	/**
	 * Returns the resulting state after this action.
	 * 
	 * @return the resulting state after this action.
	 */
	public AgentState getResultingState() {
		return resultingState;
	}
}
