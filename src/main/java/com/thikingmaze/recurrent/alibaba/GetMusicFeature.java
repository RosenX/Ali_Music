package com.thikingmaze.recurrent.alibaba;

import java.io.IOException;
import java.text.ParseException;

public class GetMusicFeature {
	public static void main(String[] args) throws ParseException, IOException{
		String actionFilePath = "C:\\Users\\star\\git\\PopularMusicPrediction\\mars_tianchi_user_actions.csv";
		int miniBatchSize = 32;
		int exampleSize = 100;
		int numExamplesToFetch = 10*miniBatchSize; 
		ArtistIterator iter = new ArtistIterator(actionFilePath, miniBatchSize, exampleSize, numExamplesToFetch);
		return ;
	}
}
