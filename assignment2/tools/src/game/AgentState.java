package game;

import java.awt.geom.Point2D;
import java.util.Scanner;

/**
 * Represents the state of an agent within the game.
 * 
 * @author lackofcheese
 * 
 */
public class AgentState {
	/** The position of the agent. */
	protected Point2D position;
	/** The heading of the agent. */
	protected double heading;
	/** True iff the agent has a camera. */
	private boolean hasCamera = false;
	/** The camera arm length, if applicable. */
	private double cameraArmLength = 0;

	/**
	 * Crates a state from a String representation, as found in input files.
	 * 
	 * @param hasCamera
	 *            whether the agent has a camera.
	 * @param line
	 *            the String representation of the state.
	 */
	public AgentState(boolean hasCamera, String line) {
		this.hasCamera = hasCamera;
		Scanner s = new Scanner(line);
		position = new Point2D.Double(s.nextDouble(), s.nextDouble());
		heading = Math.toRadians(s.nextDouble());
		if (hasCamera) {
			cameraArmLength = s.nextDouble();
		}
		s.close();
	}

	/**
	 * Creates a state for an agent with no camera.
	 * 
	 * @param position
	 *            the position of the agent.
	 * @param heading
	 *            the heading of the agent.
	 */
	public AgentState(Point2D position, double heading) {
		this.position = (Point2D) position.clone();
		this.heading = heading;
	}

	/**
	 * Creates a state for an agent that may have a camera.
	 * 
	 * @param position
	 *            the position of the agent.
	 * @param heading
	 *            the heading of the agent.
	 * @param hasCamera
	 *            whether the agent has a camera.
	 * @param cameraArmLength
	 *            the camera arm length.
	 */
	public AgentState(Point2D position, double heading, boolean hasCamera,
			double cameraArmLength) {
		this(position, heading);
		this.hasCamera = hasCamera;
		this.cameraArmLength = cameraArmLength;
	}

	/**
	 * Duplicates an agent state.
	 * 
	 * @param as
	 *            the state to duplicate.
	 */
	public AgentState(AgentState as) {
		this(as.position, as.heading, as.hasCamera, as.cameraArmLength);
	}

	/**
	 * Returns the position of the agent.
	 * 
	 * @return the position of the agent.
	 */
	public Point2D getPosition() {
		return position;
	}

	/**
	 * Returns the heading of the agent.
	 * 
	 * @return the heading of the agent.
	 */
	public double getHeading() {
		return heading;
	}

	/**
	 * Returns true iff the agent has a camera.
	 * 
	 * @return true iff the agent has a camera.
	 */
	public boolean hasCamera() {
		return hasCamera;
	}

	/**
	 * Returns the camera arm length.
	 * 
	 * @return the camera arm length.
	 */
	public double getCameraArmLength() {
		return cameraArmLength;
	}

	/**
	 * Returns a string representation of this state.
	 */
	public String toString() {
		String result = String.format("%8f %8f %11f", position.getX(),
				position.getY(), Math.toDegrees(heading));
		if (hasCamera) {
			result += String.format(" %8f", cameraArmLength);
		} else {
			result += String.format("%9s", "");
		}
		return result;
	}

	@Override
	public boolean equals(Object o) {
		if (!(o instanceof AgentState)) {
			return false;
		}
		AgentState other = (AgentState) o;
		return (position.equals(other.position) && heading == other.heading
				&& hasCamera == other.hasCamera && (!hasCamera || cameraArmLength == other.cameraArmLength));
	}

	@Override
	public int hashCode() {
		int hashCode = position.hashCode();
		hashCode = hashCode * 31 + new Double(heading).hashCode();
		if (hasCamera) {
			hashCode += new Double(cameraArmLength).hashCode();

		}
		return hashCode;
	}
}
