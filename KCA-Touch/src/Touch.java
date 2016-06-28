import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class Touch {

	public static void main(String[] args) throws Exception {
		File[] files = new File(
				"C:/Users/Romulus/Documents/Dropbox/GreenSofts/ElectronicObserver/json")
				.listFiles();
		HashMap<String, String> names = new HashMap<String, String>();
		names.put("-1", "なし");
		names.put("25", "零偵");
		names.put("52", "流星改");
		names.put("54", "彩雲");
		names.put("59", "零観");
		names.put("61", "二式艦偵");
		names.put("82", "九三一空九七");
		names.put("93", "友永九七");
		names.put("94", "友永天山");
		names.put("102", "夜偵");
		names.put("113", "六〇一流星");
		names.put("115", "Ar改");
		names.put("118", "紫雲");
		names.put("138", "二式大艇");

		// for (int k = 0; k < 3; k++) {
		// System.out.println((k + 1) + " cell");
		HashMap<String, Integer> count = new HashMap<>();
		int total = 0;
		for (File f : files) {
			String fname = f.getName();
			if (!fname.contains("@battle.json")) {
				if (fname.endsWith(".json")) {
					f.delete();
				}
				continue;
			}
			BufferedReader in = new BufferedReader(new InputStreamReader(
					new FileInputStream(f)));

			String line = in.readLine();
			String touch = StrJsonFinder.findObject(line, "api_touch_plane")
					.split(",")[0];
			if (count.containsKey(touch)) {
				count.put(touch, count.get(touch) + 1);
			} else {
				count.put(touch, 1);
			}
			total++;
			in.close();
		}
		System.out.println("Total:" + total);
		ArrayList<String> acs = new ArrayList<>(count.keySet());
		Collections.sort(acs);
		for (String s : acs) {
			if (names.containsKey(s)) {
				System.out.println(String.format("%s:%d (%.1f%%)",
						names.get(s), count.get(s), count.get(s) * 100.0
								/ total));
			} else {
				System.out.println(String.format("%s:%d (%.1f%%)", s,
						count.get(s), count.get(s) * 100.0 / total));
			}
		}
	}
	// }
}
