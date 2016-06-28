import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;

public class LogBookParser {

	private static String[] NO_TOUCH_PLANES = new String[] { "烈風", "彗星", "瑞雲",
			"晴嵐", "零戦", "零式艦戦", "深海棲艦" };

	public static void main(String[] args) throws Exception {
		final HashMap<String, HashMap<String, Integer>> result = new HashMap<>();
		final HashMap<String, Integer> counts = new HashMap<>();
		File[] files = new File("D:/Mahiru-data/data/").listFiles();
		for (int j = 0; j < files.length; j++) {
			if (j % 500 == 0) {
				System.out.println(j + "/" + files.length);
			}
			File f = files[j];
			try {
				BufferedReader in = new BufferedReader(new InputStreamReader(
						new FileInputStream(f), "UTF-8"));
				StringBuilder b = new StringBuilder();
				for (String line = in.readLine(); line != null; line = in
						.readLine()) {
					b.append(line);
				}
				int[] st1 = st1(b.toString());
				if (st1 != null) {
					if (st1[0] > 0 && st1[1] < st1[0] / 15) {
						System.out.println(f.getName());
					}
				} 
//				String[] res = parse(b.toString());
//				if (res == null) {
//					continue;
//				}
//				if (!result.containsKey(res[0])) {
//					result.put(res[0], new HashMap<String, Integer>());
//					counts.put(res[0], 0);
//				}
//				counts.put(res[0], counts.get(res[0])+1);
//				HashMap<String, Integer> stat = result.get(res[0]);
//				if (!stat.containsKey(res[1])) {
//					stat.put(res[1], 0);
//				}
//				Integer count = stat.get(res[1]);
//				stat.put(res[1], count + 1);
				in.close();
			} catch (Exception e) {
				System.out.println(f.getName());
				throw e;
			}
		}

//		BufferedWriter out = new BufferedWriter(new OutputStreamWriter(
//				new FileOutputStream("output.txt"), "UTF-8"));
//
//		ArrayList<String> keys = new ArrayList<String>();
//		Iterator<String> it = counts.keySet().iterator();
//		while (it.hasNext()) {
//			String key = it.next();
//			if (counts.get(key) == null) {
//				System.out.println(key);
//			}
//			keys.add(key);
//		}
//		keys.sort(new Comparator<String>() {
//
//			@Override
//			public int compare(String o1, String o2) {
//				return counts.get(o2).intValue() - counts.get(o1).intValue();
//			}
//		});
//
//		int total = 0;
//		for (String key : keys) {
//			HashMap<String, Integer> v = result.get(key);
//			out.write(key + "\n");
//			Iterator<String> it2 = v.keySet().iterator();
//			while (it2.hasNext()) {
//				String key2 = it2.next();
//				out.write(key2 + ": " + v.get(key2) + "\n");
//				total += v.get(key2);
//			}
//			out.write("\n");
//		}
//
//		out.write("\n");
//		out.write("total: " + total + "\n");
//		out.close();
	}
	
	public static int[] st1(String data) {
		if (!data.contains("制空権確保")) {
			return null;
		}
		int a = data.indexOf("air-stage12");
		int b = data.indexOf("enemy", a);
		String c = data.substring(b, data.indexOf("</tr>", b));
		String[] d = c.split("<td>");
		for (String e : d) {
			if (e.contains("→")) {
				String[] f = e.split(" ");
				String[] g = f[0].split("→");
				return new int[]{ Integer.parseInt(g[0]), Integer.parseInt(g[1]) };
			}
		}
		return null;
	}

	public static String[] parse(String data) {
		int s_eq = data.indexOf("friend-slotitem");
		// Purge first tr
		int c = data.indexOf("</tr>", s_eq) + 5;
		ArrayList<String> touchables = new ArrayList<>();
		for (int j = 0; j < 6; j++) {
			String planeName = "";
			for (int col = 0; col < 11; col++) {
				int s_td = data.indexOf("<td>", c) + 4;
				int e_td = data.indexOf("</td>", s_td);
				String s = data.substring(s_td, e_td);
				if (col > 0) {
					if (col % 2 == 0) {
						if (s.length() > 0) {
							boolean touchable = true;
							for (String noTouch : NO_TOUCH_PLANES) {
								if (planeName.contains(noTouch)) {
									touchable = false;
									break;
								}
							}
							if (touchable) {
								String ps = planeName + "*" + s.split("/")[0];
								touchables.add(ps);
							}
						}
					} else {
						planeName = s;
					}
				}
				c = e_td + 5;
			}
		}
		Collections.sort(touchables);

		// Get touch
		int f = data.indexOf("friend", data.indexOf("air-stage12"));
		String[] touchs = data.substring(f, data.indexOf("</tr>", f)).split(
				"</td>");
		if (touchs.length < 4) {
			return null;
		}
		String touch = touchs[4];
		touch = touch.substring(touch.indexOf("<td>") + 4);

		String[] ret = new String[2];
		StringBuilder b = new StringBuilder();
		for (String s : touchables) {
			b.append(s);
			b.append(",");
		}
		ret[0] = b.toString();
		ret[1] = touch;
		return ret;
	}

}
