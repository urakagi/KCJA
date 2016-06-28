import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class Counter {

	HashMap<String, Integer> data = new HashMap<>();

	public void tick(String key, int times) {
		if (data.containsKey(key)) {
			data.put(key, data.get(key) + times);
		} else {
			data.put(key, times);
		}
	}

	public void tick(String key) {
		tick(key, 1);
	}

	public String dump() {
		int total = 0;
		for (Integer c : data.values()) {
			total += c;
		}

		StringBuilder b = new StringBuilder();
		b.append("Total:" + total + "\n");

		ArrayList<String> acs = new ArrayList<>(data.keySet());
		Collections.sort(acs);
		for (String s : acs) {
			b.append(String.format("%s:%d (%.1f%%)\n", s, data.get(s),
					data.get(s) * 100.0 / total));
		}

		return b.toString();
	}

}
