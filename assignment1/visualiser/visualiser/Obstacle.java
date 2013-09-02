package visualiser;


import java.awt.geom.Rectangle2D;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Obstacle {
	private Rectangle2D rect; 
	
	public Obstacle(double x, double y, double w, double h) {
		this.rect = new Rectangle2D.Double(x, y, w, h);
	}
	
	public Obstacle(String str) {
		String[] tokens = str.trim().split("\\s+");
		List<Double> xs = new ArrayList<Double>();
		List<Double> ys = new ArrayList<Double>();
		for (int i = 0; i < 4; i++) {
			xs.add(Double.valueOf(tokens[i*2]));
			ys.add(Double.valueOf(tokens[i*2+1]));
		}
		double xMin = Collections.min(xs);
		double xMax = Collections.max(xs);
		double yMin = Collections.min(ys);
		double yMax = Collections.max(ys);
		this.rect = new Rectangle2D.Double(xMin, yMin, xMax-xMin, yMax-yMin);
	}
	
	public Rectangle2D getRect() {
		return (Rectangle2D)rect.clone();
	}
	
	public String toString() {
		return rect.toString();
	}
}
