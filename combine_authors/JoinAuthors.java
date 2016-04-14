import java.io.*;
import java.util.*;

class JoinAuthors {
	public static HashMap<String, ArrayList<File>> authors = new HashMap<String, ArrayList<File>>();
	
	public static void main(String[] args) throws IOException {
		final File folder = new File("novels");
		listFilesForFolder(folder);
		combineFiles();
	}

	public static void listFilesForFolder(final File folder) throws IOException {
		for (final File fileEntry : folder.listFiles()) {
			String fileName[] = fileEntry.getName().split("_");
			String lastName = fileName[0];
			if (authors.containsKey(lastName)) { 
				ArrayList<File> files = authors.get(lastName);
				files.add(fileEntry);
				authors.put(lastName, files);
			} else { 
				authors.put(lastName, new ArrayList<File>());
				ArrayList<File> files = authors.get(lastName);
				files.add(fileEntry);
				authors.put(lastName, files);
			}
		}
	}
	
	public static void combineFiles() throws IOException {
		for(String lastName : authors.keySet()) {
			BufferedWriter bw = new BufferedWriter(new FileWriter("../output/" + lastName + ".txt"));
			try {
				String line = null;
				for (File file : authors.get(lastName)) {
					BufferedReader br = new BufferedReader(new FileReader("/Users/matthewsobocinski/Desktop/novels/" + file.getName()));
					while ((line = br.readLine()) != null) {
						bw.write(line + "\n");
					}
				}
				bw.flush();
				bw.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
}