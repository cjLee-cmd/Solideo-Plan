package gov.mogaha.ntis.web.snt.fod.action;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;

import gov.mogaha.ntis.ejb.snt.fod.SntFmwMeal;
import gov.mogaha.ntis.web.snt.common.SntAction;
import gov.mogaha.ntis.web.snt.common.SSOSessionUtil;
import gov.mogaha.ntis.web.snt.common.DefaultParameters;

public class SntFmwMealAction extends SntAction {

    public ActionForward selectListSNTFMWNewBusin(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception {
        HashMap hm = (HashMap) invokeLocal(request);
        
        Collection res1 = (Collection) hm.get("res_sntfmwnewbusinapplyi");
        Collection res2 = (Collection) hm.get("resg1_sntfmwnewbusinapplyi");
        
        try {
            request.setAttribute("res_sntfmwnewbusinapplyi", (ArrayList) res1);
            request.setAttribute("resg1_sntfmwnewbusinapplyi", (ArrayList) res2);
        } catch (NullPointerException ex) { Log.error(NTIS_COMMON_DEFINE.SNTLOG, "NPE"); }
          catch (Exception e)             { Log.error(NTIS_COMMON_DEFINE.SNTLOG, "ERR"); }
        
        return null;
    }

    public ActionForward insertSNTFMWNewBusin01(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception {
        request.setAttribute("getUserID", SSOSessionUtil.getUserID(request));
        request.setAttribute("getDeptID", SSOSessionUtil.getDeptID(request));
        request.setAttribute("", invokeLocal(request));
        return null;
    }

    public ActionForward updateSNTFMWNewBusin01(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception {
        request.setAttribute("getUserID", SSOSessionUtil.getUserID(request));
        request.setAttribute("getDeptID", SSOSessionUtil.getDeptID(request));
        request.setAttribute("", invokeLocal(request));
        return null;
    }

    public ActionForward deleteSNTFMWNewBusin01(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception {
        request.setAttribute("getUserID", SSOSessionUtil.getUserID(request));
        request.setAttribute("getDeptID", SSOSessionUtil.getDeptID(request));
        request.setAttribute("", invokeLocal(request));
        return null;
    }
}
