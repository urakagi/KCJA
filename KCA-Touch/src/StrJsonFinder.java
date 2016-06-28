public class StrJsonFinder {

	public static String findObject(String json, String key, boolean trim) {
		String qkey = "\"" + key + "\":";
		int idx = json.indexOf(qkey);
		if (idx < 0) {
			idx = json.indexOf(key);
			if (idx < 0) {
				return "";
			}
			idx += key.length();
		} else {
			idx += qkey.length();
		}
		char openChar = json.charAt(idx);
		String closeChars;
		boolean checkNest;
		switch (openChar) {
		case '[':
			closeChars = "]";
			checkNest = true;
			break;
		case '{':
			closeChars = "}";
			checkNest = true;
			break;
		default:
			closeChars = ",]}";
			checkNest = false;
			break;
		}
		int nestCount = 0;
		StringBuilder b = new StringBuilder();
		b.append(openChar);
		for (idx++; idx < json.length(); idx++) {
			char c = json.charAt(idx);
			b.append(c);
			if (closeChars.indexOf(c) >= 0) {
				if (nestCount == 0) {
					if (trim) {
						if (openChar == '[' || openChar == '{') {
							b.deleteCharAt(0);
						}
						b.deleteCharAt(b.length() - 1);
					}
					return b.toString();
				} else {
					nestCount--;
				}
			}
			if (checkNest && c == openChar) {
				nestCount++;
			}
		}
		System.err.println("Error, json=" + json + "\nkey=" + key);
		return "";
	}
	
	public static String findObject(String json, String key) {
		return findObject(json, key, true);
	}

}
