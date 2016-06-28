import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;

public class Veteran {

	static final int SLOT = 3;
	static final int KOUKU_POWER = 67;
	static final int HOUGEKI_POWER = 132;
	static final String TYPE = "bak"; // bak or rai
	static final int MAX_ARMOR = (int) (13 * 1.3 - 0.6);
	final static boolean FIRST_SLOT = true;

	final static int CRITICAL_KOUKU_DAMAGE = (int) (KOUKU_POWER * 1.5 * (1 + ((FIRST_SLOT ? 0.1
			: 0) + 0.1 * SLOT)));
	final static int CRITICAL_HOUGEKI_DAMAGE = (int) (HOUGEKI_POWER * 1.5 * (1 + ((FIRST_SLOT ? 0.1
			: 0) + 0.1 * SLOT)));

	public static void main(String[] args) throws Exception {
		File[] files = new File(
				"C:/Users/Romulus/Documents/Dropbox/GreenSofts/ElectronicObserver/json")
				.listFiles();

		Counter stage3 = new Counter();
		Counter housen = new Counter();

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
			String json = in.readLine();

			// 航空攻撃
			String[] targets = StrJsonFinder.findObject(json,
					"api_e" + TYPE + "_flag").split(",");
			int distribute = 0;
			for (String s : targets) {
				if (s.equals("1")) {
					distribute++;
				}
			}
			String[] dmgs = StrJsonFinder.findObject(json, "api_edam").split(
					",");
			String[] ecls = StrJsonFinder.findObject(json, "api_ecl_flag")
					.split(",");
			if (distribute == SLOT) {
				// 重複攻撃なし、そのままeclが結果になる
				for (int i = 1; i < ecls.length; i++) {
					if (ecls[i].equals("1")) {
						stage3.tick("CL1");
					} else {
						if (Double.parseDouble(dmgs[i]) > 0) {
							stage3.tick("CL0");
						} else if (targets[i].equals("1")) {
							stage3.tick("MISS");
						}
					}
				}
			} else {
				// 重複攻撃あり、ダメージで結果を推測する
				switch (SLOT) {
				case 2:
					for (int i = 1; i < targets.length; i++) {
						if (targets[i].equals("1")) {
							double dmg = Double.parseDouble(dmgs[i]);
							// 同じスロットを攻撃した、結果は6通り
							if (dmg == 0) {
								// MISS + MISS
								stage3.tick("MISS", 2);
							} else if (ecls[i].equals("1")) {
								if (dmg > (CRITICAL_KOUKU_DAMAGE * 2 - MAX_ARMOR * 2)) {
									// CL1 + CL1, 34はホ級の最大装甲の二倍
									// クリダメージ低すぎてこれで判断ミスるような積み方しないように
									stage3.tick("CL1", 2);
								} else if (dmg > CRITICAL_KOUKU_DAMAGE
										+ KOUKU_POWER - 34) {
									// CL1 + CL0
									stage3.tick("CL1");
									stage3.tick("CL0");
								} else if (dmg > CRITICAL_KOUKU_DAMAGE
										- MAX_ARMOR) {
									// CL1 + MISS
									stage3.tick("CL1");
									stage3.tick("MISS");
								} else {
									System.err.println("Error! dmg=" + dmg
											+ ", fname=" + fname);
								}
							} else {
								if (dmg < KOUKU_POWER) {
									// MISS + CL0
									// 装甲があるので威力より少し低いことになる
									// 航空威力は装甲の三倍以上あると推定が楽
									stage3.tick("MISS");
									stage3.tick("CL0");
								} else if (dmg > KOUKU_POWER
										&& dmg < KOUKU_POWER * 2) {
									// CL0 + CL0
									stage3.tick("CL0", 2);
								} else {
									System.err.println("Error! dmg=" + dmg
											+ ", fname=" + fname);
								}
							}
							break;
						}
					}
					break;
				case 3:
					// 1+2
					for (int i = 1; i < targets.length; i++) {
						if (targets[i].equals("1")) {
							if (ecls[i].equals("1")) {

							} else {

							}
						}
					}
					break;
				default:
					System.err.println("Error!, fname=" + fname);
					break;
				}
			}

			// 砲撃戦、こちらの1回目の攻撃のみを集計するので注意
			String h1 = StrJsonFinder.findObject(json, "api_hougeki1");
			if (h1.length() > 0 && !h1.equals("null")) {
				String cls = StrJsonFinder.findObject(h1, "api_cl_list");
				String cl = cls.split(",")[1];
				switch (cl) {
				case "[0]":
					housen.tick("MISS");
					break;
				case "[1]":
					housen.tick("CL1");
					break;
				case "[2]":
					housen.tick("CL2");
					break;
				}
			}

			in.close();
		}
		System.out.print("航空戦　");
		System.out.println(stage3.dump());
		System.out.print("砲撃戦　");
		System.out.println(housen.dump());
	}
}
