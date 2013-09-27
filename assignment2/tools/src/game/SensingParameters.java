package game;

import java.util.Scanner;

/**
 * Represents the sensing parameters of an agent.
 * 
 * @author lackofcheese
 * 
 */
public class SensingParameters {
	/** True iff the agent has a camera. */
	private boolean hasCamera;
	/** The sight range. */
	private double range;
	/** The field of view, in radians. */
	private double angle;
	/** The minimum camera arm length, if applicable. */
	private double minLength;
	/** The maximum camera arm length, if applicable. */
	private double maxLength;

	/**
	 * Duplicates another set of sensing parameters.
	 * 
	 * @param otherParams
	 *            the parameters to duplicate.
	 */
	public SensingParameters(SensingParameters otherParams) {
		this.hasCamera = otherParams.hasCamera;
		this.range = otherParams.range;
		this.angle = otherParams.angle;
		this.minLength = otherParams.minLength;
		this.maxLength = otherParams.maxLength;
	}

	/**
	 * Constructs sensing parameters from a String, as seen in the input files.
	 * 
	 * @param hasCamera
	 *            whether the agent has a camera.
	 * @param line
	 *            the String to read.
	 */
	public SensingParameters(boolean hasCamera, String line) {
		this.hasCamera = hasCamera;
		Scanner s = new Scanner(line);
		if (hasCamera) {
			minLength = s.nextDouble();
			maxLength = s.nextDouble();
		}
		angle = Math.toRadians(s.nextDouble());
		range = s.nextDouble();
		s.close();
	}

	/**
	 * Constructs sensing parameters for an agent with no camera, and with the
	 * given sight range and FOV.
	 * 
	 * @param range
	 *            the sight range.
	 * @param angle
	 *            the field of view in radians.
	 */
	public SensingParameters(double range, double angle) {
		this.hasCamera = false;
		this.range = range;
		this.angle = angle;
	}

	/**
	 * Constructs sensing parameters for an agent with a camera, and with the
	 * given sight range and FOV, and camera arm bounds.
	 * 
	 * @param range
	 *            the sight range.
	 * @param angle
	 *            the field of view in radians.
	 * @param minLength
	 *            the minimum camera arm length.
	 * @param maxLength
	 *            the maximum camera arm length.
	 */
	public SensingParameters(double range, double angle, double minLength,
			double maxLength) {
		this.hasCamera = true;
		this.range = range;
		this.angle = angle;
		this.minLength = minLength;
		this.maxLength = maxLength;
	}

	/**
	 * Returns whether this agent has a camera.
	 * 
	 * @return whether this agent has a camera.
	 */
	public boolean hasCamera() {
		return hasCamera;
	}

	/**
	 * Returns the sight range of this agent.
	 * 
	 * @return the sight range of this agent.
	 */
	public double getRange() {
		return range;
	}

	/**
	 * Returns the FOV of this agent, in radians.
	 * 
	 * @return the FOV of this agent, in radians.
	 */
	public double getAngle() {
		return angle;
	}

	/**
	 * Returns the minimum camera arm length for this agent.
	 * 
	 * @return the minimum camera arm length for this agent.
	 */
	public double getMinLength() {
		return minLength;
	}

	/**
	 * Returns the maximum camera arm length for this agent.
	 * 
	 * @return the maximum camera arm length for this agent.
	 */
	public double getMaxLength() {
		return maxLength;
	}

}
