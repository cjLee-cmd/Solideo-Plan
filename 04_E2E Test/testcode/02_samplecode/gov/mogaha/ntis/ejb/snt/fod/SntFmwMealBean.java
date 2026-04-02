package gov.mogaha.ntis.ejb.snt.fod;

import javax.ejb.SessionBean;
import javax.ejb.SessionContext;
import javax.ejb.EJBException;
import javax.ejb.TransactionRolledbackLocalException;

import gov.mogaha.ntis.web.snt.common.DefaultParameters;
import gov.mogaha.ntis.web.snt.common.DefaultEJBException;
import gov.mogaha.ntis.web.snt.common.SDBException;
import gov.mogaha.ntis.web.snt.common.SSOSessionUtil;
import java.util.HashMap;
import java.util.Collection;

public class SntFmwMealBean implements SessionBean {
    private SessionContext sessionContext;
    private SntFmwMealEJBDAO ped = new SntFmwMealEJBDAO();

    public void setSessionContext(SessionContext sessionContext) {
        this.sessionContext = sessionContext;
    }

    public void ejbCreate() throws EJBException {
    }

    public void ejbActivate() throws EJBException {
    }

    public void ejbPassivate() throws EJBException {
    }

    public void ejbRemove() throws EJBException {
    }

    public HashMap selectListSNTFMWNewBusin(DefaultParameters param) throws DefaultEJBException {
        try {
            return ped.selectListSNTFMWNewBusin(param);
        } catch (SDBException ex) {
            getSessionContext().setRollbackOnly();
            throw processException("SNTE6010", ex);
        } catch (Exception ex) {
            getSessionContext().setRollbackOnly();
            throw processException("NTIS0001", ex);
        }
    }

    public Integer insertSNTFMWNewBusin01(DefaultParameters param) throws DefaultEJBException {
        try {
            return ped.insertSNTFMWNewBusin01(param);
        } catch (SDBException ex) {
            getSessionContext().setRollbackOnly();
            throw processException("SNTE6010", ex);
        } catch (Exception ex) {
            getSessionContext().setRollbackOnly();
            throw processException("NTIS0001", ex);
        }
    }

    public Integer updateSNTFMWNewBusin01(DefaultParameters param) throws DefaultEJBException {
        try {
            return ped.updateSNTFMWNewBusin01(param);
        } catch (SDBException ex) {
            getSessionContext().setRollbackOnly();
            throw processException("SNTE6010", ex);
        } catch (Exception ex) {
            getSessionContext().setRollbackOnly();
            throw processException("NTIS0001", ex);
        }
    }

    public Integer deleteSNTFMWNewBusin01(DefaultParameters param) throws DefaultEJBException {
        try {
            return ped.deleteSNTFMWNewBusin01(param);
        } catch (SDBException ex) {
            getSessionContext().setRollbackOnly();
            throw processException("SNTE6010", ex);
        } catch (Exception ex) {
            getSessionContext().setRollbackOnly();
            throw processException("NTIS0001", ex);
        }
    }

    private SessionContext getSessionContext() {
        return sessionContext;
    }

    private DefaultEJBException processException(String errorCode, Exception ex) {
        return new DefaultEJBException(errorCode, ex);
    }
}
