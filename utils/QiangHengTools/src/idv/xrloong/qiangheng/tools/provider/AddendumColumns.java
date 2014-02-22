package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class AddendumColumns implements BaseColumns {
	public static final String TABLE_NAME = "addendum";

	public static final String AUTHORITY = FindCommonComponentProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/addendum");

	public static final String NAME = "name";
	public static final String DB_NAME = "db_name";
	public static final String RANGE_EXPRESSION = "range_expression";
}
