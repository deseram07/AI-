package game;

import java.awt.geom.Rectangle2D;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

/**
 * This class represents a rectangular region in the workspace.
 * 
 * @author lackofcheese
 */
public class RectRegion {
	/** Stores the region as a Rectangle2D */
	private Rectangle2D rect;

	/**
	 * Constructs this region as a duplicte of another region.
	 * 
	 * @param other
	 *            the region to duplicate.
	 */
	public RectRegion(RectRegion other) {
		this.rect = (Rectangle2D) other.rect.clone();
	}

	/**
	 * Constructs a region with the given (x,y) coordinates of the bottom-left
	 * corner, as well as the width and height.
	 * 
	 * @param x
	 *            the minimum x-value.
	 * @param y
	 *            the minimum y-value.
	 * @param w
	 *            the width of the obstacle.
	 * @param h
	 *            the height of the obstacle.
	 */
	public RectRegion(double x, double y, double w, double h) {
		this.rect = new Rectangle2D.Double(x, y, w, h);
	}

	/**
	 * Constructs a region from the representation used in the input file: that
	 * is, the x- and y- coordinates of all of the corners of the rectangle.
	 * 
	 * @param str
	 */
	public RectRegion(String str) {
		Scanner s = new Scanner(str);
		List<Double> xs = new ArrayList<Double>();
		List<Double> ys = new ArrayList<Double>();
		for (int i = 0; i < 4; i++) {
			xs.add(s.nextDouble());
			ys.add(s.nextDouble());
		}
		double xMin = Collections.min(xs);
		double xMax = Collections.max(xs);
		double yMin = Collections.min(ys);
		double yMax = Collections.max(ys);
		this.rect = new Rectangle2D.Double(xMin, yMin, xMax - xMin, yMax - yMin);
		s.close();
	}

	/**
	 * Returns a copy of the Rectangle2D representing this region.
	 * 
	 * @return a copy of the Rectangle2D representing this region.
	 */
	public Rectangle2D getRect() {
		return (Rectangle2D) rect.clone();
	}

	/**
	 * Returns a String representation of this region.
	 * 
	 * @return a String representation of this region.
	 */
	public String toString() {
		return rect.toString();
	}
}
