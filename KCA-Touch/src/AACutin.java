import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;

import org.json.JSONObject;

public class AACutin {

	public static void main(String[] args) throws Exception {
		File[] files = new File(
				"C:/Users/Romulus/Documents/Dropbox/GreenSofts/KCRDB/json")
				.listFiles();
		int total = 0;
		int aacutin = 0;
		int cimax = Integer.MIN_VALUE;
		int nocimax = Integer.MIN_VALUE;
		int cimin = Integer.MAX_VALUE;
		int nocimin = Integer.MAX_VALUE;
		for (File f : files) {
			if (!f.getName().contains("sortie_battle")) {
				continue;
			}
			BufferedReader in = new BufferedReader(new InputStreamReader(
					new FileInputStream(f)));
			in.readLine();
			String line = in.readLine();
			line = line.substring(line.indexOf("svdata=") + 7);
			JSONObject root = new JSONObject(line);
			root = (JSONObject) root.get("api_data");
			JSONObject kouku = (JSONObject) root.get("api_kouku");
			if (kouku.isNull("api_stage2")) {
				continue;
			}
			JSONObject stage2 = kouku.getJSONObject("api_stage2");
			int ecount = stage2.getInt("api_e_count");
			if (ecount == 0) {
				continue;
			}
			total++;
			int kind = 0;
			boolean ci = stage2.has("api_air_fire");
			if (ci) {
				kind = stage2.getJSONObject("api_air_fire").getInt("api_kind");
				aacutin++;
			}
			int elostcount = stage2.getInt("api_e_lostcount");
			if (ci) {
				if (elostcount > cimax) {
					cimax = elostcount;
				}
				if (elostcount < cimin) {
					cimin = elostcount;
				}
				System.out.println("CI-" + kind + ", " + elostcount + "/" + ecount);
			} else {
				if (elostcount > nocimax) {
					nocimax = elostcount;
				}
				if (elostcount < nocimin) {
					nocimin = elostcount;
				}
				System.out.println("No-CI, " + elostcount + "/" + ecount);
			}
			in.close();
		}
		System.out.println();
		System.out.println("Total:" + total);
		System.out.println(String.format("対空CI発動:%d (%.2f%%)", aacutin, aacutin
				* 100.0 / total));
		System.out.println();
		System.out.println(String.format("CI時最多撃墜 %d、最少撃墜 %d", cimax, cimin));
		System.out.println(String.format("非CI時最多撃墜 %d、最少撃墜 %d", nocimax, 
				nocimin));
	}
	// }
}
