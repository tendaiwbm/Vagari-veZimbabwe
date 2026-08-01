from geo.utils import query_munyayi

def admin_name_validator(qDictIn):
    names = [name[0] for name in query_munyayi(f''' SELECT DISTINCT({qDictIn["admin"]}_name) FROM prelim.ward ''')]
    for name in qDictIn["admin-names"].split(";"):
        try:
            assert name in names
        except:
            raise ValueError(f"""Distribution does not understand input '{name}'""")

def admin_validator(qDictIn):
    vDict = {"ward":"ward","district":"district","province":"province"}
    try:
        adminLevel = vDict[qDictIn["admin"]]
    except:
        raise ValueError(f"Distribution does not understand input '{qDict['admin-level']}'.")
    return True

def distro_validator(qDictIn):
    vDict = {
             "category": {"distribution":"distribution"},
             "sex":      {"total":"total","male":"male","female":"female"},
             "year":     {"2002":"2002","2012":2012,"2022":"2022"},
             "grain":    {"district":"district","ward":"ward","province":"province"}
            }
    qDictOut = {}
    for key in qDictIn:
        if "admin" not in key:
            try:
                qDictOut.setdefault(key,vDict[key][qDictIn[key]])
            except:
                raise ValueError(f"""Distribution does not understand input '{key}'.""")
        elif key == "admin":
            admin_validator(qDictIn)
        elif key == "admin-names":
            admin_name_validator(qDictIn)
    return True
