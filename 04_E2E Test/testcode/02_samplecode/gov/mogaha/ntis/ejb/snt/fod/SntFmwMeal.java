package gov.mogaha.ntis.ejb.snt.fod;

import javax.ejb.EJBObject;
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.Collection;

public interface SntFmwMeal extends EJBObject {
    public HashMap selectListSNTFMWNewBusin(DefaultParameters param) throws RemoteException;
    public Integer insertSNTFMWNewBusin01(DefaultParameters param) throws RemoteException;
    public Integer updateSNTFMWNewBusin01(DefaultParameters param) throws RemoteException;
    public Integer deleteSNTFMWNewBusin01(DefaultParameters param) throws RemoteException;
}
