package geom;

import java.awt.geom.Point2D;

/**
 * Represents a 2D vector.
 * 
 * @author lackofcheese
 * 
 */
public class Vector2D {
	/** The x-coordinate of the vector. */
	private double x;
	/** The y-coordinate of the vector. */
	private double y;
	/** The magnitude of the vector. */
	private double magnitude;
	/** The direction of the vector. */
	private double direction;

	/**
	 * Constructs this vector as the vector from <code>p0</code> to
	 * </code>p1</code>.
	 * 
	 * @param p0
	 *            the initial point of the vector.
	 * @param p1
	 *            the terminal point of the vector.
	 */
	public Vector2D(Point2D p0, Point2D p1) {
		this(new double[] { p1.getX() - p0.getX(), p1.getY() - p0.getY() });
	}

	/**
	 * Constructs this vector from the given array {x, y}.
	 * 
	 * @param coords
	 *            the array of coordinates {x, y}.
	 */
	public Vector2D(double[] coords) {
		this.x = coords[0];
		this.y = coords[1];
		this.magnitude = Math.sqrt(x * x + y * y);
		this.direction = Math.atan2(y, x);
	}

	/**
	 * Constructs this vector from a magnitude and direction.
	 * 
	 * @param magnitude
	 *            the magnitude of the vector.
	 * @param direction
	 *            the direction, as an angle in radians.
	 */
	public Vector2D(double magnitude, double direction) {
		this.magnitude = magnitude;
		this.direction = GeomTools.normaliseAngle(direction);
		this.x = magnitude * Math.cos(direction);
		this.y = magnitude * Math.sin(direction);
	}

	/**
	 * Returns the turning angle from this vector to the given one.
	 * 
	 * @param otherVector
	 *            another vector.
	 * @return the turning angle from this vector to the given one.
	 */
	public double angleTo(Vector2D otherVector) {
		return GeomTools.normaliseAngle(otherVector.direction - direction);
	}

	/**
	 * Returns the negation of this vector.
	 * 
	 * @return the negation of this vector.
	 */
	public Vector2D negated() {
		return new Vector2D(magnitude, Math.PI + direction);
	}

	/**
	 * Returns the result of adding this vector to the given point.
	 * 
	 * @param point
	 *            the point to add to.
	 * @return the result of adding this vector to the given point.
	 */
	public Point2D addedTo(Point2D point) {
		return new Point2D.Double(point.getX() + x, point.getY() + y);
	}

	/**
	 * Returns the x-coordinate of this vector.
	 * 
	 * @return the x-coordinate of this vector.
	 */
	public double getX() {
		return x;
	}

	/**
	 * Returns the y-coordinate of this vector.
	 * 
	 * @return the y-coordinate of this vector.
	 */
	public double getY() {
		return y;
	}

	/**
	 * Returns the direction of this vector, as an angle in radians.
	 * 
	 * @return the direction of this vector, as an angle in radians.
	 */
	public double getDirection() {
		return direction;
	}

	/**
	 * Returns the magnitude of this vector.
	 * 
	 * @return the magnitude of this vector.
	 */
	public double getMagnitude() {
		return magnitude;
	}

	/**
	 * Returns a string representation of the vector.
	 */
	public String toString() {
		return String.format("%.3f %.3f", x, y);
	}
}
