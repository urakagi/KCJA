import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class NightTouchAndCutin {

	public static void main(String[] args) throws Exception {
		File[] files = new File(
				"C:/Users/Romulus/Documents/Dropbox/GreenSofts/KCRDB/json")
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
		names.put("118", "紫雲");

		// for (int k = 0; k < 3; k++) {
		// System.out.println((k + 1) + " cell");
		HashMap<String, Integer> count = new HashMap<>();
		count.put("102", 3);
		int total = 3;
		int ttl_flag_ci = 2;
		int ttl_flag_noci = 0;
		int ttl_2_ci = 2;
		int ttl_2_noci = -1;
		for (File f : files) {
			if (!f.getName().contains("sp_midnight")) {
				continue;
			}
			BufferedReader in = new BufferedReader(new InputStreamReader(
					new FileInputStream(f)));
			in.readLine();
			String line = in.readLine();
			int spIdx = line.indexOf("\"api_sp_list\":");
			int spStart = line.indexOf("[", spIdx);
			int spEnd = line.indexOf("]", spIdx);
			String e = line.substring(spStart + 1, spEnd);
			String[] ee = e.split(",");
			int flagci = Integer.parseInt(ee[1]);
			if (flagci == 3) {
				ttl_flag_ci++;
			} else {
				ttl_flag_noci++;
			}

			int atIdx = line.indexOf("\"api_at_list\":");
			int atStart = line.indexOf("[", atIdx);
			int atEnd = line.indexOf("]", atIdx);
			String ate = line.substring(atStart + 1, atEnd);
			String[] atee = ate.split(",");
			int secidx;
			if (Integer.parseInt(atee[3]) == 2) {
				secidx = 3;
			} else {
				secidx = 2;
			}
			int secci = Integer.parseInt(ee[secidx]);
			if (secci == 3) {
				ttl_2_ci++;
			} else {
				ttl_2_noci++;
			}

			int idx = line.indexOf("\"api_touch_plane\":");
			if (idx > 0) {
				int start = line.indexOf("[", idx);
				int end = line.indexOf("]", idx);
				String d = line.substring(start + 1, end);
				String touch = d.split(",")[0];
				if (count.containsKey(touch)) {
					count.put(touch, count.get(touch) + 1);
				} else {
					count.put(touch, 1);
				}
				total++;
			}
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
		System.out.println();
		System.out.println(String.format("旗艦CI：%d/%d (%.1f%%)", ttl_flag_ci,
				ttl_flag_ci + ttl_flag_noci, ttl_flag_ci * 100.0
						/ (ttl_flag_ci + ttl_flag_noci)));
		System.out.println(String.format("僚艦CI：%d/%d (%.1f%%)", ttl_2_ci,
				ttl_2_ci + ttl_2_noci, ttl_2_ci * 100.0
				/ (ttl_2_ci + ttl_2_noci)));
	}
	// }
}
