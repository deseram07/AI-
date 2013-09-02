package visualiser;


import java.util.ArrayList;
import java.util.List;
import java.awt.geom.Point2D;

public class State {
	private List<Point2D> asvPositions = new ArrayList<Point2D>();
	
	public static State interpolate(State s0, State s1, double t) {
		int asvCount = s0.getASVCount();
		double[] coords = new double[asvCount*2];
		for (int i = 0; i < asvCount; i++) {
			coords[i*2] = s0.getPosition(i).getX() * (1-t) + s1.getPosition(i).getX() * t;
			coords[i*2+1] = s0.getPosition(i).getY() * (1-t) + s1.getPosition(i).getY() * t;
		}
		return new State(coords);
	}
	
	public State(double[] coords) {
		for (int i = 0; i < coords.length / 2; i++) {
			asvPositions.add(new Point2D.Double(coords[i*2], coords[i*2+1]));
		}
	}
	
	public State(int asvCount, String str) {
		String[] tokens = str.trim().split("\\s+");
		for (int i = 0; i < asvCount; i++) {
			asvPositions.add(new Point2D.Double(
					Double.valueOf(tokens[i*2]), 
					Double.valueOf(tokens[i*2+1])));
		}
	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		for (Point2D point : asvPositions) {
			if (sb.length() > 0) {
				sb.append(" ");
			}
			sb.append(point.getX());
			sb.append(" ");
			sb.append(point.getY());
		}
		return sb.toString();
	}
	
	public Point2D getPosition(int asvNo) {
		return asvPositions.get(asvNo);
	}
	
	public int getASVCount() {
		return asvPositions.size();
	}
	
	public List<Point2D> getASVPositions() {
		return new ArrayList<Point2D>(asvPositions);
	}
}
