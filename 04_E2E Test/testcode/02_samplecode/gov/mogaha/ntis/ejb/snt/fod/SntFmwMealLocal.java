package gov.mogaha.ntis.ejb.snt.fod;

import javax.ejb.EJBLocalObject;
import java.util.HashMap;
import java.util.Collection;

public interface SntFmwMealLocal extends EJBLocalObject {
    public HashMap selectListSNTFMWNewBusin(DefaultParameters param);
    public Integer insertSNTFMWNewBusin01(DefaultParameters param);
    public Integer updateSNTFMWNewBusin01(DefaultParameters param);
    public Integer deleteSNTFMWNewBusin01(DefaultParameters param);
}
