import java.io.*;
import java.util.*;

import org.json.JSONObject;

import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.CoreMap;

public class Preprocessing {
	
	public static HashMap<String, Boolean> stopWords = new HashMap<String, Boolean>();
	public static BufferedReader revReader;
	public static BufferedWriter revWriter;
	public static ArrayList<JSONObject> rawReviews = new ArrayList<JSONObject>();
	public static ArrayList<JSONObject> processedReviews = new ArrayList<JSONObject>();
	public static StanfordCoreNLP pipeline;
	
	public static void readStopWords() throws IOException {
		BufferedReader bReader = new BufferedReader(new FileReader(new File("/home/ke/Documents/stop-words.txt")));
		String line =  new String();
		while ((line = bReader.readLine()) != null) {
			stopWords.put(line, true);
		}
		bReader.close();
	}
	
	public static void writeToCsv() throws IOException {
		String writeStr = new String();
		for (JSONObject jsObj : processedReviews) {
			writeStr = jsObj.getString("review_id") + ',' + jsObj.getString("business_id") + ',' + jsObj.getString("text")+'\n';
			revWriter.write(writeStr);
			revWriter.flush();
		}
	}
	
	public static void processReview() throws IOException {
		String rawText = new String();
		StringBuilder text = new StringBuilder();
		JSONObject revObj;
		for (JSONObject raw : rawReviews) {
			text = new StringBuilder();
			rawText = raw.get("text").toString();
			Annotation doc = new Annotation(rawText);
			pipeline.annotate(doc);
			
			List<CoreMap> sentences = doc.get(SentencesAnnotation.class);
			for(CoreMap sentence : sentences) {
				for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
					String lemma = token.get(LemmaAnnotation.class).toLowerCase();
					String pos = token.get(PartOfSpeechAnnotation.class);
					if (!stopWords.containsKey(lemma) && !pos.equals("CD"))
						text.append(lemma + ' ');
				}
			}
			if (text.length() != 0)
				text.deleteCharAt(text.length()-1);
			
			revObj = new JSONObject();
			revObj.put("review_id", raw.get("review_id"));
			revObj.put("business_id", raw.get("business_id"));
			revObj.put("text", text.toString());
			processedReviews.add(revObj);
		};
	}
	
	public static void main(String[] args) throws IOException {
		readStopWords();
		
		revReader = new BufferedReader(new FileReader(new File("/home/ke/Documents/review.json")));
		
		File outputFile = new File("/home/ke/Documents/processed_reviews.csv");
		if (!outputFile.exists())
			outputFile.createNewFile();
		revWriter = new BufferedWriter(new FileWriter(outputFile));
		
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize, ssplit, pos, lemma");
		pipeline = new StanfordCoreNLP(props);
		
		String line = new String();
		int count  = 0;
		while ((line = revReader.readLine()) != null) {
			if (count < 100000)
				++count;
			else {
				processReview();
				writeToCsv();
				rawReviews = new ArrayList<JSONObject>();
				processedReviews = new ArrayList<JSONObject>();
				count = 0;
			}
			rawReviews.add(new JSONObject(line));
		}
		revReader.close();
		revWriter.close();
	}
	
}