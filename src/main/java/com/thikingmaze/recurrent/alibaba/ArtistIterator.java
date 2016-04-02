package com.thikingmaze.recurrent.alibaba;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.Scanner;

import org.deeplearning4j.datasets.iterator.DataSetIterator;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.dataset.api.DataSetPreProcessor;
import org.nd4j.linalg.factory.Nd4j;

/** A very simple DataSetIterator for use in the MyLSTMModel.
 * Given a text file and a few options, generate feature vectors and labels for training,
 * where we want to predict the next character in the sequence.<br>
 * This is done by randomly choosing a position in the text file to start the sequence and
 * (optionally) scanning backwards to a new line (to ensure we don't start half way through a word
 * for example).<br>
 * Feature vectors and labels are both one-hot vectors of same length
 * @author Alex Black
 */
public class ArtistIterator implements DataSetIterator {
	private static final long serialVersionUID = -7287833919126626356L;
	private static final int MAX_SCAN_LENGTH = 200; 
	private static Map<String,String> songToArtist;
	private String[] validArtists;
	private Map<String,Integer> artistToIdxMap;
	private Map<String,List<List<Integer>>> userTimeSequence;
	private String[] actions;
	private int exampleLength;
	private int miniBatchSize;
	private int numExamplesToFetch;
	private int examplesSoFar = 0;
	private Random rng;
	private final int numArtists;
	
	public ArtistIterator(String path, int miniBatchSize, int exampleSize, int numExamplesToFetch ) throws IOException {
		this(path,miniBatchSize,exampleSize,numExamplesToFetch,getDefaultArtistSet(),new Random());
	}
	
	public ArtistIterator(String textFilePath, int miniBatchSize, int exampleLength, int numExamplesToFetch, 
			String[] validArtists, Random rng ) throws IOException {
		if( !new File(textFilePath).exists()) throw new IOException("Could not access file (does not exist): " + textFilePath);
		if(numExamplesToFetch % miniBatchSize != 0 ) throw new IllegalArgumentException("numExamplesToFetch must be a multiple of miniBatchSize");
		if( miniBatchSize <= 0 ) throw new IllegalArgumentException("Invalid miniBatchSize (must be >0)");
		this.exampleLength = exampleLength;
		this.miniBatchSize = miniBatchSize;
		this.numExamplesToFetch = numExamplesToFetch;
		this.validArtists = validArtists;
		this.rng = rng;
		this.numArtists = validArtists.length;
		
		//Store valid characters is a map for later use in vectorization
		artistToIdxMap = new HashMap<>();
		for( int i=0; i<validArtists.length; i++ ) artistToIdxMap.put(validArtists[i], i);
		
		List<String> lines = Files.readAllLines(new File(textFilePath).toPath(), Charset.defaultCharset());
		int maxSize = lines.size();	//add lines.size() to account for actions 
		this.actions = new String[maxSize];
		int currIdx = 0;
		this.userTimeSequence = new HashMap<String,List<List<Integer>>>();
		
		for( String line : lines ){
			this.actions[currIdx++] = line;
		}
		preProcessAction(this.actions);
		
		for(String action : this.actions){
			System.out.println(action);
		}
		
		if( exampleLength >= actions.length ) throw new IllegalArgumentException("exampleLength="+exampleLength
				+" cannot exceed number of valid actions in file ("+actions.length+")");
		
		System.out.println("Loaded and converted file: " + actions.length + " valid actions of " + maxSize);
	}
	
	private static void preProcessAction(String[] actions){
		class Action  implements Comparable<Action>{
			public String action = null;
			
			Action(String action){
				this.action = action;
			}
			@Override
			public int compareTo(Action o) {
				// TODO Auto-generated method stub
				Integer actionTimeA = Integer.valueOf(this.action.split(",")[2]);
				Integer actionTimeB = Integer.valueOf(o.action.split(",")[2]);
				return actionTimeA.compareTo(actionTimeB);
			}
		}
		
		List<Action> tmpActions = new ArrayList<Action>();
		for(String action : actions){
			tmpActions.add(new Action(action));
		}
		Collections.sort(tmpActions);
		for(int i = 0; i < actions.length; i++){
			actions[i] = tmpActions.get(i).action;
		}
	}
	
	/** As per getMinimalCharacterSet(), but with a few extra characters 
	 * @throws FileNotFoundException */
	public static String[] getDefaultArtistSet() throws FileNotFoundException{
		Scanner sin = new Scanner(new File("C:\\Users\\star\\git\\PopularMusicPrediction\\mars_tianchi_songs.csv"));
		List<String> validArtists = new LinkedList<>();
		songToArtist = new HashMap<String, String>();
		while(sin.hasNext()){
			String line = sin.next();
			validArtists.add(line.split(",")[1]);
			songToArtist.put(line.split(",")[0], line.split(",")[1]);
		}
		
		String[] out = new String[validArtists.size()];
		int i = 0;
		for( String c : validArtists ) out[i++] = c;
		return out;
	}
	
	public String convertIndexToArtist( int idx ){
		return validArtists[idx];
	}
	
	public int convertArtistToIndex( char c ){
		return artistToIdxMap.get(c);
	}
	
	public String getRandomArtist(){
		return validArtists[(int) (rng.nextDouble()*validArtists.length)];
	}

	public boolean hasNext() {
		return examplesSoFar + miniBatchSize <= numExamplesToFetch;
	}

	public DataSet next() {
		return next(miniBatchSize);
	}

	public DataSet next(int num) {
		throw new NoSuchElementException();
	}

	public int totalExamples() {
		return numExamplesToFetch;
	}

	public int inputColumns() {
		return numArtists;
	}

	public int totalOutcomes() {
		return numArtists;
	}

	public void reset() {
		examplesSoFar = 0;
	}

	public int batch() {
		return miniBatchSize;
	}

	public int cursor() {
		return examplesSoFar;
	}

	public int numExamples() {
		return numExamplesToFetch;
	}

	public void setPreProcessor(DataSetPreProcessor preProcessor) {
		throw new UnsupportedOperationException("Not implemented");
	}

	@Override
	public List<String> getLabels() {
		throw new UnsupportedOperationException("Not implemented");
	}

	@Override
	public void remove() {
		throw new UnsupportedOperationException();
	}

}