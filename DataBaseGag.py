import sqlite3 as sql
#IMPORTANT ---> WE HAVE TO BE IN THE RIGHT FOLDER TO CREATE THE DATABASE 
#BECAUSE THE OTHERS SCRIPTS WILL READ THE DATABASE FROM ITS OWN FOLDER

#CREATES THE DATABASE (JUST 1 TIME UNLESS LOTS OF DATA NEED TO BE UPDATED)
#CreateDB()
def CreateDB():
    conn = sql.connect("./AxionsGag.db")#modificarlo para que si ya existe haga un pass
    conn.commit()
    conn.close()


#CREATES THE TABLE OF THE DATABASE IS THE INTERFACE OF THE DATABASE 
#(ASWELL IT NEEDS TO BE CRATED ONCE UNLESS LOTS OF DATA NEEDS TO BE UPDATED)
#CreataTable
def CreateTable():
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")#modificarlo para que si ya existe haga un pass
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Axions (
        name text , 
        type text ,
        path text ,
        large_panorama integer,
        panorama integer,
        helioscopes integer,
        haloscopes integer,
        lswexps integer,
        projection integer
        )"""
    )
    conn.commit()
    conn.close()
    

#Use to insert one row at a time
#for  example we wnat to introduce a new experiment that appear in panorama and LSWexp
# called new_exp with th type band and it's not a projection
#InsterRow('new_exp',band,0,1,0,0,1,0)
def InsertRow(name, type, path, LP,P,Helios,Halos,LSW ,projection): #PARA AÑADIR UNA SOLA COLUMNA (IDEAL PARA AÑADIR UN EXPERIMENTO NUEVO)
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    instruction = f"INSERT INTO Axions  VALUES ('{name}', '{type}','{path}','{LP}','{P}','{Helios}','{Halos}',{LSW},{projection})"
    cursor.execute(instruction)
    conn.commit()
    conn.close()    


#Use for read all data without ccriteria
#data = ReadRows()
def ReadRows(): 
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    instruction = f"SELECT * FROM Axions"
    cursor.execute(instruction)
    data = cursor.fetchall()
    conn.commit()
    conn.close() 
    print(data)

#Use for inster multiple rows in the form of a list os list with all the parameters and separeted by commas
#
def InsertRows(axionexps): #ESTA ES PARECIDA A LA DE UNA SOLA COLUMNA PERO AÑADIENDO MAS PARA ELLO HAY QUE DEFINIR UNA LISTA DE LISTAS CON LOS EXPERIMENTOS COMO ESTA HECHO MAS ADELANTE
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    instruction = f"INSERT INTO Axions  VALUES (?,?,?,?,?,?,?,?,?)"
    cursor.executemany(instruction,axionexps)
    conn.commit()
    conn.close()


def ReadOrdered(field): #SE USA PARA LEER LA LISTA Y QUE DEVUELVA UN LISTA ORDENADA SEGUN UN CRITERIO
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    #Se lee ordenado alfabeticamente, y de menor a mayor , para la inversa escribir DESC despues de {field}
    instruction = f"SELECT * FROM Axions ORDER BY {field}"
    cursor.execute(instruction)
    data = cursor.fetchall()
    conn.commit()
    conn.close() 
    print(data)


#Use for searching all the data that validate the requesst such as i want all data that appears in panorama (panorama token = 1)
#data = search('panorama',1)
def Search(field, token): 
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    instruction = f"SELECT * FROM Axions WHERE {field} = {token} "
    cursor.execute(instruction)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


#Use for searching the names that validate the request such as i want all the name where the token for panorama is 1
# names = search_names('panorama',1)
def Search_Names(field, token):
    names = []
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    instruction = f"SELECT * FROM Axions WHERE {field} = {token} "
    cursor.execute(instruction)
    data = cursor.fetchall()
    for row in data:
        names.append(row[0])
    conn.commit()
    conn.close()
    return names


#Use for update one value for 1 row such as modifie in qcdband the parameter panorama with value 1 update('qcdband','panorama',1)
#Now the token for panorama for the name qcdband is 1 so it will appear in the panorama plot
def Update(name,field,value): #SE USA PARA MODIFICAR UN ELEMENTO 
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag.db")
    cursor = conn.cursor()
    instruction = f"UPDATE Axions SET '{field}' == {value} WHERE name ='{name}'"
    cursor.execute(instruction)

    conn.commit()
    conn.close() 


#Use for deleting a row with its name such as if i want to delete the qcdband
#deleteRow('qcdband')
def DeleteRow(name): #PARA ELIMINAR UNA FILA
    conn = sql.connect("/home/tfg_2022_1/git/axion-limits/AxionsGag..db")
    cursor = conn.cursor()
    instruction = f"DELETE FROM Axions WHERE name = '{name}' "
    cursor.execute(instruction)
    conn.commit()
    conn.close() 

#CREO QUE NO HACE FALTA PONER EL PATH PERO DE MOMENTO SE QUEDA
path = "/home/tfg_2022_1/git/axion-limits/data/axion/data/axion/"

#InsertRow("name","band",path + "/name.dat",Large_Panorama,Panaroma,Helios,Halos,LSW,Projection)
#ReadRows()
axionsexps= [
    ["qcdband", "band", path + "QCD_band.dat", 1, 1, 1, 1, 1, 0],
    ["ksvz", "region", path + "ksvz.dat", 1, 1, 1, 1, 1, 0],
    ["dfsz", "region", path + "dfsz.dat", 0, 1, 0, 0, 0, 0],
    ["ADMX2018", "band", path + "ADMX2018.txt", 1, 1, 1, 1, 0, 0],
    ["ADMX2019", "band", path + "ADMX2019.dat", 1, 1, 1, 1, 0, 0],
    ["ADMX2019_1", "band", path + "ADMX2019_1.txt", 0, 0, 0, 0, 0, 0],
    ["ADMX2019_2", "band", path + "ADMX2019_2.txt", 0, 0, 0, 0, 0, 0],
    ["ADMX2021", "band", path + "ADMX2021.txt", 1, 1, 1, 1, 0, 0],
    ["ADMX_sidecar", "band", path + "ADMX_sidecar.txt", 1, 1, 1, 1, 0, 0],
    ["admx", "band", path + "admx.txt", 1, 1, 1, 1, 0, 0],
    ["admx_hf_2016", "band", path + "admx_hf_2016.dat", 1, 1, 1, 0, 0, 0],
    ["CAPP-8TB", "band", path + "CAPP-8TB.txt", 1, 1, 1, 1, 0, 0],
    ["CAPP_multicell", "band", path + "CAPP_multicell_2020.dat", 0, 0, 0, 1, 0, 0],
    ["CAPP2021", "band", path + "CAPP2021.txt", 0, 1, 0, 1, 0, 0],
    ["HAYSTAC", "band", path + "HAYSTAC.txt", 1, 1, 1, 1, 0, 0],
    ["HAYSTAC2020", "band", path + "haystac2020.txt", 1, 1, 1, 1, 0, 0],
    ["ORGAN", "band", path + "ORGAN.txt", 1, 1, 1, 1, 0, 0],
    ["QUAX", "band", path + "QUAX.txt", 1, 1, 1, 1, 0, 0],
    ["QUAX2021", "band", path + "QUAX2021.txt", 1, 1, 1, 1, 0, 0],
    ["RADES2021", "band", path + "RADES2021.txt", 1, 1, 1, 1, 0, 0],
    ["THintMayer", "region", path + "Mayer_2013.dat", 0, 0, 1, 0, 1, 1],
    ["THintCIBER", "region", path + "CIBER_contour_data.dat", 0, 0, 0, 0, 1, 1],
    ["HBhint", "region", path + "hints/HB_hint.dat", 0, 0, 1, 0, 1, 1],
    ["ABRA10cm", "band", path + "ABRA10cm.txt", 0, 0, 0, 0, 0, 0],
    ["BASE_2021", "band", path + "BASE2021.txt", 0, 0, 1, 0, 0, 0],
    ["ADMX_SLIC", "band", path + "ADMX_SLIC.txt", 1, 1, 1, 1, 0, 0],
    ["hess", "band", path + "hess.dat", 1, 1, 1, 0, 1, 0],
    ["mrk421", "band", path + "Mrk421.txt", 1, 1, 1, 0, 1, 0],
    ["sn1987a_photon", "band", path + "sn1987a_photon.dat", 1, 1, 1, 0, 1, 0],
    ["FERMI_NG1275", "region", path + "FERMI_NG1275_region.dat", 1, 1, 1, 0, 1, 0],
    ["SN1987energyloss", "band", path + "cosmoalp/SN1987energyloss.txt", 1, 0, 0, 0, 0, 0],
    ["Xray", "band", path + "cosmoalp/Xray.txt", 1, 0, 0, 0, 0, 0],
    ["Deut2016", "region", path + "cosmoalp/Deut2016.txt", 1, 0, 0, 0, 0, 0],
    ["OpticalDepthTerm", "band", path + "cosmoalp/OpticalDepthTerm.txt", 1, 0, 0, 0, 0, 0],
    ["gEBL1", "band", path + "cosmoalp/gEBL1.txt", 1, 0, 0, 0, 0, 0],
    ["EBL2", "region", path + "cosmoalp/EBL2.txt", 1, 0, 0, 0, 0, 0],
    ["cmb_mu", "region", path + "cosmoalp/CMB_mu.txt", 1, 0, 0, 0, 0, 0],
    ["CMB_DEsuE", "band", path + "cosmoalp/CMB_DEsuE.txt", 0, 0, 0, 0, 0, 0],
    ["Overduin", "region", path + "cosmoalp/Overduin.txt", 1, 0, 0, 0, 0, 0],
    ["Ressell", "band", path + "cosmoalp/Ressell.txt", 1, 0, 0, 0, 0, 0],
    ["endlist2_gamma_projimprov", "band", path + "endlist2_gamma_projimprov.txt", 1, 1, 1, 0, 0, 0],
    ["HBalpbound", "band", path + "HBalpbound.txt", 1, 0, 0, 0, 0, 0],
    ["HBalpbound_l", "line", path + "HBalpbound.txt", 0, 1, 1, 0, 0, 0],
    ["telescopes", "band", path + "telescopes.dat", 1, 1, 1, 0, 0, 0],
    ["telescopes_new", "band", path + "telescopes_new.dat", 1, 1, 1, 0, 0, 0],
    ["solar_nu", "band", path + "ALPSun_nu.txt", 1, 1, 1, 0, 0, 0],
    ["ADMXprosp_2GHz", "band", path + "ADMX_prospects_2GHz.dat", 1, 1, 0, 1, 0, 1],
    ["ADMXprosp_10GHz", "band", path + "ADMX_prospects_10GHz.dat", 1, 1, 0, 1, 0, 1],
    ["ADMXprosp_2GHz_l", "line", path + "ADMX_prospects_2GHz.dat", 1, 1, 0, 1, 0, 1],
    ["ADMXprosp_10GHz_l", "line", path + "ADMX_prospects_10GHz.dat", 1, 1, 0, 1, 0, 1],
    ["CAPP4", "line", path + "CAPP4.dat", 0, 1, 0, 0, 0, 1],
    ["MADMAX", "band", path + "MADMAX.dat", 0, 1, 0, 0, 0, 1],
    ["CAPP4_l", "line", path + "CAPP4.dat", 1, 0, 0, 1, 0, 1],
    ["MADMAX_l", "line", path + "MADMAX.dat", 1, 1, 0, 1, 0, 1],
    ["ORGANprosp", "line", path + "ORGAN2.dat", 1, 1, 0, 1, 0, 1],
    ["castcapp2", "band", path + "CASTCAPP2.dat", 0, 1, 0, 0, 0, 1],
    ["ABRA1", "band", path + "ABRAres_1.dat", 1, 1, 0, 1, 0, 1],
    ["ABRA1_l", "line", path + "ABRAres_1.dat", 1, 0, 0, 0, 0, 1],
    ["ABRA2", "line", path + "ABRAres_2.dat", 0, 0, 0, 1, 0, 1],
    ["ABRA3", "line", path + "ABRAres_3.dat", 0, 0, 0, 1, 0, 1],
    ["ABRA1_l", "line", path + "ABRAres_1.dat", 1, 0, 0, 0, 0, 1],
    ["ABRA_2021_l", "line", path + "ABRA_2021.txt", 0, 0, 0, 0, 0, 1],
    ["KLASH", "line", path + "KLASH.dat", 0, 1, 0, 1, 0, 1],
    ["old_haloscopes", "band", path + "MicrowaveCavities.txt", 1, 1, 1, 1, 0, 0],
    ["IAXODM", "band", path + "IAXODM.dat", 0, 1, 0, 0, 0, 1],
    ["IAXODM_l", "line", path + "ORGAN2.dat", 0, 1, 0, 0, 0, 1],
    ["CAST", "band", path + "cast_env_2016.dat", 1, 1, 1, 1, 1, 0],
    ["SHAFT", "band", path + "SHAFT.txt", 0, 1, 1, 0, 0, 0],
    ["ABRA_2021", "band", path + "ABRA_2021.txt", 0, 1, 1, 0, 0, 0],
    ["BabyIAXO", "band", path + "miniIAXO.dat", 1, 1, 1, 1, 0, 1],
    ["IAXO", "band", path + "IAXO_nominal.txt", 0, 1, 1, 1, 0, 1],
    ["IAXOplus", "band", path + "IAXO_plus.txt", 1, 1, 1, 1, 0, 1],
    ["ALPSII", "band", path + "ALPSII.dat", 1, 0, 1, 0, 1, 1],
    ["TOORAD", "line", path + "TOORAD2.txt", 0, 0, 0, 1, 0, 1],
    ["BRASS", "line", path + "BRASS.txt", 0, 0, 0, 1, 0, 1],
    ["STAX1", "line", path + "STAX1.dat", 0, 0, 0, 0, 1, 1],
    ["STAX2", "line", path + "STAX2.dat", 0, 0, 0, 0, 1, 1],
    ["BabyIAXO_l", "line", path + "miniIAXO.dat", 1, 1, 1, 1, 0, 1],
    ["IAXO_l", "line", path + "IAXO_nominal.txt", 0, 1, 1, 1, 0, 1],
    ["IAXOplus_l", "line", path + "IAXO_plus.txt", 1, 1, 1, 1, 0, 1],
    ["ALPSII_l", "line", path + "ALPSII.dat", 1, 1, 1, 0, 0, 1],
    ["KLASH_l", "line", path + "KLASH.dat", 0, 0, 0, 0, 0, 1],
    ["AMELIE", "line", path + "amelie_1m3_arXiv_1508.03006.txt", 0, 0, 1, 0, 0, 1],
    ["JURA", "line", path + "ALPSIII.dat", 0, 0, 0, 0, 1, 1],
    ["OSCAR2015", "band", path + "osqar2015.dat", 1, 1, 1, 0, 1, 0],
    ["PVLAS2015", "band", path + "pvlas2015.dat", 1, 1, 1, 0, 1, 0],
    ["ALPSI", "band", path + "ALPSI.dat", 0, 1, 1, 0, 1, 0],
    ["CROWS", "band", path + "CROWS.txt", 1, 0, 0, 0, 1, 0],
    ["BeamDump", "region", path + "llSLAC137.txt", 1, 0, 0, 0, 0, 0]]
#CreateDB()
#RreateTable()
#InsertRows(axionsexps)
#ReadOrdered("name")
data=Search("large_panorama",1) #devuelve una lista de lista con los elementos buscados
#print(data)

name = Search_Names("large_panorama",1)
#print(name)
#print(names)
#
#deleteRow()
#for name in names:
    #print(name)