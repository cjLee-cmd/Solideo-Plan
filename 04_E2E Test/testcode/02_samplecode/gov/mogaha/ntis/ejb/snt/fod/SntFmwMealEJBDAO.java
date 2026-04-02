package gov.mogaha.ntis.ejb.snt.fod;

import gov.mogaha.ntis.web.snt.common.DefaultParameters;
import gov.mogaha.ntis.web.snt.common.QueryService;
import gov.mogaha.ntis.web.snt.common.StringUtil;
import gov.mogaha.ntis.web.snt.common.SaveResultSet;
import gov.mogaha.ntis.web.snt.common.Tokenizer;
import gov.mogaha.ntis.web.snt.common.CCDEncryption;
import java.util.HashMap;
import java.util.Collection;
import java.util.ArrayList;

public class SntFmwMealEJBDAO {
    private QueryService queryservice = null;
    private CCDEncryption ccdEnc = new CCDEncryption();

    public QueryService getQueryservice() {
        return queryservice;
    }

    public void setQueryservice(QueryService queryservice) {
        this.queryservice = queryservice;
    }

    public HashMap selectListSNTFMWNewBusin(DefaultParameters param) throws Exception {
        String mw_take_no = StringUtil.isNullTrim(param.getParameter("mw_take_no"));

        Collection res1 = getQueryservice().find("SntFmwMealEJBDAO.selectListSNTFMWNewBusin01", new String[]{mw_take_no});
        Collection res2 = getQueryservice().find("SntFmwMealEJBDAO.selectListSNTFMWNewBusin02", new String[]{mw_take_no});
        res2 = ccdEnc.sntDecryptCol(res2, "sid");

        HashMap hm = new HashMap();
        hm.put("res_sntfmwnewbusinapplyi", res1);
        hm.put("resg1_sntfmwnewbusinapplyi", res2);
        return hm;
    }

    public Integer insertSNTFMWNewBusin01(DefaultParameters param) throws Exception {
        String mw_take_no = StringUtil.isNullTrim(param.getParameter("mw_take_no"));
        String busin_type = StringUtil.isNullTrim(param.getParameter("busin_type"));
        String appl_cnt = StringUtil.isNullTrim(param.getParameter("appl_cnt"));
        String ssn_no = param.getParameter("ssn_no");
        String telno = param.getParameterNoTrim("telno");

        Object[] params = {
            mw_take_no,
            busin_type,
            appl_cnt,
            ccdEnc.sntEncrypt(ssn_no),
            telno
        };

        getQueryservice().update("SntFmwMealEJBDAO.insertSNTFMWNewBusin01", params);
        return new Integer(0);
    }

    public Integer updateSNTFMWNewBusin01(DefaultParameters param) throws Exception {
        String mw_take_no = StringUtil.isNullTrim(param.getParameter("mw_take_no"));
        String busin_type = StringUtil.isNullTrim(param.getParameter("busin_type"));
        String appl_cnt = StringUtil.isNullTrim(param.getParameter("appl_cnt"));
        String ssn_no = param.getParameter("ssn_no");
        String telno = param.getParameterNoTrim("telno");

        Object[] params = {
            busin_type,
            appl_cnt,
            ccdEnc.sntEncrypt(ssn_no),
            telno,
            mw_take_no
        };

        getQueryservice().update("SntFmwMealEJBDAO.updateSNTFMWNewBusin01", params);
        return new Integer(0);
    }

    public Integer deleteSNTFMWNewBusin01(DefaultParameters param) throws Exception {
        String mw_take_no = StringUtil.isNullTrim(param.getParameter("mw_take_no"));

        Object[] params = { mw_take_no };
        getQueryservice().update("SntFmwMealEJBDAO.deleteSNTFMWNewBusin01", params);
        return new Integer(0);
    }

    public Integer insertSNTFMWNewMealDetailIP01(DefaultParameters param) throws Exception {
        String mw_take_no = StringUtil.isNullTrim(param.getParameter("mw_take_no"));
        ArrayList insList = new ArrayList(), upsList = new ArrayList(), delList = new ArrayList();

        SaveResultSet rs = new SaveResultSet();
        Tokenizer.getSaveResultSet(param.getParameter("cud_data"), "smode", rs, "^", "|");

        while (rs.next()) {
            String[] row = { mw_take_no, rs.get("필드명") };
            if      ("i".equals(rs.get("smode"))) insList.add(row);
            else if ("u".equals(rs.get("smode"))) upsList.add(row);
            else if ("d".equals(rs.get("smode"))) delList.add(row);
        }

        if (insList.size() > 0) getQueryservice().batchUpdate("SntFmwMealEJBDAO.insertXXX", insList);
        if (upsList.size() > 0) getQueryservice().batchUpdate("SntFmwMealEJBDAO.updateXXX", upsList);
        if (delList.size() > 0) getQueryservice().batchUpdate("SntFmwMealEJBDAO.deleteXXX", delList);

        return new Integer(0);
    }
}
