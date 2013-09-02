package visualiser;


import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Shape;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.geom.AffineTransform;
import java.awt.geom.Path2D;
import java.awt.geom.Point2D;
import java.util.List;

import javax.swing.JComponent;
import javax.swing.Timer;

public class VisualisationPanel extends JComponent {
	/** UID, as required by Swing */
	private static final long serialVersionUID = -4286532773714402501L;
	
	private ProblemSetup problemSetup = new ProblemSetup();
	private Visualiser visualiser;
	
	private AffineTransform translation = AffineTransform.getTranslateInstance(0, -1);
	private AffineTransform transform = null;
	
	private State currentState;
	private boolean animating = false;
	private boolean displayingSolution = false;
	private Timer animationTimer;
	private int framePeriod = 20; // 50 FPS
	private Integer frameNumber = null;
	private int maxFrameNumber;
	
	private int samplingPeriod = 100;
	
	private class VisualisationListener implements ComponentListener {
		@Override
		public void componentResized(ComponentEvent e) {
			calculateTransform();
		}
		@Override
		public void componentHidden(ComponentEvent e) {}
		@Override
		public void componentMoved(ComponentEvent e) {}
		@Override
		public void componentShown(ComponentEvent e) {}
	}
	
	public VisualisationPanel(Visualiser visualiser) {
		super();
		this.setBackground(Color.WHITE);
		this.setOpaque(true);
		this.visualiser = visualiser;
		this.addComponentListener(new VisualisationListener());
	}
	
	public void setDisplayingSolution(boolean displayingSolution) {
		this.displayingSolution = displayingSolution;
		repaint();
	}
	
	public boolean isDisplayingSolution() {
		return displayingSolution;
	}
	
	public void setFramerate(int framerate) {
		this.framePeriod = 1000 / framerate;
		if (animationTimer != null) {
			animationTimer.setDelay(framePeriod);
		}
	}

	public void initAnimation() {
		if (!problemSetup.solutionLoaded()) {
			return;
		}
		if (animationTimer != null) {
			animationTimer.stop();
		}
		animating = true;
		gotoFrame(0);
		maxFrameNumber = problemSetup.getPath().size() - 1;
		animationTimer = new Timer(framePeriod, new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				int newFrameNumber = frameNumber+1;
				if (newFrameNumber >= maxFrameNumber) {
					animationTimer.stop();
					visualiser.setPlaying(false);
				}
				if (newFrameNumber <= maxFrameNumber) {
					gotoFrame(newFrameNumber);
				}
			}
		});
		visualiser.setPlaying(false);
		visualiser.updateMaximum();
	}
	
	public void gotoFrame(int frameNumber) {
		if (!animating || (this.frameNumber != null && this.frameNumber == frameNumber)) {
			return;
		}
		this.frameNumber = frameNumber;
		visualiser.setFrameNumber(frameNumber);
		currentState = problemSetup.getPath().get(frameNumber);
		repaint();
	}
	
	public int getFrameNumber() {
		return frameNumber;
	}
	
	public void playPauseAnimation() {
		if (animationTimer.isRunning()) {
			animationTimer.stop();
			visualiser.setPlaying(false);
		} else {
			if (frameNumber >= maxFrameNumber) {
				gotoFrame(0);
			}
			animationTimer.start();
			visualiser.setPlaying(true);
		}
	}
	
	public void stopAnimation() {
		if (animationTimer != null) {
			animationTimer.stop();
		}
		animating = false;
		visualiser.setPlaying(false);
		frameNumber = null;
	}
	
	public ProblemSetup getProblemSetup() {
		return problemSetup;
	}
	
	public void calculateTransform() {
		transform = AffineTransform.getScaleInstance(
				getWidth(), -getHeight());
		transform.concatenate(translation);
	}
	
	public void paintState(Graphics2D g2, State s) {
		if (s == null) {
			return;
		}
		Path2D.Float path = new Path2D.Float();
		
		List<Point2D> points = s.getASVPositions();
		Point2D p = points.get(0);
		path.moveTo(p.getX(), p.getY());
		for (int i = 1; i < points.size(); i++) {
			p = points.get(i);
			path.lineTo(p.getX(), p.getY());
		}
		path.transform(transform);
		g2.draw(path);
	}
	
	public void setSamplingPeriod(int samplingPeriod) {
		this.samplingPeriod = samplingPeriod;
		repaint();
	}
	
	public void paintComponent(Graphics graphics) {
		super.paintComponent(graphics);
		if (!problemSetup.problemLoaded()) {
			return;
		}
		Graphics2D g2 = (Graphics2D)graphics;
		g2.setColor(Color.WHITE);
		g2.fillRect(0, 0, getWidth(), getHeight());

		List<Obstacle> obstacles = problemSetup.getObstacles();
		if (obstacles != null) {
			g2.setColor(Color.red);
			for (Obstacle obs : problemSetup.getObstacles()) {
				Shape transformed = transform.createTransformedShape(obs.getRect());
				g2.fill(transformed);
			}
		}
		
		g2.setStroke(new BasicStroke(3));
		if (!animating) {
			if (displayingSolution) {
				List<State> path = problemSetup.getPath();
				int lastIndex = path.size() - 1;
				for (int i = 0; i < lastIndex; i += samplingPeriod) {
					float t = (float)i / lastIndex;
					g2.setColor(new Color(0, t, 1-t));
					paintState(g2, path.get(i));
				}
				g2.setColor(Color.green);
				paintState(g2, path.get(lastIndex));
			} else {
				g2.setColor(Color.blue);	
				paintState(g2, problemSetup.getInitialState());
				
				g2.setColor(Color.green);
				paintState(g2, problemSetup.getGoalState());
			}
		} else {
			g2.setColor(Color.blue);
			paintState(g2, currentState);
		}
	}
}